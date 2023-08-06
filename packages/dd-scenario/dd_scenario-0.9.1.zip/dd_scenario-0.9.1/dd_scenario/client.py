# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------


import json
import requests
import os

from six import string_types

try:
    from urllib import urlencode
except ImportError:
    # py3
    from urllib.parse import urlencode

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from six import iteritems
import time

from .container import Container, get_container_name
from dd_scenario.model_builder import ModelBuilder, get_model_builder_id
from .asset import Asset, get_asset_name
from .table import Table, get_table_name, TableType
from .solve import SolveStatus, SolveConfig

content_json = {'Content-Type': 'application/json'}
content_octet_stream = {'Content-Type': 'application/octet-stream',
                        'Content-Encoding': 'identity'}
content_csv = {'Content-Type': 'text/csv'}
accept_csv = {'Content-Type': 'application/json',
              'Accept': 'text/csv'}

def display_headers(session, headers=None):
    h = {}
    h.update(session.headers)
    h.update(headers)
    print(json.dumps(h, indent=3))


class DDException(Exception):
    '''The base exception for the Decision Optimization client.

    Attributes:
        errors: A list of errors as [{'code': code, 'message': message}]
        trace: The trace id
        message: a string representation of the errors
    '''
    def __init__(self, json_def):
        self.errors = json_def['errors']
        self.trace = json_def.get('trace')
        super(DDException, self).__init__(self.message)

    @property
    def message(self):
        m = [('%s:%s' % (x['code'], x['message'])) for x in self.errors]
        return '\n'.join(m)

class DDClientException(Exception):
    '''Generic client exception
    '''
    pass


class IAMAuthHandler(object):
    def __init__(self, apikey):
        self.apikey = apikey

    def get_authorization(self):
        from project_lib.utils import environment as pcl_env  # @UnresolvedImport
        iam_api = pcl_env.get_iam_service_url()
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'cache-control': 'no-cache'
            }
        data = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey={apikey}&response_type=cloud_iam'.format(apikey=self.apikey)
        r = requests.post(iam_api, headers=headers, data=data)
        if r.status_code == 200:
            iam_info = json.loads(r.content.decode(r.encoding if r.encoding else 'utf-8'))
            if not 'access_token' in iam_info:
                raise DDClientException('Could not request access_token from IAM server')
            return iam_info['access_token']
        else:
            r.raise_for_status()

    def get_api_url(self):
        from project_lib.utils import environment as pcl_env  # @UnresolvedImport
        return '%s/v2' % pcl_env.get_common_api_url()




class Client(object):
    '''The class to access containers in Decision Optimization.

    To use the client::

        from dd_scenario import Client
        client = Client()

    or if you want to access another project::

        from dd_scenario import Client
        client = Client(project_id="project id string",
                        authorization="bearer authorization token",
                        api_url='https://localhost/dd-scenario-api/v2')

    Then use methods to work with scenario assets, tables and data:

    * Methods to work with model builders

        * :meth:`~dd_scenario.Client.get_model_builders`
        * :meth:`~dd_scenario.Client.create_model_builder`
        * :meth:`~dd_scenario.Client.get_model_builder`
        * :meth:`~dd_scenario.Client.update_model_builder`
        * :meth:`~dd_scenario.Client.delete_model_builder`

    * Methods to work with containers

        * :meth:`~dd_scenario.Client.get_containers`
        * :meth:`~dd_scenario.Client.create_container`
        * :meth:`~dd_scenario.Client.get_container`
        * :meth:`~dd_scenario.Client.update_container`
        * :meth:`~dd_scenario.Client.copy_container`
        * :meth:`~dd_scenario.Client.delete_container`

    * Methods to work with assets

        * :meth:`~dd_scenario.Client.get_assets`
        * :meth:`~dd_scenario.Client.create_asset`
        * :meth:`~dd_scenario.Client.get_asset`
        * :meth:`~dd_scenario.Client.update_asset`
        * :meth:`~dd_scenario.Client.delete_asset`
        * :meth:`~dd_scenario.Client.get_asset_data`

    * Methods to work with tables

        * :meth:`~dd_scenario.Client.get_tables`
        * :meth:`~dd_scenario.Client.create_table`
        * :meth:`~dd_scenario.Client.get_table`
        * :meth:`~dd_scenario.Client.add_table`
        * :meth:`~dd_scenario.Client.delete_table`
        * :meth:`~dd_scenario.Client.get_tables_type`
        * :meth:`~dd_scenario.Client.get_table_type`
        * :meth:`~dd_scenario.Client.update_table_type`
        * :meth:`~dd_scenario.Client.get_table_data`
        * :meth:`~dd_scenario.Client.add_table_data`
        * :meth:`~dd_scenario.Client.delete_table_data`

    * Solve api:

        * :meth:`~dd_scenario.Client.solve`
        * :meth:`~dd_scenario.Client.stop_solve`
        * :meth:`~dd_scenario.Client.get_solve_status`
        * :meth:`~dd_scenario.Client.wait_for_completion`

    * Notebook import/export:

        * :meth:`~dd_scenario.Client.import_notebook`
        * :meth:`~dd_scenario.Client.export_notebook`

    Examples:
        To return the list of containers::

            from dd_scenario import Client

            client = Client()
            # get list of available containers
            containers = client.get_containers()

        In the following example, the client session is closed when it's no
        longer needed::

            with Client() as client:
                for container in client.get_containers():
                    # delete all container containing 'foo'
                    if 'foo' in container['description']:
                        client.delete(container)

    '''

    def __init__(self,
                 api_url=None,
                 authorization=None,
                 project_id=None,
                 max_retries=3,
                 proxies=None,
                 cognitive_url=None,
                 pc=None,
                 apikey=None,
                 verify=None):
        '''Creates a new Decision Optimization scenario client.

        Args:
            authorization: The authorization key.
            api_url (:obj:`str`, optional): The scenario API url entry point.
                If not specified, the client will use default value:
                http://dd-scenario-api-svc:8450/dd-scenario-api/v2
            max_retries (:obj:`int`, optional): maximum number of retries.
                Default is 3.
            proxies (:obj:`dict`, optional): Optional dictionary mapping
                protocol to the URL of the proxy.
            pc: Optional project context
            apikey: IAM api key
            verify: override http's verify property
        '''
        default_api_url = None
        if pc:
            # a project context is passed, so we can assume project_lib is installed
            from project_lib.utils import environment as pcl_env  # @UnresolvedImport
            default_api_url = '%s/v2' % pcl_env.get_common_api_url()
        if apikey:
            # apikey is an IAM apikey, request for a token
            auth_handler = IAMAuthHandler(apikey)
            authorization = auth_handler.get_authorization()
            default_api_url = auth_handler.get_api_url()
        # at this point, if api_url has not been guessed, use a default
        # value suitable for use with DSX
        if default_api_url is None:
            default_api_url = 'http://dd-scenario-api-svc:8450/dd-scenario-api/v2'
        self.api_url = api_url if api_url is not None else default_api_url
        self.cognitive_url = cognitive_url if cognitive_url is not None else \
            'http://dd-cognitive-svc:80/v1/cognitive'
        # Create session
        self.session = requests.Session()
        # mount custom adapters for http and https for this session
        hta = requests.adapters.HTTPAdapter
        self.session.mount('http://', hta(max_retries=max_retries))
        self.session.mount('https://', hta(max_retries=max_retries))
        # get info from project context if available
        if pc and authorization is None:
            authorization = pc.accessToken
        if pc and project_id is None:
            project_id = pc.projectID
        # Relay authorization token
        token = ""
        if authorization:
            token = authorization
        else:
            token = os.environ.get('DSX_TOKEN')
        bearer = "Bearer"
        if bearer != token[:len(bearer)]:
            token = "%s %s" % (bearer, token)
        self.session.headers.update({'Authorization': token})
        if verify is not None:
            self.session.verify = verify
        self.project_id = project_id
        if (self.project_id is None):
            self.project_id = os.environ.get('DSX_PROJECT_NAME')
        # proxies
        if proxies is not None:
            self.session.proxies.update(proxies)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # Closes this client and frees up used resources.
        self.session.close()

    def _check_status(self, response, ok_status):
        ''' Checks that the request is performed correctly. '''
        if not (response.status_code in ok_status):
            # if the error already has a corresponding exception in the HTTP
            # lib, just raise it
            raise_this = None
            try:
                j = response.json()
                if 'errors' in j:
                    raise DDException(j)
            except DDException:
                raise
            except ValueError: # no json
                pass
            response.raise_for_status()
            raise RuntimeError("%s: %s" % (response.status_code,
                                           response.reason))

    def get_containers(self, parent_id, category=None):
        '''Returns the list of containers.

        Container type include:

            * ``scenario``
            * ``inputset``
            * ``model``

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/``

        Args:
            parent_id: The parent_id
            category: The container category.
        Returns:
            a list of :class:`~dd_scenario.Container`
        '''
        type_sel = "&category=%s" % category if category else ""
        url = '{api_url}/containers?projectId={pid}&parentId={parent}{type_sel}'.format(
            api_url=self.api_url,
            pid=self.project_id,
            parent=parent_id,
            type_sel=type_sel)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        containers_as_json = response.json()
        return [Container(parent_id=parent_id, json=s, client=self) for s in containers_as_json]

    def create_container(self, parent_id, container):
        '''Creates a container.

        This is a direct mapping to REST API:

            ``PUT /dd-scenario-api/v2/containers/``

        Args:
            container (:class:`~dd_scenario.Container`): The container metadata
        Returns:
            The container.
        '''
        if getattr(container, 'projectId') == None:
            container.projectId = self.project_id
        url = '{api_url}/containers/{container_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_name=container.name,
            pid=self.project_id,
            parent=parent_id)
        response = self.session.put(url, headers=content_json,
                                     data=container.to_json())
        self._check_status(response, [200, 201])
        container_as_json = response.json()
        return Container(parent_id=parent_id, json=container_as_json, client=self)

    def get_container(self, parent_id, id):
        ''' Returns the container metadata.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{container_name}``

        Args:
            id: A :class:`~dd_scenario.Container` or a container name
               as string
        Returns:
            a list of :class:`~dd_scenario.Container`
        '''
        sid = get_container_name(id)
        url = '{api_url}/containers/{container_id}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=sid,
            pid=self.project_id,
            parent=parent_id)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        container_as_json = response.json()
        return Container(parent_id=parent_id, json=container_as_json, client=self)

    def update_container(self, container, new_data):
        ''' Updates container metadata.

        This is a direct mapping to REST API:

            ``PUT /dd-scenario-api/v2/containers/{container_name}``

        Examples:

            Updates a container with new data using the container name:

            >>> new = Container()
            >>> new.description = "new description"
            >>> client.update_container(container_name}, new)

            Get a container's metadata, then replace description:

            >>> container = client.get_container(container_name)
            >>> container.description = "new description"
            >>> client.update_container(container)

        Args:
            container: A :class:`~dd_scenario.Container`. This ``container`` is used to indicate which container
               is to be updated. If ``new_data`` is None, the container is
               updated with the data from this ``container``.
            new_data (:class:`~dd_scenario.Container`, optional): A
               :class:`~dd_scenario.Container` containing metadata to update.
        '''
        sid = get_container_name(container)
        url = '{api_url}/containers/{container_id}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=sid,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_json,
                                    data=new_data.to_json(),allow_redirects=False)
        self._check_status(response, [200, 301])

    def delete_container(self, container):
        ''' Deletes the container.

        This is a direct mapping to REST API:

            ``DELETE /dd-scenario-api/v2/containers/{container_name}``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string
        '''
        sid = get_container_name(container)
        url = '{api_url}/containers/{container_id}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=sid,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.delete(url, headers=content_json)
        self._check_status(response, [204])

    def copy_container(self, container, metadata=None):
        '''Copies a container.

        This is a direct mapping to REST API:

            ``POST /dd-scenario-api/v2/containers/{container_name}/copy``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This is the source container.
            metadata (:class:`~dd_scenario.Container`, optional): new metadata
                to override, as a ``Container``.
        Returns:
            The created container
        '''
        sid = get_container_name(container)
        url = '{api_url}/containers/{container_id}/copy?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=sid,
            pid=self.project_id,
            parent=container.parent_id)
        container_data = metadata
        if isinstance(container, Container) and metadata is None:
            container_data = container
        response = self.session.post(url, headers=content_json,
                                     data=container_data.to_json() if container_data else None)
        self._check_status(response, [201])
        container_as_json = response.json()
        return Container(container.parent_id, json=container_as_json, client=self)

    def get_assets(self, container, name=None):
        '''Returns assets for a container.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{container_name}/assets``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
        Returns:
            A dict where keys are asset name and values are
            :class:`~dd_scenario.Asset`.
        '''
        qparams = {}
        if name is not None:
            qparams['name'] = name
        query_str = '&%s' % urlencode(qparams) if qparams else ""
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/assets?projectId={pid}&parentId={parent}{qstr}'.format(
            api_url=self.api_url,
            container_id=container_id,
            pid=self.project_id,
            parent=container.parent_id,
            qstr=query_str)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        assets_as_json = response.json()
        return {asset_json["name"]: Asset(asset_json)
                for asset_json in assets_as_json}

    def update_asset(self, container, name, new_data=None):
        ''' Updates asset metadata.

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This ``container`` is used to indicate which container
               is to be updated.
            name: An asset name.
            new_data (:class:`~dd_scenario.Asset`): A
               :class:`~dd_scenario.Asset` containing metadata to update.
        ''' 
        container_id = get_container_name(container)
        if new_data is None:
            raise ValueError("No asset data provided")
        url = '{api_url}/containers/{container_id}/assets/{asset_id}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            asset_id=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.post(url, headers=content_json,
                                    data=json.dumps(new_data),allow_redirects=False)
        self._check_status(response, [200, 301])

    def create_asset(self, container, asset_meta=None):
        ''' Creates a new asset with given meta data.
        '''
        container_name = get_container_name(container)
        asset_name = get_asset_name(asset_meta)
        url = '{api_url}/containers/{container_name}/assets/{asset_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_name=container_name,
            asset_name=asset_name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_json,
                                     data=asset_meta.to_json())
        self._check_status(response, [201])
        asset_as_json = response.json()
        return Asset(json=asset_as_json, container=container)

    def get_asset(self, container, name):
        ''' Gets asset metadata.

        This can get the asset by id or by name.

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: An asset name
        Returns:
            A :class:`~dd_scenario.Asset` instance.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_name = get_container_name(container)
        if name is None:
            return None
        if not isinstance(name, string_types): 
            raise ValueError("name shoudl be a string type")
        url = '{api_url}/containers/{container_name}/assets/{asset_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_name=container_name,
            asset_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=content_json)  
        self._check_status(response, [200,404])
        if response.status_code == 404:
            return None
        asset_as_json = response.json()
        return Asset(json=asset_as_json, client=self)

    def get_asset_data(self, container, name):
        ''' Gets asset data.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{container_name}/assets/{assetName}/data``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: An asset name.
        Returns:
            The asset data as a byte array.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/assets/{asset_id}/data?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            asset_id=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=content_octet_stream)
        self._check_status(response, [200, 204])
        if response.status_code == 204:
            return None
        return response.content

    def get_asset_name(self, asset=None, name=None):
        # returns the id for an asset or asset name
        asset_name = None
        if name:
            asset_name = name
        if asset_name is None:
            asset_name = get_asset_name(asset)
        return asset_name

    def get_table_name(self, table=None, name=None):
        # returns the id for a table or table name
        table_name = None
        if name:
            table_name = name
        if not table_name:
            table_name = get_table_name(table)
        return table_name

    def add_asset_data(self, container, name, data=None):
        ''' Adds or updates asset data.

        This is a direct mapping to REST API:

            ``PUT /dd-scenario-api/v2/containers/{containerName}/tables/{tableName}``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This ``container`` is used to indicate which container
               is to be updated.
            name: An asset name.
            data: A stream containing the data to upload.
        Returns:
            the asset metadata as :class:`~dd_scenario.Asset`
        '''
        container_id = get_container_name(container)
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        if data is None:
            raise ValueError("No data provided")
        url = '{api_url}/containers/{sid}/assets/{asset_id}/data?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            sid=container_id,
            asset_id=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_octet_stream,
                                    data=data)
        self._check_status(response, [200])

        return Asset(json=response.json(), client=self)

    def delete_asset(self, container, name):
        ''' Deletes the asset.

        This can delete the asset by id if ``asset`` is specified or by name
        if ``name`` is specified.

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string
            name: An asset name.
        '''
        container_name = get_container_name(container)
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        url = '{api_url}/containers/{container_name}/assets/{asset_id}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_name=container_name,
            asset_id=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.delete(url, headers=content_json)
        self._check_status(response, [204])

    def get_tables(self, container, category=None, name=None):
        '''Returns all container table metadata.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{container_name}/tables``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: A name to filter tables with.
            category: The category of tables. Can be 'input', 'output' or None
                if both input and output tables are to be returned.
        Returns:
            A dict where keys are table name and values are
            :class:`~dd_scenario.Table`.
        '''
        qparams = {}
        if category is not None:
            qparams['category'] = category
        if name is not None:
            qparams['name'] = name
        query_str = '&%s' % urlencode(qparams) if qparams else ""
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/tables?projectId={pid}&parentId={parent}{qstr}'.format(
            api_url=self.api_url,
            container_id=container_id,
            pid=self.project_id,
            parent=container.parent_id,
            qstr=query_str)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        tables_as_json = response.json()
        return {table_json["name"]: Table(json=table_json, container=container)
                for table_json in tables_as_json}

    def create_table(self, container, table_meta=None):
        ''' Creates a new table with given meta data.
        '''
        container_id = get_container_name(container)
        table_name = get_table_name(table_meta)
        url = '{api_url}/containers/{container_id}/tables/{table_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            table_name=table_name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_json,
                                     data=table_meta.to_json())
        self._check_status(response, [200, 201])
        table_as_json = response.json()
        return Table(json=table_as_json, container=container)

    def add_table(self, container, name, new_data=None, category=None):
        '''Adds table metadata.

        This can add metadata by table id or table name.

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This ``container`` is used to indicate which container
               is to be updated.
            name: A table name.
            new_data (:class:`~dd_scenario.Table`): A
               :class:`~dd_container.Table` containing metadata to update.
        '''
        container_id = get_container_name(container)
        table_data = new_data
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        if table_data is None:
            raise ValueError("No table data provided")
        if category is not None:
            table_data.category = category
        url = '{api_url}/containers/{container_id}/tables/{table_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_json,
                                    data=table_data.to_json())
        self._check_status(response, [200])

    def get_table(self, container, name):
        ''' Gets table metadata.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{containerName}/tables/{tableName}``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: A table name.
        Returns:
            A :class:`~dd_scenario.Table` instance.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_name = get_container_name(container)
        url = '{api_url}/containers/{container_name}/tables/{table_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_name=container_name,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200,404])
        if response.status_code == 404:
            return None
        table_as_json = response.json()
        return Table(json=table_as_json, container=container)

    def delete_table(self, container, name):
        ''' Deletes the table.


        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string
            name: A table name.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/tables/{table_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.delete(url, headers=content_json)
        self._check_status(response, [204])

    def get_table_type(self, container, name):
        '''Gets table type.

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: the name of the table
        Returns:
            A :class:`~dd_scenario.TableType` instance.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_id = get_container_name(container)
        url = '{api_url}/containers/{sid}/tables/{table_name}/type?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            sid=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        type_as_json = response.json()
        return TableType(json=type_as_json, id=name)

    def update_table_type(self, container, name, new_value=None):
        ''' Updates table type.

        This is a direct mapping to REST API:

            ``PUT /dd-scenario-api/v2/containers/{container_name}/tables/{tableName}/type``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This ``container`` is used to indicate which container
               is to be updated.
            name: the name of the table.
            new_value (:class:`~dd_container.TableType`): A
               :class:`~dd_container.TableType` containing metadata to update.
        '''
        container_id = get_container_name(container)
        if new_value is None:
            raise ValueError("No container table type provided")
        url = '{api_url}/containers/{sid}/tables/{table_name}/type?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            sid=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.put(url, headers=content_json,
                                    data=json.dumps(new_value.to_json()))
        self._check_status(response, [200])

    def get_tables_type(self, container):
        '''Returns a dictionary of table types for each table.

        This is a direct mapping to REST API:

            ``GET /dd-scenario-api/v2/containers/{container_name}/tables/types``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
        Returns:
            A dict which keys are table names and values are
            :class:`~dd_scenario.TableType`'s.
        '''
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/tables/types?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        types_as_json = response.json()
        return {name: TableType(json=type_json, name=name)
                for name, type_json in iteritems(types_as_json)}

    def get_table_data(self, container, name, raw=False):
        ''' Gets table data.

        Examples:

            Returns the specified table data as a dataframe::

                with Client(project_context) as client:
                    df = client.get_table_data(container, name)
        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string.
            name: the name of the table.
            raw: If set, data is returned as is from the server, without
               conversion into a `pandas.DataFrame`
        Returns:
            A :py:obj:`pandas.DataFrame` containing the data or the raw data.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_id = get_container_name(container)
        url = '{api_url}/containers/{sid}/tables/{table_name}/data?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            sid=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.get(url, headers=accept_csv)
        self._check_status(response, [200, 204])
        if response.status_code == 200:
            if pd and not raw:
                data = BytesIO(response.content)
                return pd.read_csv(data, index_col=None)
            else:
                return response.content
        else:
            return None

    def add_table_data(self, container, name, category=None, data=None):
        ''' Adds table metadata.

        This is a direct mapping to REST API:

            ``PUT /dd-scenario-api/v2/containers/{container_name}/tables/{tableName}``

        Example:

            The following code uploads a pandas.DataFrame into a container::

                with Client() as client:
                    client.add_table_data(container_id, table_name, df,
                                          category='input')

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string. This ``container`` is used to indicate which container
               is to be updated.
            name: the name of the table.
            category (optional): The category of the table ('input' or 'output')
            data (:obj:`pandas.DataFrame` or bytes): The data to upload. If
                the data is a `pandas.DataFrame`, it is converted to csv first.
        '''
        container_id = get_container_name(container)
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        if data is None:
            raise ValueError("No data provided")
        if pd and isinstance(data, pd.DataFrame):
            data = data.to_csv(index=False)
        qparams = []
        if category is not None:
            qparams.append("category=%s" % category)
        query_str = '&%s' % '&'.join(qparams) if qparams else ""
        url = '{api_url}/containers/{sid}/tables/{table_name}/data?projectId={pid}&parentId={parent}{query_str}'.format(
            api_url=self.api_url,
            sid=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id,
            query_str=query_str)
        response = self.session.put(url, headers=content_csv,
                                    data=data)
        self._check_status(response, [200])

    def delete_table_data(self, container, name):
        ''' Deletes table data.

        This is a direct mapping to REST API:

            ``DELETE /dd-scenario-api/v2/containers/{container_name}/tables/{tableName}/data``

        Args:
            container: A :class:`~dd_scenario.Container` or a container name
               as string
            name: the name of the table.
        '''
        if not isinstance(name, string_types): 
            raise ValueError("name should be a string type")
        container_id = get_container_name(container)
        url = '{api_url}/containers/{container_id}/table/{table_name}?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            container_id=container_id,
            table_name=name,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.delete(url, headers=content_json)
        self._check_status(response, [204])

    def get_model_builders(self, name=None):
        '''Returns the list of decision model builders.

        This is a direct mapping to REST API:

            ``GET /v2/decisions/``

        Args:
            name: An optional parameter. If given, only the model builders for which
                names match ``name`` are returned.
        Returns:
            a list of :class:`~dd_scenario.ModelBuilder`
        '''
        url = '{api_url}/decisions?projectId={pid}'.format(
            api_url=self.api_url,
            pid=self.project_id)
        response = self.session.get(url, headers=content_json)
        self._check_status(response, [200])
        model_builders_as_json = response.json()
        model_builders = [ModelBuilder(json=s, client=self) for s in model_builders_as_json]
        if name:
            return [x for x in model_builders if x.name == name]
        else:
            return model_builders

    def create_model_builder(self, model_builder=None, **kwargs):
        '''Creates a decision model_builder.

        This is a direct mapping to REST API:

            ``PUT /v2/decisions/``

        If this method is given an ``model_builder`` argument, that model_builder is
        used to initialize the values for the new model_builder. Otherwise, the
        ``**kwargs`` are used to initialize a
        :class:`~dd_scenario.ModelBuilder`.

        Example:

            Creates a model builder using the model builder name passed as ``kwargs``::

                model_builder = client.create_model_builder(name='test model_builder')

            Creates a model builder using the model_builder passed as a ModelBuilder:

                meta = ModelBuilder(name='test model_builder')
                model_builder = client.create_model_builder(model_builder=meta)

        Args:
            model_builder (:class:`~dd_scenario.ModelBuilder`): The
                model builder metadata used as initial data.
            **kwargs: kwargs used to initialize the ModelBuilder
        Returns:
            The decision model builder as a :class:`~dd_scenario.ModelBuilder`
        '''
        model_builder_value = ModelBuilder()
        if model_builder:
            model_builder_value.json.update(model_builder.json)
        if kwargs:
            model_builder_value.json.update(kwargs)
        url = '{api_url}/decisions/{decision_name}?projectId={pid}'.format(
            api_url=self.api_url,
            decision_name=get_model_builder_id(model_builder_value),
            pid=self.project_id)
        response = self.session.put(url, headers=content_json,
                                     data=model_builder_value.to_json())
        self._check_status(response, [201])
        json_resp = response.json()
        return ModelBuilder(json=json_resp, client=self)

    def get_model_builder(self, name=None, id=None):
        ''' Returns the decision model builder metadata.

        This is a direct mapping to REST API:

            ``GET /v2/decisions/{model_builder_name}``

        where ``{model_builder_name}`` is the model builder name. 

        Args:
            id (optional): name of the decision model to look for.
            name (optional): The name of the model builder to look for
        Returns:
            a list of :class:`~dd_scenario.ModelBuilder`
        '''
        # search by model builder name
        if id is not None:
            guid = get_model_builder_id(id)
            url = '{api_url}/decisions/{guid}?projectId={pid}'.format(
                api_url=self.api_url,
                guid=guid,
                pid=self.project_id)
            response = self.session.get(url, headers=content_json)
            self._check_status(response, [200])
            framework_as_json = response.json()
            return ModelBuilder(json=framework_as_json, client=self)
        elif name is not None:
            possible = self.get_model_builders(name=name)
            return possible[0] if possible else None
        else:
            raise ValueError("get_model_builder expects an id or name to filter decision models.")

    def update_model_builder(self, model_builder, new_data=None):
        ''' Updates decision model metadata.

        This is a direct mapping to REST API:

            ``PUT /v2/decisions/{model_builder_name}``

        where ``{model_builder_name}`` is the model builder name. 

        Examples:

            Updates a model builder with new data using name::

            >>> new = ModelBuilder()
            >>> new.description = "new description"
            >>> client.update_model_builder(decision_model_name, new)

            Gets a model builder, then replaces description::

            >>> model_builder = client.get_model_builder(id=guid)
            >>> model_builder.description = "new description"
            >>> client.update_model_builder(model_builder)

            Gets a model builder by name, then replaces description::

            >>> model_builder = client.get_model_builder(name='decision model name')
            >>> model_builder.description = "new description"
            >>> client.update_model_builder(model_builder)

        Args:
            model_builder: A :class:`~dd_scenario.ModelBuilder` or a name
               as string. This ``model_builder`` is used to indicate which
               model builder is to be updated. If ``new_data`` is None, the
               model builder is updated with the data from this ``model_builder``.
            new_data (:class:`~dd_scenario.ModelBuilder`, optional): A
               :class:`~dd_scenario.ModelBuilder` containing metadata to
               update.
        '''
        guid = get_model_builder_id(model_builder)
        model_builder_data = new_data
        if isinstance(model_builder, ModelBuilder) and new_data is None:
            model_builder_data = model_builder
        if model_builder_data is None:
            raise ValueError("No model_builder data provided")
        url = '{api_url}/decisions/{guid}?projectId={pid}'.format(
            api_url=self.api_url,
            guid=guid,
            pid=self.project_id)
        response = self.session.put(url, headers=content_json,
                                    data=json.dumps(model_builder_data))
        self._check_status(response, [200])

    def delete_model_builder(self, model_builder):
        ''' Deletes the decision model.

        This is a direct mapping to REST API:

            ``DELETE /v2/decisions/{model_builder_name}``

        Args:
            model_builder: A :class:`~dd_scenario.ModelBuilder` or a name
               as string
        '''
        guid = get_model_builder_id(model_builder)
        url = '{api_url}/decisions/{guid}?projectId={pid}'.format(
            api_url=self.api_url,
            guid=guid,
            pid=self.project_id)
        response = self.session.delete(url, headers=content_json)
        self._check_status(response, [204])

    def is_cognitive_scenario(self, container):
        # get container info
        container_id = get_container_name(container)
        qualifiers = None
        try:
            qualifiers = container.qualifiers
        except AttributeError:
            cc = self.get_container(container.parent_id, container_id)
            qualifiers = cc.qualifiers
        # check if this is a cognitive model
        if qualifiers is None:
            return False
        qual_dict = {q['name']: q['value'] for q in qualifiers}
        return (qual_dict.get('modelType') == 'cognitive')

    def solve(self,
              container,
              **kwargs):
        '''Solves the scenario model of the container which id is specified.

        This method returns as soon as the request is sent. Use
        Client.wait_for_completion() to wait for solve completion.

        Args:
            container: The Container or container id to solve()
            **kwargs: extra arguments passed to the solve using a SolveConfig
        '''
        container_id = get_container_name(container)
        endpoint = None
        if self.is_cognitive_scenario(container):
            endpoint = '{api_url}/solve?projectId={pid}&parentId={parent}'.format(
                api_url=self.cognitive_url,
                pid=self.project_id,
                parent=container.parent_id)
        else:
            endpoint = '{api_url}/decisions/solve?projectId={pid}&parentId={parent}'.format(
                api_url=self.api_url,
                pid=self.project_id,
                parent=container.parent_id)
        # create SolveConfig
        sc = SolveConfig(containerId=container_id, **kwargs)
        # run the solve
        response = self.session.post(endpoint, headers=content_json,
                                     data=sc.to_json())
        self._check_status(response, [202])

    def stop_solve(self, container):
        '''Stops the solve for a scenario.
        '''
        container_id = get_container_name(container)
        endpoint = None
        if self.is_cognitive_scenario(container):
            endpoint = '{api_url}/solve/status/{guid}?projectId={pid}&parentId={parent}'.format(
                api_url=self.cognitive_url,
                guid=container_id,
                pid=self.project_id,
                parent=container.parent_id)
        else:
            endpoint = '{api_url}/decisions/solve/status/{guid}?projectId={pid}&parentId={parent}'.format(
                api_url=self.api_url,
                guid=container_id,
                pid=self.project_id,
                parent=container.parent_id)
        response = self.session.delete(endpoint, headers=content_json)
        self._check_status(response, [202])

    def wait_for_completion(self, container):
        '''Waits for the solve operation specified container to complete.

        Returns:
            The last :class:`~dd_scenario.SolveStatus`
        '''
        s = self.get_solve_status(container)
        while s.state not in {'FAILED', 'TERMINATED'}:
            time.sleep(1)
            s = self.get_solve_status(container)
        return s

    def get_solve_status(self, container):
        '''Queries and returns the solve status for the specified container.

        Returns:
            A :class:`~dd_scenario.SolveStatus`
        '''
        container_id = get_container_name(container)
        endpoint = None
        if self.is_cognitive_scenario(container):
            endpoint = '{api_url}/solve/status/{guid}?projectId={pid}&parentId={parent}'.format(
                api_url=self.cognitive_url, 
                guid=container_id,
                pid=self.project_id,
                parent=container.parent_id)
        else:
            endpoint = '{api_url}/decisions/solve/status/{guid}?projectId={pid}&parentId={parent}'.format(
                api_url=self.api_url,
                guid=container_id,
                pid=self.project_id,
                parent=container.parent_id)
        response = self.session.get(endpoint, headers=content_json)
        return SolveStatus(json=response.json())

    def export_notebook(self, container, name, description=None):
        '''Creates a notebook from a container's model.

        Args:
            container: The container or container_id
            name: the name of the notebook
            descrition (Optional): The notebook description
        Returns:
            A dict with the notebook creation info::

            {
               'projectNotebookId': 'aeiou',
               'notebookId': 'aeiou',
               'notebookUrl': 'aeiou'
            }
        '''
        payload = {'containerId': get_container_name(container),
                   'notebookName': name}
        if description:
            payload['notebookDescription'] = description
        url = '{api_url}/decisions/export/notebook?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.post(url, headers=content_json,
                                     data=json.dumps(payload))
        self._check_status(response, [200])
        return response.json()

    def import_notebook(self, container, notebook_id):
        '''Updates container model from notebook.

        Args:
            container: The container or container_id
            name: the name of the notebook
            descrition (Optional): The notebook description
        '''
        payload = {'containerId': get_container_name(container),
                   'notebookId': notebook_id}
        url = '{api_url}/decisions/import/notebook?projectId={pid}&parentId={parent}'.format(
            api_url=self.api_url,
            pid=self.project_id,
            parent=container.parent_id)
        response = self.session.post(url, headers=content_json,
                                     data=json.dumps(payload))
        self._check_status(response, [200])
        print(response.content)

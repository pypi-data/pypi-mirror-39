# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

import json
try:
    from StringIO import StringIO as BytesIO
except ImportError:  # py3
    from io import BytesIO
from collections import deque
import sys

from six import string_types, iteritems

from .base_resource import DDObject
from .table import Table
from .asset import Asset


def get_container_name(what):
    if hasattr(what, "name"):
        return what.name
    elif isinstance(what, string_types):
        return what
    else:
        raise ValueError("Don't know how to get container id from %s" % what)


class Container(DDObject):
    '''The container class.
    '''
    def __init__(self, parent_id=None, json=None, pc=None, **kwargs):
        '''Creates a new container.

        Examples:

            Creates a list of :class:`~Container` from containers metadata of a
            project, for instance, the response.json() from
            :class:`~dd_scenario.Client.get_containers()`:

                >>> containers = [Container(json=s) for s in client.get_containers()]

            Creates a container with a given name and projectId:

                >>> container = Container(name="foo", projectId="aeiou")

            Creates a container with a given name and using the project context:

                >>> container = Container(name="foo", pc=pc)

        Args:
           json (:obj:`dict`, optional): The dict describing the container.
           pc (:obj:`projectContext`, optional): The project context
           **kwargs (optional): kwargs to override container attributes.
               Attributes specified here will override those of ``desc``.
        '''
        super(Container, self).__init__(json=json, **kwargs)
        # update project id with pc if pc is passed
        if pc and hasattr(pc, 'projectId'):
            self.json.update({'projectId': pc.projectId})
        self.parent_id = parent_id

    def __repr__(self):
        return json.dumps(self.json, indent=3)

    def add_table_data(self, what, data=None, category=None):
        '''Adds the table data to the container.

        Data must be ``pandas.DataFrame``.

        Examples:

            Adds the data for the table with the specified name::

                >>> container.add_table_data("table1", data=table1_data)

            Adds the data for the tables in the dict:

                >>> tables = { "table1": table1_df, "table2": table2_df }
                >>> scenario.add_table_data(tables)

        Args:
            what: what to add. Can be either a table name or a dict of
                ``{table_name: table_data}``
            data: The data if ``what`` is a table name.
        '''
        if isinstance(what, string_types) or isinstance(what, Table):
            # check table existance
            if isinstance(what, string_types):
                tables = self.client.get_tables(self)
                table = tables.get(what, None)
                if not table:
                    table_meta = Table(name=what, category=category,
                                       lineage='python client')
                    table = self.client.create_table(self, table_meta)
                what = table
            self.client.add_table_data(self, what.name, data=data, category=category)
        else:
            for (name, value) in iteritems(what):
                self.add_table_data(name, data=value,
                                    category=category)

    def get_table_data(self, table):
        '''Calls ``self.client.get_table_data(self, table)``

        See :meth:`dd_scenario.Client.get_table_data`.
        '''
        try:
            table_name = table.name
        except AttributeError:
            table_name = table
        return self.client.get_table_data(self, name=table_name)

    def delete_table_data(self, table):
        '''Calls ``self.client.delete_table_data(self, table)``

        See :meth:`dd_sccontainerlient.delete_table_data`.
        '''
        return self.client.delete_table_data(self, table)

    def get_table_type(self, name):
        '''Returns a :class:`~dd_scenario.TableType`` descriptor for the
        ``table`` which name is specified.

        See :meth:`dd_scenario.Client.get_table_type`.

        Args:
            name: A table name as a string.
        Returns:
            A :class:`~dd_scenario.TableType` instance.
        '''
        return self.client.get_table_type(self, name=name)

    def update_table_type(self, table_type):
        '''Updates the table type for the specified table type.

        Calls ``self.client.update_table_type(self, table_type.id,
        new_value=table_type)``

        See :meth:`dd_scenario.Client.update_table_type`.

        Args:
            table_type: A TableType for the update.
        '''
        return self.client.update_table_type(self, table_type.id,
                                             new_value=table_type)

    def get_tables_data(self, category=None):
        '''Returns a dict of all tables. Keys are table names, values are
        DataFrames with table data.
        '''
        t = self.client.get_tables(self, category=category)
        return {n: self.client.get_table_data(self, v.name) for n, v in iteritems(t)}

    def get_tables(self, category=None):
        '''Returns all container table metadata.

        Args:
            category: The category of tables. Can be 'input', 'output' or None
                if both input and output tables are to be returned.
        Returns:
            A dict where its keys are asset names and its values are
            :class:`~dd_scenario.Table`.
        '''
        return self.client.get_tables(self, category=category)

    def add_asset_data(self, name, data=None):
        ''' Adds or updates asset data.

        Args:
            name: The name of the asset
            data: A stream containing the data to upload.
        Returns:
            the asset metadata as :class:`~dd_scenario.Asset`
        '''
        asset = self.client.get_asset(self, name=name)
        if not asset:
            asset_meta = Asset(name=name, category='model')
            asset = self.client.create_asset(self, asset_meta)
        return self.client.add_asset_data(self, name=name, data=data)

    def get_asset_data(self, name):
        ''' Gets asset data.

        Args:
            name: The name of the asset.
        Returns:
            The asset data as a byte array.
        '''
        return self.client.get_asset_data(self, name=name)

    def get_asset(self, name):
        '''Gets asset metadata using name.

        Args:

            asset: An asset or asset name as a string.
            name: An asset name.
        Returns:
            A :class:`~dd_scenario.Asset` instance.
        '''
        return self.client.get_asset(self, name=name)

    def delete_asset(self, name):
        ''' Deletes the asset.

        Args:
            name: The name of the asset as a string.
        '''
        return self.client.delete_asset(self, name)

    def create_asset(self, name, data=None, category='model'):
        ''' Creates an asset.
        '''
        asset = Asset(name=name, category=category)
        return self.client.create_asset(self, asset)

    def get_assets(self):
        '''Returns asset metadata for all of this container's assets.

        Returns:
            A dict where its keys are asset names and its values are
            :class:`~dd_scenario.Asset`'s metadata.
        '''
        return self.client.get_assets(self)

    def solve(self, display_log=None, log_lines=25, log_output=None, **kwargs):
        '''Solves this scenario.

        If an error occurs and ``display_log`` is None or not set, this prints
        the last ``log_lines`` lines of log (default: 25)

        If ``display_log`` is set to False, nothing is displayed.

        If display_log is set to True, the log are always displayed.

        Args:
            **kwargs: extra arguments passed as SolveConfig attributes
            display_log: If True, log is downloaded after solve and displayed.
                Default is False
            log_lines: number of lines of log to print. Default is 25. If None,
                all log lines are displayed.
            log_output: the file like object to write logs to. If not specified
                or None, defaults to sys.stdout.
        '''
        args = {}
        if kwargs:
            args.update(kwargs)
        # True unless we specifically do not want logs
        if display_log != False:
            args['collectEngineLog'] = True
        self.client.solve(self, **args)
        status = self.client.wait_for_completion(self)
        # job state
        state = status['state']
        # get job details
        execution_status = None
        job_details = status['jobDetails']
        if job_details is not None:
            # execution status:
            execution_status = job_details.get('executionStatus')
            if execution_status is None:
                print('Could not find jobDetails/executionStatus in status')
                print('Status = %s' % json.dumps(status.json, indent=3))
                raise KeyError('Could not find executionStatus in status')
        # is this failed ?
        is_failed = (execution_status == 'FAILED' or state == 'FAILED')
        # if display_log == False => do exactly nothing
        if display_log or (display_log is None and is_failed):
            if log_output is None:
                log_output = sys.stdout
            assets = self.get_assets()
            if 'log.txt' in assets:
                logs = self.get_asset_data('log.txt')
                strio = BytesIO(logs)
                last_n_lines = deque(strio.readlines(), maxlen=log_lines)
                for l in last_n_lines:
                    log_output.write(l)
        return status

    def copy(self, name):
        '''Copies this container.

        Arg:
            name (Mandatory): The name of the copy.

        Returns:
            The :class:`~Container` for the copy.
        '''
        metadata = Container(name=name)
        return self.client.copy_container(self, metadata=metadata)

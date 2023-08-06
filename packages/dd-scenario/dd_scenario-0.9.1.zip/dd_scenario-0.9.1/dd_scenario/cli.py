# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2017, 2018
# --------------------------------------------------------------------------

#
# Command line module
#
import argparse
import json
import os
import requests
from requests.exceptions import TooManyRedirects
import shutil
import sys
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse  # python3

import zipfile
from io import BytesIO

from six import iteritems

from dd_scenario import Client, Container, DDException, Table

import pandas

# for dev portals, we otherwise get a lot of warnings
try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # @UndefinedVariable
finally:
    pass

# This will be the ipython context if any
ip = None
try:
    from IPython.core.magic import (Magics, magics_class, line_magic,
                                    cell_magic, line_cell_magic)
    from IPython.core.display import display
    from IPython.display import HTML

    import shlex
    import base64

    def create_download_link(data, title = "Download ZIP file", filename = "output.zip"):
        b64 = base64.b64encode(data)
        payload = b64.decode()
        html = '<a download="{filename}" href="data:application/zip;base64,{payload}" target="_blank">{title}</a>'
        html = html.format(payload=payload, title=title, filename=filename)
        return HTML(html)

    @magics_class
    class DDScenarioCliMagics(Magics):
        def __init__(self, shell):
            super(DDScenarioCliMagics, self).__init__(shell)

        @line_magic
        def dd_cli(self, line):
            "The docplex CLI magics"
            args = shlex.split(line)
            try:
                output_handler = ZipOutput()
                if '--api' in args:
                    api_url = None  # do not override from here
                else:
                    # use internal
                    api_url = 'http://dd-scenario-api-svc:8450/dd-scenario-api/v2'
                status = run_command('dd_cli',
                                     args,
                                     output_handler=output_handler,
                                     api_url=api_url)
                if status == 0:
                    display(create_download_link(output_handler.buffer.getvalue()))
            except SystemExit:
                pass

    # register the magics
    try:
        ip = get_ipython()  # @UndefinedVariable
        ip.register_magics(DDScenarioCliMagics)
    except NameError:
        # get_ipython not found -> we are not in a notebook
        pass
except ImportError:
    # ipython is not available
    pass



try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib


def get_user_token_from_cookie_txt(cookie_file):
    user_token = None
    print(cookie_file)
    if os.path.isfile(cookie_file):
        cj = cookielib.MozillaCookieJar(cookie_file)
        cj.load()
        for cookie in cj:
            if cookie.name == 'ibm-private-cloud-session':
                user_token = cookie.value
                print("using user token = %s value = %s" % (cookie.name,
                                                            cookie.value))
    return user_token


def get_authorization(server, user, password):
    h = {'Content-Type': 'application/x-www-form-urlencoded',
         'Accept': 'application/json'}
    d = 'username=%s&password=%s' % (user, password)
    try:
        url = '{url}/v1/preauth/signin'.format(url=server)
        resp = requests.post(url,
                             data=d,
                             headers=h, verify=False)
        if 'ibm-private-cloud-session' in resp.cookies:
            return resp.cookies['ibm-private-cloud-session']
    except Exception as e:
        print('Cannot POST %s to get authentication token' % url)
        print('Error: %s' % e)
    return None


class ArchiveName(object):
    def __init__(self, arcname):
        '''arcname is expected to look like:

        <framework_name>/<scenario_cat>/<scenario_name>/table/<table category>/<table_name.csv>

        or

        <framework_name>/<scenario_cat>/<scenario_name>/asset/<asset category><asset_name>

        <scenario_cat> = scenario | input_set | model
        <table category> = input | output

        '''
        self.arcname = arcname
        self._is_table = None
        self._is_asset = None
        self.split = arcname.split(os.path.sep)

    @property
    def framework_name(self):
        return self.split[0]

    @property
    def scenario_category(self):
        return self.split[1]

    @property
    def scenario_name(self):
        return self.split[2]

    @property
    def container_metadata_path(self):
        path = '/'.join(self.split[0:3])
        path = '/'.join([path, 'metadata.json'])
        return path

    def is_table(self):
        if self._is_table is None:
            self._is_table = (self.split[3] == 'table')
        return self._is_table

    def is_asset(self):
        if self._is_asset is None:
            self._is_asset = (self.split[3] == 'asset')
        return self._is_asset

    def is_metadata(self):
        return (self.split[-1] == 'metadata.json')

    @property
    def table_category(self):
        if self.is_table():
            return self.split[4]
        else:
            return None

    @property
    def asset_category(self):
        if self.is_asset():
            return self.split[4]
        else:
            return None

    @property
    def data_name(self):
        if self.is_table() or self.is_asset():
            return self.split[5]
        else:
            return None


class DirectoryOutput(object):
    def __init__(self, path):
        self.root = path
        if os.path.isdir(self.root):
            shutil.rmtree(self.root)

    def add(self, path, contents):
        output_path = os.path.join(self.root, path)
        par = os.path.dirname(output_path)
        if not os.path.isdir(par):
            os.makedirs(par)
        with open(output_path, "wb") as o:
            o.write(contents)

    def close(self):
        pass

    def __repr__(self):
        return self.root


class DirectoryInput(object):
    def __init__(self, path):
        self.root = path

    def __repr__(self):
        return self.root

    def get_container_metadata(self, arc_spec):
        path = os.path.join(os.path.dirname(self.root),
                            arc_spec.container_metadata_path)
        if os.path.isfile(path):
            with open(path) as data_file:
                m = json.load(data_file)
                return m

    @property
    def inputs(self):
        common = os.path.dirname(self.root)
        for (dirpath, dirnames, filenames) in os.walk(self.root):
            for dir in dirnames:
                for f in os.listdir(os.path.join(dirpath, dir)):
                    arcname = os.path.join(dirpath, dir, f)
                    if os.path.isfile(arcname):
                        with open(arcname, 'rb') as f:
                            data = bytearray(f.read())
                            yield os.path.relpath(arcname, common), BytesIO(data)


class ZipOutput(object):
    def __init__(self, path=None):
        self.zippath = path
        if path:
            self.zf = zipfile.ZipFile(path, 'w')
        else:
            self.buffer = BytesIO()
            self.zf = zipfile.ZipFile(self.buffer, 'w')

    def add(self, path, contents):
        if contents is None:
            contents = b''
        self.zf.writestr(path, contents)

    def close(self):
        self.zf.close()

    def __repr__(self):
        return self.zippath if self.zippath else 'in memory'


class ZipInput(object):
    def __init__(self, path):
        self.zippath = path
        self.zf = zipfile.ZipFile(self.zippath, 'r')

    def __repr__(self):
        return self.zippath

    @property
    def inputs(self):
        infolist = list(self.zf.infolist())
        for zinfo in infolist:
            # make sure that arcname path separators are os.path.sep
            arcname = zinfo.filename.replace('/', os.path.sep)
            data = BytesIO(self.zf.open(zinfo, 'r').read())
            yield arcname, data

    def get_container_metadata(self, arc_spec):
        zip_spec = arc_spec.container_metadata_path.replace('\\', '/')
        try:
            zinfo = self.zf.getinfo(zip_spec)
        except KeyError:
            zinfo = None
        if zinfo:
            with self.zf.open(zinfo, 'r') as data_file:
                return json.load(data_file)
        return None


def get_project_id(server, authorization, project):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer %s' % authorization}
    project_id = project
    try:
        # is this v3 ?
        r = requests.get('%s/v3/projects?visibility=private' % server,
                         headers=headers,
                         verify=False)
        if r.status_code != 200:
            # this is v2 so query project id
            r = requests.get("%s/v2/projects?name=%s" % (server, project),
                             headers=headers,
                             verify=False)
            if r.status_code == 200:
                result = r.json()
                if result['total_results'] == 1:
                    project_id = result['resources'][0]["metadata"]["guid"]
                elif result['total_results'] > 1:
                    raise RuntimeError('Could not get project id for "%s": multiple projects with the same name' % project)
    except TooManyRedirects as tmr:
        # dsx has the habit of redirecting the request to a login page
        # if no valid Authorization is provided. Just catch that
        # and raise a clearer message
        raise RuntimeError("Could not connect to projects API (too many redirects). Check Authorization")
    except ValueError:
        pass
    return project_id


def get_project(server, authorization, id):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer %s' % authorization}
    try:
        r = requests.get("{server}/v2/projects/{id}".format(server=server,
                                                            id=id),
                         headers=headers,
                         verify=False)
        if r.status_code == 200:
            result = r.json()
            return result
    except TooManyRedirects as tmr:
        # dsx has the habit of redirecting the request to a login page
        # if no valid Authorization is provided. Just catch that
        # and raise a clearer message
        raise RuntimeError("Could not connect to projects API (too many redirects). Check Authorization")
    return None


def create_container(fw, arc_spec, input):
    '''Creates the container if needed.

    Returns:
       The container
    '''
    scn = fw.lookup_container(name=arc_spec.scenario_name)
    if scn is None:
        kwargs = {}
        meta = input.get_container_metadata(arc_spec)
        if meta:
            kwargs.update(meta)
            print('   Creating container %s with metadata %s' %
                  (arc_spec.scenario_name, arc_spec.container_metadata_path))
        else:
            print('   Creating container %s' % arc_spec.scenario_name)
        scn = fw.create_container(category=arc_spec.scenario_category,
                                  name=arc_spec.scenario_name,
                                  **kwargs)
    return scn


def upload_csv(fw, arc_spec, data, input):
    scn = create_container(fw, arc_spec, input)
    # find out data size
    datasize = None  # unknown by default
    try:
        datasize = len(data.getvalue())  # works if data is a BytesIO
    except:
        pass
    if datasize == 0:
        # just create the table
        print('      No table data, creating empty table')
        table_meta = Table(name=arc_spec.data_name,
                           category=arc_spec.table_category,
                           lineage='python client')
        table = scn.client.create_table(scn, table_meta)
    else:
        # when size is unknown, try to write it anyway (let pandas raise an error)
        data_name = arc_spec.data_name
        if data_name.lower().endswith('.csv'):
            data_name = data_name[:-4]
        scn.add_table_data(data_name, data=data,
                           category=arc_spec.table_category)


def upload_asset(fw, arc_spec, data, input):
    scn = create_container(fw, arc_spec, input)
    if scn.get_asset(arc_spec.data_name):
        scn.delete_asset(arc_spec.data_name)
    scn.create_asset(name=arc_spec.data_name,
                     category=arc_spec.asset_category,
                     data=data)
    # create asset with category
    scn.add_asset_data(arc_spec.data_name, data=data)
    if arc_spec.data_name == 'model.py':
        cont_meta = input.get_container_metadata(arc_spec)
        try:
            pymdl = [q for q in (cont_meta['qualifiers'] if cont_meta else [])
                     if q['name'] == 'modelType' and q['value'] == 'python']
            if pymdl:
                print('This is a python model')
                metas = [q['value'] for q in cont_meta['qualifiers']
                         if q['name'] == 'modelMetadata']
                if metas:
                    meta = json.loads(metas[0])
                    name = meta.get('notebookName')
                    desc = meta.get('notebookDescription')
                    if name:
                        print('   Syncing notebook')
                        print('      Exporting notebook')
                        r = fw.client.export_notebook(scn, name=name,
                                                      description=desc)
                        nb_id = r['notebookId']
                        # get the last up to date container
                        cont = fw.client.get_container(scn)
                        qq = cont['qualifiers']
                        for q in qq:
                            if q['name'] == 'modelMetadata':
                                values = json.loads(q['value'])
                                values['notebookId'] = nb_id
                                q['value'] = json.dumps(values)
                        # update qualifiers
                        j = {'qualifiers': qq}
                        fw.client.update_container(cont)
        except KeyError:
            pass



def import_scenario(fw, arcname, data, arc_spec, input):
    if arc_spec.is_table() and arc_spec.table_category in ['input', 'output']:
        # for now, only tables can be 'missing'
        if arc_spec.data_name.endswith('.missing'):
            print('   IGNORING missing table %s' % arc_spec.arcname)
        else:
            print("   Uploading data  %s as '%s' in %s:%s" %
                  (arc_spec.data_name, arc_spec.table_category,
                   arc_spec.scenario_name, arc_spec.scenario_category))
            upload_csv(fw, arc_spec, data, input)
    elif arc_spec.is_asset():
        print("   Uploading asset %s as '%s' in %s:%s" %
              (arc_spec.data_name, arc_spec.asset_category,
               arc_spec.scenario_name, arc_spec.scenario_category))
        upload_asset(fw, arc_spec, data, input)
    elif arc_spec.is_metadata():
        pass  # meta data are processed when container is created
    else:
        print('   IGNORED: Don\'t know what to do with %s' % arcname)


def import_framework(server=None,
                     api_url=None,
                     authorization=None,
                     project=None,
                     framework=None,
                     input=None,
                     clean=None):
    print('%s: Importing framework "%s" in project "%s" from %s' %
          (server, framework, project, input))
    project_id = get_project_id(server, authorization, project)
    if project_id is None:
        print('ERROR: The project %s does not exist' % project)
        exit(1)
    client = Client(project_id=project_id,
                    authorization=authorization,
                    api_url=api_url)
    if framework is not None:
        default_fw = client.get_model_builder(framework)
        if clean and default_fw:
            print('Deleting framework %s (clean mode)' % framework)
            client.delete_model_builder(default_fw)
            default_fw = None
        if default_fw is None:
            print('Creating framework name = %s' % framework)
            default_fw = client.create_model_builder(name=framework)
    else:
        default_fw = None
    frameworks = {}
    for arcname, data in input.inputs:
        arc_spec = ArchiveName(arcname)
        if framework is not None:
            fw = default_fw
        else:
            fw = frameworks.get(arc_spec.framework_name, None)
            if fw is None:
                fw = client.get_model_builder(arc_spec.framework_name)
                if clean and fw:  # that will have the effect of deleting the
                    # framework the first time it is cached
                    print('Deleting framework %s' % arc_spec.framework_name)
                    client.delete_model_builder(fw)
                    fw = None
                if fw is None:
                    print('Creating framework %s' % arc_spec.framework_name)
                    fw = client.create_model_builder(name=arc_spec.framework_name)
                frameworks[arc_spec.framework_name] = fw
        import_scenario(fw, arcname, data, arc_spec, input)


def export_framework(server=None,
                     api_url=None,
                     authorization=None,
                     project=None,
                     framework=None,
                     output=None):
    print('%s: Exporting framework "%s" from project "%s" to %s' %
          (server, project, framework, output))
    project_id = get_project_id(server, authorization, project)
    if project_id is None:
        print('ERROR: The project %s does not exist' % project)
        exit(1)
    print('project id = %s' % project_id)
    print('using api url = %s' % api_url)
    client = Client(project_id=project_id, authorization=authorization,
                    api_url=api_url)
    fw = client.get_model_builder(name=framework)
    for container in fw.get_containers():
        # qualifiers we want to keep
        q = container.qualifiers if container.qualifiers else []
        if len(q) > 0:
            arcname = '/'.join([framework,
                                container.category,
                                container.name,
                                'metadata.json'])
            data = {'qualifiers': q}
            print('   Writting metadata %s' % arcname)
            output.add(arcname, json.dumps(data).encode('utf-8'))
        tables = container.get_tables()
        for tablename, table in iteritems(tables):
            arcname = '/'.join([framework,
                                container.category,
                                container.name,
                                'table',
                                table.category,
                                table.name + '.csv'])
            print("   Writting table %s" % arcname)
            try:
                table_data = client.get_table_data(container, name=table.name,
                                                   raw=True)
                output.add(arcname, table_data if table_data is not None else b'')
            except DDException as dde:
                print('      *** WARNING *** %s' % dde)
                if 'table_not_found' in str(dde):
                    arcname = '%s.missing' % arcname
                    print('      writing placeholder %s' % arcname)
                    output.add(arcname, b'')
        assets = container.get_assets()
        for assetname, asset in iteritems(assets):
            arcname = '/'.join([framework,
                                container.category,
                                container.name,
                                'asset',
                                asset.category,
                                asset.name])
            print("   Writting asset %s" % arcname)
            output.add(arcname, container.get_asset_data(asset.name))


def run_command(prog, argv, output_handler=None, api_url=None):
    description = '''Command line client for Decision Optimization scenarios.'''
    epilog = '''Command details:
  export         Exports a decision framework.
  import         imports a decision framework.

  For authorization, one of the authorization or user/password arguments is required.

  Tables of a scenario are written or read as:

     <framework name>/<scenario category>/<scenario name>/table/<table category>/table_name.csv

  where <table category> is (input|output)
        <scenario category> is (scenario|input_set|model)

  Assets are written as:

     <framework name>/<scenario category>/<scenario name>/asset/asset_name

Examples:

  Exports framework 'Diet problem' into zip file:

     $ python -m dd_scenario.cli --user joe@ibm.com --password PaSSwoRd1 --project 'MyProject' --framework 'Diet problem' export output.zip
'''
    parser = argparse.ArgumentParser(prog=prog, description=description, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command',
                        metavar='COMMAND',
                        help='DD import/export command')
    parser.add_argument('arguments', metavar='ARG', nargs='*',
                        help='Arguments for the command')
    parser.add_argument('--cookie', metavar='COOKIE_FILE',
                        default=None,
                        help="The cookie file containing authorization")
    parser.add_argument('--authorization', metavar='AUTH',
                        default=None,
                        help="Authorization token")
    parser.add_argument('--user', '-u', metavar='USER',
                        default=None,
                        help="User")
    parser.add_argument('--password', '-p', metavar='PASSWORD',
                        default=None,
                        help="Password")
    parser.add_argument('--server', metavar='SERVER',
                        default=None,
                        help="Server")
    parser.add_argument('--api', metavar='API_URL',
                        default=None,
                        help="API Url to use")
    parser.add_argument('--project', metavar='PROJECT_NAME',
                        default=None,
                        help="project name. The project must exist.")
    parser.add_argument('--framework', metavar='FRAMEWORK_NAME',
                        default=None,
                        help="The name of the framework")
    parser.add_argument('--clean',
                        default=True,
                        action='store_true',
                        help="If specified, any existing framework is first deleted then recreated (default is True)")
    parser.add_argument('--no-clean',
                        dest='clean',
                        action='store_false',
                        help="If specified, do not delete framework if it exists (update mode).")
    args = parser.parse_args(argv)
    # tune parameters
    # if cookie is provided:
    if args.cookie:
        args.authorization = get_user_token_from_cookie_txt(args.cookie)
    # check that authorization is there
    if (args.authorization is None) and (args.user is None):
        print('Authorization or user/password are required')
        return -1
    # make sure args.server starts with a scheme (default: https)
    pserv = urlparse(args.server)
    if pserv.scheme == '':
        args.server = 'https://%s' % args.server
    # get token
    if args.authorization is None:
        args.authorization = get_authorization(args.server, args.user, args.password)
    # if auth is still None -> check credentials
    if args.authorization is None:
        print('Could not get authorization from server. Please check credentials')
        return -1
    # api url
    if args.api is None:
        if api_url is None:
            args.api = "%s/v2" % args.server
        else:
            args.api = api_url
    # process commands
    if args.command == 'import':
        if len(args.arguments) < 1:
            print('Import needs a directory or zip file for output')
            return -1
        zip_or_dir = args.arguments[0]
        input_handler = ZipInput(zip_or_dir) if zip_or_dir.lower().endswith('.zip') \
            else DirectoryInput(zip_or_dir)
        import_framework(server=args.server,
                         api_url=args.api,
                         authorization=args.authorization,
                         project=args.project,
                         framework=args.framework,
                         input=input_handler,
                         clean=args.clean)
    elif args.command == 'export':
        if len(args.arguments) < 1:
            print('Exports needs a directory or zip file for output')
            return -1
        zip_or_dir = args.arguments[0]
        if output_handler is None:
            output_handler = ZipOutput(zip_or_dir) if zip_or_dir.lower().endswith('.zip') \
                else DirectoryOutput(zip_or_dir)
        try:
            export_framework(server=args.server,
                             api_url=args.api,
                             authorization=args.authorization,
                             project=args.project,
                             framework=args.framework,
                             output=output_handler)
        finally:
            output_handler.close()
    else:
        print('Unknown command: %s' % args.command)
        parser.print_help()
        return -1
    return 0


if __name__ == '__main__':
    exit(run_command(sys.argv[0], sys.argv[1:]))

import requests
import json
import os


class WorkspaceNotFound(Exception):
    pass


class ImproperCredentials(Exception):
    pass

class ImproperFormat(Exception):
    pass

class ParameterRequired(Exception):
    pass

class Geoserver(object):
    """
    T
    """

    def __init__(self, geoserver_url='http://localhost:8080/geoserver/', username="admin",
                 password="geoserver"):  # , disable_ssl_certificate_validation=False):
        self.geoserver_url = geoserver_url
        self.auth = (username, password)
        if self.geoserver_url[-1] != '/':
            self.geoserver_url = self.geoserver_url + '/'
        if 'geoserver' not in self.geoserver_url:
            self.geoserver_url = self.geoserver_url + 'geoserver/'

        self.headers = {'Content-type': 'text/json'}
        response = requests.post(self.geoserver_url, headers=self.headers, auth=self.auth)

        if response.status_code != 200:
            raise ImproperCredentials("The credentials you provided weren't correct")
        else:
            self.geoserver_url = self.geoserver_url + 'rest/'

    
    def get_workspace(self, workspace_name):
        response = requests.get(self.geoserver_url + 'workspaces/' + workspace_name + '.json', headers=self.headers, auth=self.auth)
        if response.status_code == 200:
            return response.content, response.status_code
        else:
            raise WorkspaceNotFound("Workspace couldn't be found")


    def create_workspace(self, workspace_name):
        data = json.dumps({'workspace':{'name':workspace_name}})

        response = requests.post(self.geoserver_url + 'workspaces', headers=self.headers, auth=self.auth, data=data)

        if response.status_code == 201:
            return response.status_code
        else:
            raise WorkspaceNotFound("Workspace couldn't be found")

    def list_workspaces(self):
        response = requests.get(self.geoserver_url + 'workspaces.json', headers=self.headers,
                                auth=self.auth)

        if response.status_code == 200:
            return response.content, response.status_code
        else:
            raise WorkspaceNotFound("Workspace couldn't be found")



    def upload_shapefile_zip(self, workspace_name, datastore_name=None, file=None, address=None):

        if not (file or address):
            raise ParameterRequired('At least one keyword of %s=x or %s=y is required' % ('address', 'file'))
        else:
            if address:
                try:
                    file = open(address, 'rb')
                    filename, file_extension = os.path.splitext(file.name)
                    file = file.read()
                except IOError:
                    print('Ops, it seems the address you provided is not correct')

            if file_extension != '.zip':
                raise ImproperFormat('A .zip file is required')

            if (not datastore_name) and filename.index('/') != -1:
                datastore_name = filename.split('/')[-1]
            elif not datastore_name:
                datastore_name = filename.split('\\')[-1]

        headers = {
            'Content-type': 'application/zip',
        }

        url = '%sworkspaces/%s/datastores/%s/file.shp' % (self.geoserver_url,workspace_name, datastore_name)

        response = requests.put(url, headers=headers,data=file, auth=self.auth)

        if response.status_code != 201:
            raise ImproperFormat('The information provided was invalid')
        else:
            return response.status_code


geoserv = Geoserver()

# code = geoserv.create_workspace('my_workspace')
# code, results = geoserv.get_workspace('my_workspace')
# code, results = geoserv.list_workspaces()

geoserv.upload_shapefile_zip('my_workspace', address='/Users/bobleujr/Downloads/shapefile_example.zip')



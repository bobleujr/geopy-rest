import requests
import json


class WorkspaceNotFound(Exception):
    pass


class ImproperCredentials(Exception):
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


geoserv = Geoserver()

code = geoserv.create_workspace('my_workspace')
code, results = geoserv.get_workspace('my_workspace')
code, results = geoserv.list_workspaces()


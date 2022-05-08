import json
import base64
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
import config

class EmpireController:
    def __init__(self):
        self.HEADERS = {'Content-Type': 'application/json',}
        self.args = config.empire_conf()


    def getEmpireToken(self):
        data = {
            "username":self.args['username'],
            "password":self.args['password']
            }
        payload = json.dumps(data)
        baseEndPoint = "/api/admin/login"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.post(url, headers=self.HEADERS, data=payload, verify=False)
        result = response.json()
        try:
            if result['token']:
                token = result['token']
        except(KeyError):
            token = ''
        finally:
            return(token)

    def createHTTPListener(self, token):
        params = (('token', token),)
        data = {
            "Name":self.args['listenerName'],
            "Port":self.args['port']
            }
        payload = json.dumps(data)
        baseEndPoint = "/api/listeners/http"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.post(url, headers=self.HEADERS, params=params, data=payload, verify=False)
        result = response.json()
        try:
            if result['success']:
                value = 1
        except(KeyError):
            if result['error']:
                value = 0
        finally:
            return(value)


    def getAllStager(self, token):
        params = (('token', token),)
        baseEndPoint = "/api/stagers"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.get(url, params=params, verify=False)
        result = response.json()
        stagerlists = []
        try:
            if result['stagers']:
                for stager in result['stagers']:
                    stagerlists.append([stager['Name'],stager['Description']])
        except(KeyError):
            stagerlists.append(['',''])
        finally:
            return(stagerlists)

    def getCurrentListeners(self,token):
        params = (('token', token),)
        baseEndPoint = f"/api/listeners/{self.args['listenerName']}"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.get(url, params=params, verify=False)
        result = response.json()
        listenrers = []
        try:
            if result['listeners']:
                for listener in result['listeners']:
                    module = listener['module']
                    name = listener['name']
                    host = listener['options']['Host']['Value']
                    launcher = listener['options']['Launcher']['Value']
        except(KeyError):
            module, name, host, launcher = '', '', '', ''
        finally:
            listenrers.append([name,module,host,launcher])
            return(listenrers)

    def killListener(self, token, listener):
        params = (('token', token),)
        baseEndPoint = f"/api/listeners/{listener}"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.delete(url, params=params, verify=False)
        result = response.json()
        try:
            if result['success']:
                value = 1
        except(KeyError):
            if result['error']:
                value = 0
        finally:
            return(value)

    def generateStager(self, token, stagerName, listener):
        params = (('token', token),)
        baseEndPoint = "/api/stagers"
        url = f"{self.args['server']}{baseEndPoint}"
        data = {
            "StagerName":stagerName,
            "Listener":listener
            }
        payload = json.dumps(data)
        response = requests.post(url, headers=self.HEADERS, params=params, data=payload, verify=False)
        result = response.json()
        stagers = []
        try:
            if result[stagerName]:
                try:
                    outstr = base64.b64decode(result[stagerName]['Output']).decode()
                except:
                    outstr = result[stagerName]['Output']
                outfile = result[stagerName]['OutFile']['Value']
        except(KeyError):
            outstr, outfile = '',''
        finally:
            stagers.append([outstr,outfile])
            return(stagers)

    def getCurrentAgents(self, token):
        params = (('token', token),)
        baseEndPoint = "/api/agents"
        url = f"{self.args['server']}{baseEndPoint}"
        response = requests.get(url, params=params, verify=False)
        result = response.json()
        agents = []
        if result['agents']:
            for agent in result['agents']:
                try:
                    id = agent['ID']
                    name = agent['session_id']
                    language = agent['language']
                    internal_ip = agent['internal_ip']
                    username = agent['username']
                    process_name = agent['process_name']
                    process_id = agent['process_id']
                    lastseen_time = agent['lastseen_time']
                    listener = agent['listener']
                except(KeyError):
                    id, name, language, internal_ip, username, process_name, process_id, lastseen_time, listener = '','','','','','','','',''
                try:
                    os_details = agent['os_details']
                except(KeyError):
                    os_details = ''
                agents.append([id,name,language,internal_ip,username,process_name,process_id,lastseen_time,listener,os_details])
        else:
            agents.append(['','','','','','','','','',''])
        return(agents)

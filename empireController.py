import json
import base64
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from config import empire_conf as config

headers = {'Content-Type': 'application/json',}

def getEmpireToken():
    args = config()
    data = {
        "username":args['username'],
        "password":args['password']
        }
    payload = json.dumps(data)
    baseEndPoint = "/api/admin/login"
    url = args['server'] + baseEndPoint
    response = requests.post(url, headers=headers, data=payload, verify=False)
    result = response.json()
    try:
        if result['token']:
            token = result['token']
    except(KeyError):
        token = ''
    finally:
        return(token)

def createHTTPListener(token, listener, port):
    args = config()
    params = (('token', token),)
    data = {
        "Name":listener,
        "Port":port
        }
    payload = json.dumps(data)
    baseEndPoint = "/api/listeners/http"
    url = args['server'] + baseEndPoint
    response = requests.post(url, headers=headers, params=params, data=payload, verify=False)
    result = response.json()
    try:
        if result['success']:
            value = 1
    except(KeyError):
        if result['error']:
            value = 0
    finally:
        return(value)


def getAllStager(token):
    args = config()
    params = (('token', token),)
    baseEndPoint = "/api/stagers"
    url = args['server'] + baseEndPoint
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

def getCurrentListeners(token,listener):
    args = config()
    params = (('token', token),)
    baseEndPoint = "/api/listeners/" + listener
    url = args['server'] + baseEndPoint
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

def killListener(token, listener):
    args = config()
    params = (('token', token),)
    baseEndPoint = "/api/listeners/" + listener
    url = args['server'] + baseEndPoint
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

def generateStager(token, stagerName, listener):
    args = config()
    params = (('token', token),)
    baseEndPoint = "/api/stagers"
    url = args['server'] + baseEndPoint
    data = {
        "StagerName":stagerName,
        "Listener":listener
        }
    payload = json.dumps(data)
    response = requests.post(url, headers=headers, params=params, data=payload, verify=False)
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

def getCurrentAgents(token):
    args = config()
    params = (('token', token),)
    baseEndPoint = "/api/agents"
    url = args['server'] + baseEndPoint
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

# if __name__ == "__main__":
    # token = getEmpireToken()
    # listenerName = "pakuri"
    # port = "8081"
    # result = createHTTPListener(token, listenerName, port)
    # print(result)
    # result = getCurrentListeners(token, listenerName)
    # print(result)
    # stagerName = "multi/macro"
    # result = generateStager(token, stagerName, listenerName)
    # print(result)
    # result = killListener(token, listenerName)
    # print(result)
    # result=getCurrentAgents(token)
    # print(result)

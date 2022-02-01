import errno
import json
import sys
import xml.etree.ElementTree as ET
import db_controller as db
import requests
from config import chat_conf as config
import Communicator as comm


def NextcloudTalkSendMessage(token, message):
    """指定したtokenを持つ部屋にメッセージを送信する

    Args:
        token : tokenパラメータ
        message : 送信メッセージ
    """
    data = {
        "token": token,
        "message": message,
    }
    params = config()
    baseEndPoint = "/ocs/v2.php/apps/spreed/api/v1"
    url = params['server'] + baseEndPoint + "/chat/{}".format(token)
    payload = json.dumps(data)
    headers = {'content-type': 'application/json', 'OCS-APIRequest': 'true'}
    requests.post(url, data=payload, headers=headers, auth=(params['username'], params['password']))

def NextcloudTalkSendInformation(message):
    """Information Room へtokenを使用してメッセージを送信する

    Args:
        token : tokenパラメータ
        message : 送信メッセージ
    """
    params = config()
    token = NextcloudTalkGetInfoRoomToken()[0]
    data = {
        "token": token,
        "message": message,
    }
    baseEndPoint = "/ocs/v2.php/apps/spreed/api/v1"
    url = params['server'] + baseEndPoint + "/chat/{}".format(token)
    payload = json.dumps(data)
    headers = {'content-type': 'application/json', 'OCS-APIRequest': 'true'}
    requests.post(url, data=payload, headers=headers, auth=(params['username'], params['password']))


def NextcloudTalkGetInfoRoomToken():
    """InformationのroomNameを受け取り、tokenを配列で返す

    Returns:
        [str array]: [token]
    """
    params = config()
    baseEndPoint = "/ocs/v2.php/apps/spreed/api/v4"
    url = params['server'] + baseEndPoint + "/room"
    headers = {'content-type': 'application/json', 'OCS-APIRequest': 'true'}
    response = requests.get(url, headers=headers, auth=(params['username'], params['password']))
    try:
        responseXml = ET.fromstring(response.text)
    except ET.ParseError as e:
        print("Parse error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(2)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(2)
    data = responseXml.findall("data")
    elments = data[0].findall("element")
    token = []
    for element in elments:
        roomName = element.find("name").text
        if roomName == params['inforoom']:
            token.append(element.find("token").text)
    return token


def NextcloudTalkGetRoomToken():
    """roomNameを受け取り、tokenを配列で返す

    Returns:
        [str array]: [token]
    """
    params = config()
    baseEndPoint = "/ocs/v2.php/apps/spreed/api/v4"
    url = params['server'] + baseEndPoint + "/room"
    headers = {'content-type': 'application/json', 'OCS-APIRequest': 'true'}
    response = requests.get(url, headers=headers, auth=(
        params['username'], params['password']))
    try:
        responseXml = ET.fromstring(response.text)
    except ET.ParseError as e:
        print("Parse error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(2)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(2)
    data = responseXml.findall("data")
    elments = data[0].findall("element")
    token = []
    for element in elments:
        token.append( element.find("token").text)
    return token

def NextcloudTalkGetReceivedmessage(token_array):
    """Botへのメッセージを受け取り、DBに保存する

    Args:
        token : tokenの配列
    """
    data = {
        "lookIntoFuture": 1,
        "includLastKnown":0
    }
    params = config()
    for token in token_array:
        baseEndPoint = "/ocs/v2.php/apps/spreed/api/v1"
        url = params['server'] + baseEndPoint + "/chat/{}".format(token)
        payload = json.dumps(data)
        headers = {'content-type': 'application/json', 'OCS-APIRequest': 'true'}
        response = requests.get(url, data=payload, headers=headers, auth=(params['username'], params['password']))
        try:
            responseXml = ET.fromstring(response.text)
        except ET.ParseError as e:
            print("Parse error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(2)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit(2)
        data_elements = responseXml.findall("data")
        elments = data_elements[0].findall("element")
        for element in elments:
            talkId = element.find("id").text
            actor = element.find("actorId").text
            message = element.find("message").text
            try:
                msg_parameters = element.find("messageParameters")[0].find("id")
                userid = msg_parameters.text
                if userid == params['username']:
                    message = message.split(" ")[1]
                    sql = """SELECT msgid FROM t_message_list WHERE msgid = %s;"""
                    id = db.get_SingleValue(sql, talkId)
                    if id is None:
                        # DBに登録されてないのでIPを登録し、戻り値のIDを格納
                        sql = """INSERT INTO t_message_list(msgid, token, actor, message, response) VALUES(%s,%s,%s,%s,%s) RETURNING id;"""
                        arg = (talkId, token, actor, message,"0")
                        db.insert_db(sql, arg)
            except:
                pass

if __name__ == "__main__":
    tokenArry = NextcloudTalkGetRoomToken()
    NextcloudTalkGetReceivedmessage(tokenArry)
    # Check Messages
    sql = """SELECT id,token,actor,message FROM t_message_list WHERE response = %s;"""
    messages = db.get_AllValues(sql, "0")
    for message in messages:
        id = message[0]
        token = message[1]
        actor = message[2]
        msg = message[3]
        receivedMsg = (id, token, actor, msg)
        comm.ChatCommunication(receivedMsg)

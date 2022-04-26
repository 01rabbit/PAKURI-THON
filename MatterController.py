import json
import requests
from flask import request
from config import matter_conf as config
import datetime
from textwrap import dedent
import db_controller as db
import JobController as jc


def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def botbot_reply():
    params = config()
    BOT_TOKEN = params['bot_id']
    posted_user = request.json['user_name']
    CHANNEL_ID = params['channel_id']
    posted_msg  = request.json['text']
    baseEndPoint = "/api/v4/posts"
    url = params['server'] + baseEndPoint
    
    reply_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + BOT_TOKEN,
    }


    answer = ""
    strArry = posted_msg.split(" ")
    command = strArry[1]
    if command == "hello":
        answer = "hello"
    # scan
    elif command == "nmap":
        sql = """SELECT cmd_name,value FROM t_command_list WHERE cmd_type = %s;"""
        nmap_list = db.get_AllValues(sql, "nmap")
        cmdNames = []
        for nmapCmd in nmap_list:
            cmdName = nmapCmd[0]
            cmdNames.append(cmdName)
        if len(strArry) == 4:
            cmdType = strArry[3]
            target = strArry[4]
            for nmapCmd in nmap_list:
                cmdName, value = nmapCmd
                if cmdType == cmdName:
                    answer = "I'll run a " + cmdName + " to " + target
                    filename = cmdName + "_" + target + "_" + get_timestamp()
                    cmdValue = value + " " + target + " -oA tmp/" + filename + " &&  python xmlparser.py tmp/" + filename +".xml"
                    jc.Set_myjob(cmdValue, posted_user)
                    break
            if answer == "":
                answer = "I don't know what to do with " + cmdType + ".\n"
                answer += "If you want to use Nmap to do the scanning, enter it in the following format:\n" +\
                    "nmap,[Command Name],[Target IP]\n Nmap command names are:\n" + str(cmdNames)
        else:
            answer = "If you want to use Nmap to do the scanning, enter it in the following format:\n" +\
                "nmap,[Command Name],[Target IP]\n Nmap command names are:\n" + str(cmdNames)

    # other or help
    else:
        answer = '''
        I don't konw :)
        If you hello, I will say hello back.
        '''
        answer += "If you want to use Nmap to do the scanning, enter it in the following format:\n" +\
            "nmap,[Command Name],[Target IP]\n"

    result = dedent(answer)
    
    reply_data = {
        "channel_id": CHANNEL_ID,
        "message": f"@{posted_user} " + result,
        "props": {
            "attachments": [
                    {
                "author_name": posted_user,
                "text": posted_msg,
                }
            ]
        },
    }
    
    sql = """UPDATE t_message_list SET response = %s WHERE id = %s;"""
    args = ("1", id)
    db.update_db(sql, args)

    return requests.post(url, headers=reply_headers, data=json.dumps(reply_data))

    # reply_request = requests.post(
    #     MM_API_ADDRESS,
    #     headers = reply_headers,
    #     data = json.dumps(reply_data)
    # )

    # return reply_request
    # return requests.post(MM_API_ADDRESS, headers = reply_headers, data = payloads)

def botbot_information(commander, message):
    params = config()
    BOT_TOKEN = params['bot_id']
    CHANNEL_ID = params['channel_id']
    baseEndPoint = "/api/v4/posts"
    url = params['server'] + baseEndPoint
    
    reply_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + BOT_TOKEN,
    }
    
    reply_data = {
        "channel_id": CHANNEL_ID,
        "message": f"@{commander} " + message,
    }

    return requests.post(url, headers=reply_headers, data=json.dumps(reply_data))
    
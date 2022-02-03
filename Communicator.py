import sys
import datetime
from textwrap import dedent
import ChatController as cc
import db_controller as db
import JobController as jc


def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def ChatCommunication(rcvMsg):
    id = rcvMsg[0]
    token = rcvMsg[1]
    actor = rcvMsg[2]
    message = rcvMsg[3]
    answer = ""
    strArry = message.split(",")
    command = strArry[0]
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
        if len(strArry) == 3:
            cmdType = strArry[1]
            target = strArry[2]
            for nmapCmd in nmap_list:
                cmdName, value = nmapCmd
                if cmdType == cmdName:
                    answer = "I'll run a " + cmdName + " to " + target
                    filename = cmdName + "_" + target + "_" + get_timestamp()
                    cmdValue = value + " " + target + " -oA tmp/" + filename + " &&  python xmlparser.py tmp/" + filename +".xml"
                    jc.Set_myjob(cmdValue, actor, token)
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
    ans_msg = ">> @"+actor+"\n"+result

    cc.NextcloudTalkSendMessage(token, ans_msg)
    sql = """UPDATE t_message_list SET response = %s WHERE id = %s;"""
    args = ("1", id)
    db.update_db(sql, args)

def ChatSendMessage(token, actor, msg):
    ans_msg = ">> @" + actor +" \n" + dedent(msg)
    cc.NextcloudTalkSendMessage(token, ans_msg)

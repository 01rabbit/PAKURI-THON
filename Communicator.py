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
        if len(strArry) == 3:
            cmdType = strArry[1]
            target = strArry[2]
            if cmdType == "Quick":
                answer = "I'll run a fast scan to "+target
                cmdValue = "nmap -T4 -Pn -F " + target + " -oA tmp/Quick_scan_" + target +"_" + get_timestamp()
                jc.Set_myjob(cmdValue)
            elif cmdType == "Regular":
                answer = "I'll run a regular scan to "+target
                cmdValue = "nmap -T4 -Pn -oA tmp/Regular_scan_" + target +"_" + get_timestamp()
                jc.Set_myjob(cmdValue)
            elif cmdType == "Full":
                answer = "I'll run a full scan to "+target
                cmdValue = "nmap -sC -sV -n -sT -O -p- -oA tmp/All_TCP_Ports_scan_" + target +"_" + get_timestamp()
                jc.Set_myjob(cmdValue)
            else:
                answer = '''
    I don't know what to do
    If you want to use Nmap for scanning, type inthe following example:
    nmap,[Quick,Regular,Full],IP
    '''
        else:
            answer = '''
    I don't know what to do
    If you want to use Nmap for scanning, type inthe following example:
    nmap,[Quick,Regular,Full],IP
    '''
    # autorecon
    elif command == "autorecon":
        if len(strArry) == 2:
            value2 = strArry[1]
            answer = "I'll use Autorecon to run a scan to "+value2
        else:
            answer = '''
        I don't know what to do
        If you want to use Autorecon to enumetate the target information, type inthe following example:
        \"autorecon,IP\"
        '''
    # other or help
    else:
        answer = '''
        I don't konw :)
        If you hello, I will say hello back.
        If you want to use Nmap for scanning, type inthe following example:
        nmap,[Quick,Regular,Full],IP
        If you want to use Autorecon to enumetate the target information, type inthe following example:
        \"autorecon,IP\"
        '''
    result = ">> " + command + "\n" + dedent(answer)
    ans_msg = "@"+actor+" "+result

    cc.NextcloudTalkSendMessage(token, ans_msg)
    sql = """UPDATE t_message_list SET response = %s WHERE id = %s;"""
    args = ("1", id)
    db.update_db(sql, args)

def ChatSendMessage(token, msg):
    ans_msg = ">> @all \n" + dedent(msg)
    cc.NextcloudTalkSendMessage(token, ans_msg)

import datetime
from flask import request
import db_controller as db
import JobController as jc
import MatterController as mc

# 現在時刻の把握
def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Cmd向けHELP
def cmd_i_dont_know(user,cmd):
    attachment = {
                "mrkdwn_in": ["text"],
                "text": f"@{user} If you have any questions, please type `{cmd} help`."
            }
    return attachment


def cmd_howto(user,cmd):
    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#917c50",
        "text": f"@{user} If you want me to use {cmd}, please enter it in the following format." + "\n \
***Be careful to separate the commands with a space.***\n\
`nmap [Command Type] [Target IP Address]`\n\n\
### Command Type",
    }
    sql = """SELECT cmd_name,description FROM t_command_list WHERE cmd_type = %s;"""
    cmdList = db.get_AllValues(sql, cmd)
    attachfield = []
    for selectCmd in cmdList:
        attachfield.append({"title": selectCmd[0],"value": selectCmd[1],"short": "false"},)
        attachment["fields"] = attachfield
    return attachment

def help_me():
    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#9a1117",
        "text": "Need help?\n\ I am #P.i.t.to. controlling this system.\n\
If you want an nmap scan, please chat with `#pitto nmap help` first.\n\
Or if you want a nikto scan, please chat with #pitto nikto help` first."
}
    return attachment

def ChatCommunication():
    posted_user = request.json['user_name']
    posted_msg  = request.json['text']

    strArry = posted_msg.split(" ")
    # strArry[0] : WakeUp Code
    # strArry[1] : Command
    # strArry[2] : Argument
    # strArry[3] : Target
    command = strArry[1]

    if command == "hello" or command == "Hello":
        attachment = {"mrkdwn_in": ["text"], "text": f"Hi, @{posted_user} ! :wave:" }
    elif command == "hi" or command == "Hi":
        attachment = {"mrkdwn_in": ["text"], "text": f"Hello, @{posted_user} ! :wave:" }
    elif command == "help":
        attachment = help_me()

    # nmap or nikto
    elif command == "nmap" or command == "nikto":
        # gather all nmap commands
        sql = """SELECT cmd_name,value FROM t_command_list WHERE cmd_type = %s;"""
        cmdList = db.get_AllValues(sql, command)
        cmdNames = []
        for selectCmd in cmdList:
            cmdName = selectCmd[0]
            cmdNames.append(cmdName)
        if len (strArry) == 3:
            args = strArry[2]
            if args == "help":
                attachment = cmd_howto(posted_user,command)
            else:
                attachment = cmd_i_dont_know(posted_user,command)
        elif len(strArry) == 4:
            cmdType = strArry[2]
            target = strArry[3]
            for selectCmd in cmdList:
                cmdName, value = selectCmd
                if cmdName == cmdType:
                    filename = cmdName + "_" + target + "_" + get_timestamp()
                    if command == "nmap":
                        cmdValue = value + " " + target + " -oA tmp/" + filename + " &&  python xmlparser.py tmp/" + filename +".xml"
                    elif command == "nikto":
                        cmdValue = value + target + " -o tmp/" + filename + ".xml | tee tmp/" + filename + ".txt && python xmlparser.py tmp/" + filename + ".xml"
                    attachment = {
                        "mrkdwn_in": ["text"],
                        "fallback": "I'll run a " + cmdName + " to " + target,
                        "title": "Your order",
                        "pretext": "I'll run a " + cmdName + " to " + target,
                        "text": cmdValue
                    }
                    jc.Set_myjob(cmdValue, posted_user)
                    break
            if cmdValue == "":
                attachment = cmd_howto(posted_user,command)
        else:
            attachment = cmd_i_dont_know(posted_user,command)

    # other or help
    else:
        pretext = "I don't konw :man_shrugging:"
        attachment = {
            "markdwn_in": ["text","pretext"],
            "pretext" : pretext,
            "color": "#9a1117",
            "text": "If you have any questions, please type `help`. :thumbsup:"
        }
    
    return mc.botbot_information(attachment)

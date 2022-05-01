import datetime
from flask import request
import db_controller as db
import JobController as jc
import MatterController as mc

def get_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def cmd_i_dont_know(user,cmd):
    attachment = {
                "mrkdwn_in": ["text"],
                "text": f"@{user} If you have any questions, please type `#pitto {cmd} help`."
            }
    return attachment

def info_howto(*args):
    user=args[0]
    flg=args[1]
    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#9a1117",
    }
    if flg == "norecord":
        attachment["text"] = f"@{user} The IP address entered is not on the target list. Please try again."
    else:
        attachment["text"] = f"@{user} If you want to know more information about a host, please enter `#pitto info [IP Address]`"
    
    return attachment

def cmd_howto(user,cmd):
    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#917c50",
        "text": f"@{user} If you want me to use {cmd}, please enter it in the following format." + f"\n \
***Be careful to separate the commands with a space.***\n\
`#pitto {cmd} [Command Type] [Target IP Address]`\n\n\
#### Command Type",
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
        "text": "Need help?\nI am ***P.I.T.To***. controlling this system.\n\
For example, if you want to do a reconnaissance, enter `#pitto nmap help` or `#pitto nikto help`.\n\
If you want to see information about a target, type `#pitto info help`. "
}
    return attachment

def targetlist():
    sql = """SELECT * FROM t_host_list;"""
    hosts = db.get_AllValues(sql, "")

    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#9a1117",
        "text": "#### Host list"
    }
    attachfield = []
    for host in hosts:
        attachfield.append({
                "title": f"{host[1]}" + f" ({host[2]})",
                "value": f"Hostname: {host[3]}",
                "short": "true"
            },)
        attachment["fields"] = attachfield
    return attachment

def hostinfo(host_id):
    sql = """SELECT * FROM t_host_list WHERE id = %s;"""
    host = db.get_AllValues(sql,host_id)[0]
    sql = """SELECT * FROM t_port_list WHERE host_id = %s;"""
    ports = db.get_AllValues(sql,host_id)
    
    attachment = {
        "mrkdwn_in": ["text"],
        "color": "#9a1117",
        "thumb_url": "images/other.png",
        "text": f"#### IP: {host[1]}\n" + f"##### MAC:{host[2]}\n" +\
            f"##### OS:{host[7]}\n---",
    }
    attachfield = []
    for port in ports:
        attachfield.append({
                "value": f"**{port[3]}/{port[2]} ({port[5]})** {port[6]} {port[7]} {port[8]}",
                "short": "false"
            },)
        attachment["fields"] = attachfield
    
    return attachment

def ChatCommunication():
    posted_user = request.json['user_name']
    posted_msg  = request.json['text']

    strArry = posted_msg.split(" ")
    ## strArry[0] : WakeUp Code ##
    ## strArry[1] : Command     ##
    ## strArry[2] : Argument    ##
    ## strArry[3] : Target      ##
    command = strArry[1]

    if command == "hello" or command == "Hello":
        attachment = {"mrkdwn_in": ["text"], "text": f"Hi, @{posted_user} ! :wave:" }
    elif command == "hi" or command == "Hi":
        attachment = {"mrkdwn_in": ["text"], "text": f"Hello, @{posted_user} ! :wave:" }
    elif command == "help":
        attachment = help_me()
    elif command == "target":
        attachment = targetlist()

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
    elif command == "info":
        if len(strArry) == 3:
            target = strArry[2]
            if target == "help":
                attachment = info_howto(posted_user,"help")
            else:
                sql = """SELECT id FROM t_host_list WHERE ip_address = %s;"""
                host_id = db.get_SingleValue(sql, target)
                if host_id is None:
                    attachment = info_howto(posted_user,"norecord")
                else:
                    attachment = hostinfo(host_id)
        else:
            attachment = info_howto(posted_user,"error")
    # other or help
    else:
        pretext = "I don't konw :man_shrugging:"
        attachment = {
            "markdwn_in": ["text","pretext"],
            "pretext" : pretext,
            "color": "#9a1117",
            "text": "If you have any questions, please type `#pitto help`. :thumbsup:"
        }
    
    return mc.botbot_information(attachment)

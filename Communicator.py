import datetime
import ipaddress
from flask import request
import JobController as jc
import pkr_Interface

class Communicator:
    def __init__(self):
        self.db = pkr_Interface.db_controller()
        self.mc = pkr_Interface.matter_controller()
    
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    def check_ipaddress(self,ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def ipaddress_error(self,user,ip):
        """IPアドレスに問題が発生した場合のエラー

        Args:
            user : ユーザ名
            ip : IPアドレス

        Returns:
            Mattermost用のattachment
        """
        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#e2041b", #猩々緋しょうじょうひ
            "text": f"@{user}\n ### :warning: Warning :warning: `{ip}` is an invalid IP address."
        }
        return attachment

    def cmd_i_dont_know(self,user,cmd):
        attachment = {
                    "mrkdwn_in": ["text"],
                    "text": f"@{user} If you have any questions, please type `#pitto {cmd} help`."
                }
        return attachment

    def cmd_help(self,user,cmd):
        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#917347",# 朽葉色くちばいろ
            "text": f"@{user} If you want me to use {cmd}, please enter it in the following format." + f"\n \
    ***Be careful to separate the commands with a space.***\n"
        }
        if cmd == "nikto":
            attachment["text"] += "\n\n##### Example\n`#pitto nikto [Command Type] [Target IP Address]` or `#pitto nikto [Target URL]`"
        elif cmd == "nmap":
            attachment["text"] += f"\n\n##### Example\n`#pitto {cmd} [Command Type] [Target IP Address]`"

        attachment["text"] += f"\n\n##### Command Type\n"
        sql = """SELECT cmd_name,description FROM t_command_list WHERE cmd_type = %s;"""
        cmdList = self.db.get_AllValues(sql, cmd)
        attachment["text"] += "|Command|Discription|\n"
        attachment["text"] += "|:--|:--|\n"
        for selectCmd in cmdList:
            attachment["text"] += f"|{selectCmd[0]}|{selectCmd[1]}|\n"
        return attachment

    def help_me(self):
        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#e2041b", #猩々緋しょうじょうひ
            "text": "Need help? :thinking: \nI am ***P.I.T.To***. controlling this system. :bust_in_silhouette: \n\
    Here is an example of one of my orders to me.\n\
    - Confirm the target list `#pitto target`\n\
    - Confirm target details `#pitto info [IP Address]`\n\
    - Reconnaissance\n\
        - Nmap scanning `#pitto nmap help`\n\
        - Nikto scanning `#pitto nikto help`\n\
        - Other tools scanning `#pitto tools help`\n"
        }
        return attachment

    def targetlist(self):
        sql = """SELECT * FROM t_host_list;"""
        hosts = self.db.get_AllValues(sql, "")

        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#9a1117",
            "text": "#### Host list"
        }
        attachfield = []
        for host in hosts:
            attachfield.append({
                    "title": f"{host[1]} ({host[2]})",
                    "value": f"Hostname: {host[3]}",
                    "short": "true"
                },)
            attachment["fields"] = attachfield
        return attachment

    def hostinfo(self,host_id):
        sql = """SELECT * FROM t_host_list WHERE id = %s;"""
        host = self.db.get_AllValues(sql,host_id)[0]
        sql = """SELECT * FROM t_port_list WHERE host_id = %s;"""
        ports = self.db.get_AllValues(sql,host_id)
        
        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#9a1117",
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

    def info_help(self,*args):
        """Target情報を確認するヘルプ
        Args:
            args[0] : ユーザ名
            args[1] : コマンド名
        Returns:
            Mattermost用のattachment
        """
        user=args[0]
        flg=args[1]
        attachment = {
            "mrkdwn_in": ["text"],
            "color": "#9a1117",
        }
        if flg == "norecord":
            attachment["text"] = f"@{user} The IP address entered is not on the target list.:persevere: Please try again."
        else:
            attachment["text"] = f"@{user} If you want to know more information about a host, please enter `#pitto info [IP Address]` :disappointed_relieved:"
        
        return attachment

    def tools_help(self,user):
        """外部toolを使用するヘルプ
        
        Args:
            user : ユーザ名
                
        """
        attachment = {
            "mrkdwn_in": ["text"],
            "color" : "#38b48b", # 翡翠色ひすいいろ
            "text" : f"@{user} \n\
    1. If you want to use Autorecon, please enter it in the following format.\n\
    ***Be careful to separate the commands with a space.***\n##### Example\n\
    `#pitto tools AutoRecon [Target IP Address]`\n\
    > ### [AutoRecon](https://github.com/Tib3rius/AutoRecon)\n  \
    > ##### Author: Tib3rius\n  \
    > - AutoRecon is a multi-threaded network reconnaissance tool which performs automated enumeration of services. It is intended as a time-saving tool for use in CTFs and other penetration testing environments (e.g. OSCP). It may also be useful in real-world engagements.\n\
    > - The tool works by firstly performing port scans / service detection scans. From those initial results, the tool will launch further enumeration scans of those services using a number of different tools. For example, if HTTP is found, feroxbuster will be launched (as well as many others).\n\
    > - Everything in the tool is highly configurable. The default configuration performs **no automated exploitation** to keep the tool in line with OSCP exam rules. If you wish to add automatic exploit tools to the configuration, you do so at your own risk. The author will not be held responsible for negative actions that result from the mis-use of this tool."
        }
        return attachment

    ##############################################################################################

    def ChatCommunication(self):
        """Chatを管理する
        
        Parameters:
            - posted_user : ユーザー名
            - posted_text : メッセージ
            - strArry : メッセージを分割した配列
                - strArry[0] : WakeUp Code
                - strArry[1] : Command
                - strArry[2] : Argument
                - strArry[3] : Target
        
        return:
            組み上がったメッセージをMatterControllerに渡す
        
        """
        posted_user = request.json['user_name']
        posted_msg  = request.json['text']

        strArry = posted_msg.split(" ")
        command = strArry[1]

        if command == "hello" or command == "Hello":
            attachment = {"mrkdwn_in": ["text"], "text": f"Hi, @{posted_user} ! :wave:" }
        elif command == "hi" or command == "Hi":
            attachment = {"mrkdwn_in": ["text"], "text": f"Hello, @{posted_user} ! :wave:" }
        elif command == "help":
            attachment = self.help_me()
        elif command == "target":
            attachment = self.targetlist()

        # nmap or nikto
        elif command == "nmap" or command == "nikto" or command == "tools":
            # gather all commands
            sql = """SELECT cmd_name,value FROM t_command_list WHERE cmd_type = %s;"""
            cmdList = self.db.get_AllValues(sql, command)
            cmdNames = []
            cmdValue = ""
            for selectCmd in cmdList:
                cmdName = selectCmd[0]
                cmdNames.append(cmdName)
            if len (strArry) == 3:
                args = strArry[2]
                if args == "help":
                    if command == "nmap" or command == "nikto":
                        attachment = self.cmd_help(posted_user,command)
                    elif command == "tools":
                        attachment = self.tools_help(posted_user)
                    else:
                        attachment = self.cmd_i_dont_know(posted_user,command)
                    
            elif len(strArry) == 4:
                cmdType = strArry[2]
                target = strArry[3]
                for selectCmd in cmdList:
                    cmdName, value = selectCmd
                    if cmdName == cmdType:
                        filename = f"{cmdName}_{target}_" + self.get_timestamp()
                        if command == "nmap" or command == "tools":
                            if self.check_ipaddress(target):
                                # Use Nmap
                                if command == "nmap":
                                    cmdValue = f"{value} {target} -oA tmp/{filename} &&  python xmlparser.py tmp/{filename}.xml"
                                # Use tools
                                elif command == "tools":
                                    # use AutoRecon
                                    if cmdName == "AutoRecon":
                                        cmdValue = f"{value} {target} && python xmlparser.py tmp/{target}/scans/xml"
                            else:
                                attachment = self.ipaddress_error(posted_user,target)
                        elif command == "nikto":
                            cmdValue = f"{value} {target} -o tmp/{filename}.xml | tee tmp/{filename}.txt && python xmlparser.py tmp/{filename}.xml"
                        attachment = {
                            "mrkdwn_in": ["text"],
                            "fallback": f"I'll run a {cmdName} to {target}",
                            "color": "#b79b5b", # 桑染くわぞめ
                            "title": "Your order",
                            "pretext": f"I'll run a {cmdName} to {target}",
                            "text": cmdValue
                        }
                        jc.Set_myjob(cmdValue, posted_user)
                        break
                if cmdValue == "":
                    attachment = self.cmd_help(posted_user,command)
            else:
                attachment = self.cmd_i_dont_know(posted_user,command)
        # Show host information
        elif command == "info":
            if len(strArry) == 3:
                target = strArry[2]
                if target == "help":
                    attachment = self.info_help(posted_user,"help")
                else:
                    if self.check_ipaddress(target):
                        sql = """SELECT id FROM t_host_list WHERE ip_address = %s;"""
                        host_id = self.db.get_SingleValue(sql, target)
                        if host_id is None:
                            attachment = self.info_help(posted_user,"norecord")
                        else:
                            attachment = self.hostinfo(host_id)
                    else:
                        attachment = self.ipaddress_error(posted_user,target)
            else:
                attachment = self.info_help(posted_user,"error")

        # other or help
        else:
            pretext = "I don't konw :man_shrugging:"
            attachment = {
                "markdwn_in": ["text","pretext"],
                "pretext" : pretext,
                "color": "#d0af4c", # 芥子色からしいろ
                "text": "If you have any questions, please type `#pitto help`. :thumbsup:"
            }
        
        return self.mc.botbot_information(attachment)

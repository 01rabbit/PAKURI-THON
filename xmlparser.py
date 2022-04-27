import sys
import xml.etree.ElementTree as ET
import argparse
import db_controller as db
import MatterController as mc
import datetime


def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def parseArgs():
    parser = argparse.ArgumentParser(
        description="XMLParser : Parse Nmap & Nikto XML output and update DB")
    parser.add_argument("scanfile", help="Nmap & Nikto XML output file")
    args = parser.parse_args()
    return args.scanfile

def createTree(scanfile):
    try:
        tree = ET.parse(scanfile)
        root = tree.getroot()
    except ET.ParseError as e:
        print("Parse error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(2)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(2)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(2)
    return root

def parse_nmap_xml(root):
    hosts = root.findall("host")
    for host in hosts:
        # これを元にしてNmapの結果を解析する
        # ホストテーブルに登録する
        # Nmap results are analyzed based on this.
        # The analysis results are registered in a database.
        if not host.findall("status")[0].attrib["state"] == "up":
            continue
        else:
            state="open"
        addr = host.findall("address")[0].attrib["addr"]
        try:
            mac_addr = host.findall("address")[1].attrib["addr"]
        except IndexError:
            mac_addr = None
        print(addr, state)
        host_name_element = host.findall("hostnames")
        try:
            hostname = host_name_element[0].findall("hostname")[0].attrib["name"]
        except IndexError:
            hostname = ""
        try:
            os_element = host.findall("os")
            os_name = os_element[0].findall("osmatch")[0].attrib["name"]
        except IndexError:
            os_name = ""
        time = get_timestamp()

        # ホストテーブルに登録済みなら、ホストテーブルに登録されているホストのIDを取得
        # If already registered in the database, obtain the ID of the registered host.
        sql = """SELECT id FROM t_host_list WHERE ip_address = %s;"""
        host_id=db.get_SingleValue(sql,addr)
        if host_id is not None:
            # DBに登録済み
            sql = """UPDATE t_host_list SET state = %s, timestamp = %s WHERE id = %s;"""
            arg = (state, time, host_id)
            db.update_db(sql, arg)
        else:
            # DBに登録されてないのでIPを登録し、戻り値のIDを格納
            # Register the IP as it is not registered in the database and store the ID in the return value.
            sql = """INSERT INTO t_host_list(ip_address,mac_address,host_name,osname,timestamp) VALUES(%s,%s,%s,%s,%s) RETURNING id;"""
            arg = (addr, mac_addr, hostname, os_name, time)
            host_id = db.insert_db(sql, arg)
            if host_id != "None":
                sql = """UPDATE t_host_list SET state = %s, timestamp = %s WHERE id = %s;"""
                arg = (state, time, host_id)
                db.update_db(sql, arg)

        try:
            port_element = host.findall("ports")
            ports = port_element[0].findall("port")
            for port in ports:
                protocol = port.attrib["protocol"]
                portid = port.attrib["portid"]
                portstate = port.find("state").attrib["state"]
                portservice = port.findall("service")[0].attrib["name"]
                try:
                    product = port.findall("service")[0].attrib["product"]
                except (IndexError, KeyError):
                    product = ""
                try:
                    version = port.findall("service")[0].attrib["version"]
                except (IndexError, KeyError):
                    version = ""
                try:
                    extrainfo = port.findall("service")[0].attrib["extrainfo"]
                except (IndexError, KeyError):
                    extrainfo = ""
                    
                # ポートテーブルに登録する
                # Register in the port list table.
                sql = """SELECT id FROM t_port_list WHERE host_id = """+str(host_id)+""" AND port_num = %s;"""
                port_id=db.get_SingleValue(sql,portid)
                if port_id is not None:
                    # DBに登録済み
                    # Already registered in the database.
                    sql = """UPDATE t_port_list SET protocol=%s, port_num=%s, state=%s, serv_name=%s, serv_prod=%s, serv_ver=%s, extrainfo=%s, timestamp = %s WHERE id = %s;"""
                    arg = (protocol, portid, portstate, portservice, product, version, extrainfo, time, port_id)
                    db.update_db(sql, arg)
                else:
                    # DBに登録されてないのでポートを登録し、戻り値のIDを格納
                    # Register the IP as it is not registered in the database and store the ID in the return value.
                    sql = """INSERT INTO t_port_list(host_id,protocol,port_num,timestamp) VALUES(%s,%s,%s,%s) RETURNING id;"""
                    arg = (host_id, protocol, portid, time)
                    port_id = db.insert_db(sql, arg)
                    if port_id != "None":
                        sql = """UPDATE t_port_list SET state=%s, serv_name=%s, serv_prod=%s, serv_ver=%s, extrainfo=%s, timestamp = %s WHERE id = %s;"""
                        arg = (portstate, portservice, product, version, extrainfo, time, port_id)
                        db.update_db(sql, arg)

                # vulnテーブルに登録
                # Registered in the Vuln table.
                try:
                    servicefp = port.findall("service")[0].attrib["servicefp"]
                except (IndexError, KeyError):
                    servicefp = ""
                script_element = port.findall("script")
                for script in script_element:
                    try:
                        script_id = script.attrib["id"]
                    except (IndexError, KeyError):
                        script_id = ""
                    try:
                        script_output = script.attrib["output"]
                    except (IndexError, KeyError):
                        script_output = ""
                    # PortIDと絡めてVulnテーブルを作成しインポートしていく
                    # 同じものがあるか確認。なければインポート
                    # Create Vuln table with port ID and import data.
                    # Check if there is the same data, and if not, import it.
                    sql = """SELECT id FROM t_vuln_list WHERE port_id = """+str(port_id)+""" AND script_id = %s;"""
                    vuln_id = db.get_SingleValue(sql, script_id)
                    if vuln_id is None:
                        sql = """INSERT INTO t_vuln_list(port_id,script_id,output,timestamp) VALUES(%s,%s,%s,%s) RETURNING id;"""
                        arg = (port_id, script_id, script_output, time)
                        vuln_id = db.insert_db(sql, arg)
        except IndexError:
            continue

def parse_nikto_xml(root):
    details = root.findall("scandetails")
    try:
        targetip = details[0].attrib["targetip"]
    except (IndexError, KeyError):
        targetip = ""
    targethostname = details[0].attrib["targethostname"]
    try:
        targetport = details[0].attrib["targetport"]
    except (IndexError, KeyError):
        targetport = ""
    targetbanner = details[0].attrib["targetbanner"]
    sitename = details[0].attrib["sitename"]
    siteip = details[0].attrib["siteip"]
    time = get_timestamp()
    sql = """SELECT id FROM t_host_list WHERE ip_address = %s;"""
    host_id = db.get_SingleValue(sql, targetip)
    sql = """SELECT id FROM t_port_list WHERE host_id = """ + str(host_id)+""" AND port_num = %s;"""
    port_id = db.get_SingleValue(sql, targetport)

    items = details[0].findall("item")
    for item in items:
        try:
            item_id = item.attrib["id"]
        except (IndexError, KeyError):
            item_id = ""
        osvdbid = item.attrib["osvdbid"]
        osvdblink = item.attrib["osvdblink"]
        method = item.attrib["method"]
        try:
            description = item.findall("description")[0].text
        except (IndexError, KeyError):
            description = ""
        uri = item.findall("uri")[0].text
        namelink = item.findall("namelink")[0].text
        iplink = item.findall("iplink")[0].text
        sql = """SELECT id FROM t_vuln_list WHERE port_id = """+str(port_id)+""" AND script_id = %s;"""
        vuln_id = db.get_SingleValue(sql, item_id)
        if vuln_id is None:
            sql = """INSERT INTO t_vuln_list(port_id,script_id,output,timestamp) VALUES(%s,%s,%s,%s) RETURNING id;"""
            arg = (port_id, item_id, description, time)
            vuln_id = db.insert_db(sql, arg)

if __name__ == "__main__":
    try:
        # scanfile = "test.xml"
        scanfile = parseArgs()
        tree = createTree(scanfile)
        if tree.tag == "nmaprun":
            parse_nmap_xml(tree)
        elif tree.tag == "niktoscan":
            parse_nikto_xml(tree)
        else:
            print("Unknown file format")
            sys.exit(2)
    except:
        sys.exit(2)
    attachment = {
        "mrkdwn_in": ["text"],
        "title": "File imported",
        "text": "Imported filename " + scanfile + "."
    }
    mc.botbot_information(attachment)


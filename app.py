from crypt import methods
import os
import subprocess
import qrcode
import hashlib
from subprocess import PIPE
import JobController as jobcon
import Communicator as com
import empireController as ec
import netifaces as ni
import config
import pkr_Interface as pkr
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'xml','txt'}
COMMANDER = "PAKURI-THON"
CONFIG_FILE= "config.ini"
DBNAME = "postgresql"
WEBSSH = "webssh"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_ip_address():
    nx = [ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
          for iface in ni.interfaces() if ni.AF_INET in ni.ifaddresses(iface)]
    nxx = nx[0] if nx[0] != "127.0.0.1" else nx[1]
    return nxx


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileread(filename):
    with open(filename) as f:
        return f.read()


def process_action(command):
    result = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    return(result.stdout.decode('utf-8').split('\n')[0])


def create_qrcode(message,filename):
    img =qrcode.make(message)
    img.save(filename)


@app.route('/' , methods=['GET'])
def index():
    myip = get_ip_address()
    return render_template('index.html',myip=myip)


@app.route('/import', methods=['GET','POST'])
def fileimport():
    jc = jobcon.JobController()
    if request.method == 'POST':
        if 'uploadFile' not in request.files:
            return redirect(request.url)
        file = request.files['uploadFile']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # t_job_listにXMLファイルを読み込むJobを登録する
            command = "python xmlparser.py " + \
                os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # process_action(command)
            jc.Set_myjob(command, COMMANDER, "")
            return redirect(url_for('index'))
    return render_template('import.html')

@app.route('/recon_menu', methods=['GET'])
def recon_menu():
    ip = request.args.get('ip', '')
    return render_template('recon_menu.html', ip=ip)


@app.route('/scan_nmap', methods=['GET','POST'])
def scan_nmap():
    db = pkr.db_controller()
    jc = jobcon.JobController()
    if request.method == 'POST':
        command = request.form.get('setCommand')
        filename = f"{request.form.get('setFilename')}.xml"
        command = f"{command} && python xmlparser.py {app.config['UPLOAD_FOLDER']}/{filename}"
        jc.Set_myjob(command, COMMANDER, "")
        return redirect(url_for('scan_nmap'))
    else:
        hosts = db.get_AllValues("""SELECT ip_address FROM t_host_list;""", "")
        ip = request.args.get('ip', '')
        myip = get_ip_address()
        sql = """SELECT * FROM t_command_list WHERE cmd_type = %s;"""
        nmap_list = db.get_AllValues(sql, "nmap")
        if request.args.get('setip') == 'Set':
            return redirect(url_for('scan_nmap', ip=ip))
        return render_template('scan_nmap.html', hosts=hosts, commands=nmap_list, ip=ip, myip=myip)


@app.route('/scan_nikto', methods=['GET', 'POST'])
def scan_nikto():
    db = pkr.db_controller()
    jc = jobcon.JobController()
    if request.method == 'POST':
        command = request.form.get('setCommand')
        filename = request.form.get('setFilename')
        command = f"{command} && python xmlparser.py tmp/{filename}"
        jc.Set_myjob(command, COMMANDER, "")
        return redirect(url_for('scan_nikto'))
    else:
        hosts = db.get_AllValues("""SELECT ip_address FROM t_host_list;""", "")
        ip = request.args.get('ip', '')
        myip = get_ip_address()
        sql = """SELECT * FROM t_command_list WHERE cmd_type = %s;"""
        nikto_list = db.get_AllValues(sql, "nikto")
        if request.args.get('setip') == 'Set':
            return redirect(url_for('scan', ip=ip))
        return render_template('scan_nikto.html', hosts=hosts, scan_nikto=nikto_list, commands=nikto_list, ip=ip, myip=myip)

@app.route('/build_command', methods=['POST'])
def build_command():
    command = request.form.get('setCommand')
    filename = request.form.get('setFilename')
    detail = request.form.get('setDetail')
    hs = hashlib.md5(command.encode()).hexdigest()
    qr_img = f"static/images/qrcode/{hs}.png"
    create_qrcode(command,qr_img)
    return render_template('build_command.html', command=command,filename=filename,detail=detail,qr_img=qr_img)

@app.route('/hostlist', methods=['GET'])
def hostlist():
    db = pkr.db_controller()
    sql = """SELECT * FROM t_host_list;"""
    hosts = db.get_AllValues(sql, "")
    sql = """
            SELECT h.ip_address ,p.protocol ,p.port_num ,p.serv_name ,p.serv_prod ,p.serv_ver ,v.script_id 
            FROM t_port_list p
                inner join t_host_list h
                    on h.id = p.host_id 
                inner join t_vuln_list v
                    on p.id = v.port_id;
        """
    vlist = db.get_AllValues(sql, "")
    return render_template('hostlist.html', hosts=hosts, vlist=vlist)


@app.route('/hostdetail/<int:id>', methods=['GET', 'POST'])
def hostdetail(id):
    db = pkr.db_controller()
    if request.method == 'POST':
        ostype = str(request.form.get("ostype"))
        name = request.form.get("name")
        sql = """UPDATE t_host_list SET ostype = %s, host_name = %s WHERE id = %s;"""
        arg = (ostype, name, id)
        db.update_db(sql, arg)
        return redirect(url_for('hostdetail', id=id))
    else:
        sql = """SELECT * FROM t_port_list WHERE host_id = %s;"""
        ports = db.get_AllValues(sql,id)
        sql = """SELECT * FROM t_host_list WHERE id = %s;"""
        host = db.get_AllValues(sql,id)
        return render_template('hostdetail.html', ports=ports, host_id=id, host=host[0])

@app.route('/portdetail/<int:id>', methods=['GET', 'POST'])
def portdetail(id):
    db = pkr.db_controller()
    sql = """SELECT * FROM t_port_list WHERE id = %s;"""
    ports = db.get_AllValues(sql, id)
    
    sql = """SELECT * FROM t_vuln_list WHERE port_id =%s;"""
    vulns = db.get_AllValues(sql, id)
    return render_template('portdetail.html', ports=ports[0], vulns=vulns)

@app.route('/docker')
def docker():
    cmd = "docker-compose -f docker/webssh/docker-compose.yml ps|grep Up|wc -l"
    webssh_flg = process_action(cmd)
    cmd = "docker-compose -f docker/mattermost-docker/docker-compose.yml ps|grep Up|wc -l"
    mattermost_flg = process_action(cmd)
    return render_template('docker.html',webssh=webssh_flg,mattermost=mattermost_flg)

@app.route('/docker/webssh')
def docker_webssh():
    cmd = "docker-compose -f docker/webssh/docker-compose.yml ps|grep Up|wc -l"
    flg = process_action(cmd)
    # 1: Up, 0: Down
    if flg == "1":
        cmd = "docker-compose -f docker/webssh/docker-compose.yml stop"
        process_action(cmd)
    else:
        cmd = "docker-compose -f docker/webssh/docker-compose.yml start"
        process_action(cmd)
    return redirect(url_for('docker'))

@app.route('/docker/mattermost')
def docker_mattermost():
    cmd = "docker-compose -f docker/mattermost-docker/docker-compose.yml ps|grep Up|wc -l"
    flg = process_action(cmd)
    # 3: Up, 0: Down
    if flg == "3":
        cmd = "docker-compose -f docker/mattermost-docker/docker-compose.yml stop"
        process_action(cmd)
    else:
        cmd = "docker-compose -f docker/mattermost-docker/docker-compose.yml start"
        process_action(cmd)
    return redirect(url_for('docker'))


@app.route('/terminal')
def terminal():
    myip = get_ip_address()
    cmd = "wssh --version|wc -l"
    console_flg = process_action(cmd)
    params = config.webssh_conf()
    return render_template('terminal.html', myip=myip, console_flg=console_flg,username=params['username'],password=params['password'])

@app.route('/task')
def task():
    db = pkr.db_controller()
    sql = """SELECT * FROM t_job_list;"""
    jobs = db.get_AllValues(sql, "")
    return render_template('task.html', jobs=jobs)

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/empire_home',methods=['GET','POST'])
def empire_home():
    empire = ec.EmpireController()
    if request.method == 'POST':
        token = request.form.get('token')
        return redirect(url_for('empire_home', token=token))
    else:
        token = empire.getEmpireToken()
        agents = empire.getCurrentAgents(token)
        if agents[0][0] == '' and len(agents) == 1:
            i = 0
        else:
            i = len(agents)
        if token == '':
            return render_template(url_for('empire_home'))
        else:
            stagers = empire.getAllStager(token)
            listeners = empire.getCurrentListeners(token)
            if listeners[0][0] == '':
                flg = empire.createHTTPListener(token)
                if flg:
                    listeners = empire.getCurrentListeners(token)
                else:
                    listeners = ['','']
            return render_template('empire_home.html', token=token, stagers=stagers, listeners=listeners[0], i=i)

@app.route('/empire_stager',methods=['POST'])
def empire_stager():
    empire = ec.EmpireController()
    token = empire.getEmpireToken()
    stagers = request.form.get('setStager')
    listener = request.form.get('setListener')
    createStagers = empire.generateStager(token,stagers)
    output = createStagers[0][0]
    description = createStagers[0][1]
    return render_template('empire_stager.html', listener=listener, stagers=stagers, output=output, description=description)

@app.route('/empire_agent')
def empire_agent():
    empire = ec.EmpireController()
    token = empire.getEmpireToken()
    agents = empire.getCurrentAgents(token)
    if agents[0][0] == '':
        i = 0
    else:
        i = len(agents)
    return render_template('empire_agent.html', agents=agents, i=i)


@app.route('/bot', methods=['POST'])
def bot_replay():
    comm = com.Communicator()
    comm.ChatCommunication()
    return

@app.route('/qr_reader', methods=['POST','GET'])
def qr_reader():
    db = pkr.db_controller()
    jc = jobcon.JobController()
    if request.method == 'POST':
        command = request.form.get('setCommand')
        # jc.Set_myjob(command, COMMANDER, "")
        return redirect(url_for('recon_menu'))
    else:
        return render_template('qr_reader.html')

@app.route('/kali_tools', methods=['POST','GET'])
def kali_tools():
    return render_template('kali_tools.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5555)

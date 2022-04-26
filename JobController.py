import time
import subprocess
import db_controller as db
import ChatController as cc
import Communicator as comm
import MatterController as mc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def Get_myJobList():
    sql = """SELECT id,command,commander,token FROM t_job_list WHERE status=%s;"""
    joblist = db.get_AllValues(sql, "waiting")
    if len(joblist) != 0:
        Run_myjob(joblist)

def Set_myjob(command, commander):
    sql = """INSERT INTO t_job_list(command,commander,status,timestamp) VALUES(%s,%s,%s,%s) RETURNING id;"""
    status = "waiting"
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arg = (command, commander, status, time)
    job_id = db.insert_db(sql, arg)
    msg = "[+] Adding: ID:{}  Commander:{}  Command:{}".format(job_id, commander, command)
    mc.botbot_information(commander, msg)

def Run_command(job):
    job_id, command, commander, token = job
    sql = """UPDATE t_job_list SET status=%s, timestamp=%s WHERE id= %s;"""
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = ("running", time, job_id)
    db.update_db(sql, args)
    p = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err, job_id, command, commander, token

def Run_myjob(joblist):
    executer = ThreadPoolExecutor(max_workers=3)
    futures = []

    for job in joblist:
        job_id, command, commander, token = job
        msg = "[+] Running: ID:{}  Commander:{}  Command:{}".format(job_id, commander, command)
        # chat message send
        cc.NextcloudTalkSendInformation(msg)
        print(msg)
        time.sleep(1)
        future = executer.submit(Run_command, job)
        futures.append(future)

    while True:
        if len(futures) == 0:
            break
        else:
            for future in futures:
                if future.done():
                    out, err, job_id, command, commander, token = future.result()
                    print("[+] Done: Job_ID: {}".format(job_id))
                    if len(out) != 0:
                        print("[+] Output: {}".format(out))
                    if len(err) != 0:
                        print("[+] Error: {}".format(err))
                    print("[+] Done: Commander:{}  Command: {}".format(commander, command))
                    cc.NextcloudTalkSendInformation("[+] Done: Job_ID: {}".format(job_id))
                    cc.NextcloudTalkSendInformation("[+] Done: Commander:{}  Command: {}".format(commander, command))
                    comm.ChatSendMessage(token, commander, "Done: Job_ID: {} Command: {}".format(job_id, command))
                    sql = """UPDATE t_job_list SET status=%s, timestamp=%s WHERE id= %s;"""
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    args = ("done", timestamp, job_id)
                    db.update_db(sql, args)
                    futures.remove(future)
        time.sleep(25)

    executer.shutdown()

if __name__ == "__main__":
    while True:
        Get_myJobList()
        time.sleep(1) # sleep 1 sec short?

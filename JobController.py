import time
import subprocess
import pkr_Interface
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class JobController:
    def __init__(self):
        self.db = pkr_Interface.db_controller()
        self.mc = pkr_Interface.matter_controller()
        
    def Get_myJobList(self):
        sql = """SELECT id,command,commander,token FROM t_job_list WHERE status=%s;"""
        joblist = self.db.get_AllValues(sql, "waiting")
        if len(joblist) != 0:
            self.Run_myjob(joblist)

    def Set_myjob(self, command, commander):
        sql = """INSERT INTO t_job_list(command,commander,status,timestamp) VALUES(%s,%s,%s,%s) RETURNING id;"""
        status = "waiting"
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        arg = (command, commander, status, time)
        job_id = self.db.insert_db(sql, arg)
        attachment = {
            "mrkdwn_in": ["text"],
            "title": "Added order JobID:{}".format(job_id),
            "pretext": "I added your order",
            "text": f"@{commander} Your order is accepted.\n" + " JobID:{}\n Command:{}".format(job_id, command)
        }
        self.mc.botbot_information(attachment)

    def Run_command(self, job):
        job_id, command, commander, token = job
        sql = """UPDATE t_job_list SET status=%s, timestamp=%s WHERE id= %s;"""
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args = ("running", time, job_id)
        self.db.update_db(sql, args)
        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out, err, job_id, command, commander, token

    def Run_myjob(self,joblist):
        executer = ThreadPoolExecutor(max_workers=3)
        futures = []

        for job in joblist:
            job_id, command, commander, token = job
            # chat message send
            attachment = {
                "mrkdwn_in": ["text"],
                "fallback": f"@{commander} Processing start.",
                "title": "Start JobID:{}".format(job_id),
                "pretext": "Processing began as ordered.",
                "text": f"@{commander} Ordered processing has been started.\n" + " JobID:{}\n Command:{}".format(job_id, command)
            }
            self.mc.botbot_information(attachment)
            time.sleep(1)
            future = executer.submit(self.Run_command, job)
            futures.append(future)

        while True:
            if len(futures) == 0:
                break
            else:
                for future in futures:
                    if future.done():
                        out, err, job_id, command, commander, token = future.result()
                        if len(out) != 0:
                            attachment = {
                                "mrkdwn_in": ["text"],
                                "fallback": f"@{commander} Done.",
                                "title": f"Done. JobID:{job_id}",
                                "pretext": "Process is finished.",
                                "text": f"@{commander} The process was successfully completed.\n" + \
                                    " JobID:{}\n Command:{}".format(job_id, command) + \
                                    "\n\n" + out.decode("utf-8")
                            }
                        elif len(err) != 0:
                            attachment = {
                                "mrkdwn_in": ["text"],
                                "fallback": f"@{commander} Error. JobID:{job_id}",
                                "title": f"Error. JobID:{job_id}",
                                "pretext": "Processing has failed.",
                                "text": f"@{commander} The process was failed.\n" + \
                                    " JobID:{}\n Command:{}".format(job_id, command) + \
                                    "\n\n" + err.decode("utf-8")
                            }
                        self.mc.botbot_information(attachment)
                        sql = """UPDATE t_job_list SET status=%s, timestamp=%s WHERE id= %s;"""
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        args = ("done", timestamp, job_id)
                        self.db.update_db(sql, args)
                        futures.remove(future)
            time.sleep(25)

        executer.shutdown()

# if __name__ == "__main__":
#     while True:
#         Get_myJobList()
#         time.sleep(1) # sleep 1 sec short?

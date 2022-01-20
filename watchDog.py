import datetime
import sys
import time
from threading import Thread
import db_controller as db
import ChatController  as cc
import Communicator as comm
import JobController as jc


if __name__ == "__main__":
    try:
        while True:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # ----Job Check and Run----
            thread_job = Thread(target=jc.Get_myJobList)
            thread_job.start()
            # ----NextCloud Chat----
            # Get Chat Messages
            tokenArry = cc.NextcloudTalkGetRoomToken()
            # print(tokenArry)
            cc.NextcloudTalkGetReceivedmessage(tokenArry)
            # Check Messages
            sql = """SELECT id,token,actor,message FROM t_message_list WHERE response = %s;"""
            messages = db.get_AllValues(sql, "0")
            for message in messages:
                id = message[0]
                token = message[1]
                actor = message[2]
                msg = message[3]
                receivedMsg = (id, token, actor, msg)
                comm.ChatCommunication(receivedMsg)
            time.sleep(10)

    except(KeyboardInterrupt):
        print("finishing..")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)

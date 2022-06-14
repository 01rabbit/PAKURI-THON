import datetime
import sys
import time
from threading import Thread
import JobController as jc


if __name__ == "__main__":
    jc = jc.JobController()
    try:
        while True:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # ----Job Check and Run----
            thread_job = Thread(target=jc.Get_myJobList)
            thread_job.start()
            time.sleep(10)

    except(KeyboardInterrupt):
        print("finishing..")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)

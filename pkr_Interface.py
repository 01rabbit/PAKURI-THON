import psycopg2
import sys
import slackweb
import config


class db_controller:
    def __init__(self):
        params = config.db_conf()
        self.conn = None
        try:
            self.conn = psycopg2.connect(**params)
        except psycopg2.OperationalError:
            sys.exit('Database not found')
        self.cur = self.conn.cursor()

    def insert_db(self, sql, arg):
        try:
            self.cur.execute(sql,(arg))
            value = self.cur.fetchone()[0]
            self.conn.commit()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            # print("insert_db :"+error)
            pass
        finally:
            if self.conn is not None:
                self.conn.close()
        return value

    def update_db(self,sql,arg):
        try:
            self.cur.execute(sql,(arg))
            self.conn.commit()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            # print("update_db :"+error)
            pass
        finally:
            if self.conn is not None:
                self.conn.close()

    def get_SingleValue(self,sql,arg):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql,(arg,))
            value = self.cur.fetchone()[0]
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            # print("get_SingleValue dberror:"+error)
            pass
        finally:
            if self.conn is not None:
                self.conn.close()
        return value

    def get_AllValues(self,sql,arg):
        value = []
        try:
            self.cur.execute(sql,(arg,))
            value = self.cur.fetchall()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            # print("get_AllValues :"+error)
            pass
        finally:
            if self.conn is not None:
                self.conn.close()
        return value

class matter_controller:
    def __init__(self):
        params = config.matter_conf()
        self.attachments = []
        self.mattermost = slackweb.Slack(url=params['webhooks'])

    def botbot_information(self,attachment):
        self.attachments.append(attachment)
        self.mattermost.notify(text="", attachments=self.attachments)



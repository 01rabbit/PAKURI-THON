import psycopg2
import os
import configparser
import sys
from config import db_conf as config


class db_controller:
    def __init__(self):
        # Read config.ini
        path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        try:
            config.read(os.path.join(path, 'config.ini'))
        except FileExistsError:
            sys.exit('config.ini not found')
        
        DB_HOST = config['postgresql']['host']
        DB_PORT = int(config['postgresql']['port'])
        DB_USER = config['postgresql']['user']
        DB_PASS = config['postgresql']['password']
        DB_NAME = config['postgresql']['database']
        self.conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME)
        
def insert_db(sql,arg):
    conn = None
    value = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(arg))
        value = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # print("insert_db :"+error)
        pass
    finally:
        if conn is not None:
            conn.close()
    return value

def update_db(sql,arg):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(arg))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # print("update_db :"+error)
        pass
    finally:
        if conn is not None:
            conn.close()

def get_SingleValue(sql,arg):
    conn = None
    value = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(arg,))
        value = cur.fetchone()[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # print("get_SingleValue dberror:"+error)
        pass
    finally:
        if conn is not None:
            conn.close()
    return value

def get_AllValues(sql,arg):
    conn = None
    value = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(arg,))
        value = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        # print("get_AllValues :"+error)
        pass
    finally:
        if conn is not None:
            conn.close()
    return value

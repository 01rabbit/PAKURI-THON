import psycopg2
from config import db_conf as config


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

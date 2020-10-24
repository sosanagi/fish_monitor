import sqlite3
import time
import json

f = open("module.json", "r")
module = json.load(f)
sql_list = module["sql"]

DB="fish.db"

def create():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(sql_list["cre_ftime"])

    c.execute(sql_list["ins_ftime"],(time.time(),))
    c.execute(sql_list["ins_ftime"],(time.time(),))
    c.execute(sql_list["ins_ftime"],(time.time(),))

    conn.commit()

    conn.close()

def select_one():
    ftime=1577804400.0

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for row in c.execute(sql_list["slt_once_ftime"]):
        ftime=row[0]

    conn.close()

    return ftime

def select():
    ut = time.time() - 86400 #24*60*60
    data = []

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for row in c.execute(sql_list["slt_img_ftime"],(str(ut),)):
        ftime=row[0]
        data.append(ftime)

    conn.close()

    return data

def insert(time_str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(sql_list["ins_ftime"],(time_str,))

    conn.commit()
    conn.close()

def delete():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(sql_list["del_one_time"])

    conn.commit()
    conn.close()

#create()
#insert(time.time())
#ftime=select()
#print(ftime)

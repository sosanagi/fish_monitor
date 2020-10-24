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

    c.execute(sql_list["cre_temp"])

    c.execute(sql_list["ins_temp"],(23.6,time.time(),))
    c.execute(sql_list["ins_temp"],(24.6,time.time(),))
    c.execute(sql_list["ins_temp"],(23.4,time.time(),))

    conn.commit()

    conn.close()

def select_one():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for row in c.execute(sql_list["slt_one_temp"]):
        w_temp=row[0]
        wt_time=row[1]

    conn.close()
    return w_temp,wt_time

def select():
    ut = time.time() - 86400 #24*60*60
    data = []

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for row in c.execute(sql_list["slt_img_temp"],(str(ut),)):
        w_temp=row[0]
        wt_time=row[1]
        data.append((w_temp,wt_time))

    conn.close()

    return data


def insert(temp_f,time_f):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(sql_list["ins_temp"],(temp_f,time_f),)

    conn.commit()
    conn.close()

def delete():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(sql_list["del_one_temp"])

    conn.commit()
    conn.close()



#create()
#insert(38.6,time.time())
#data=select()
#print(data)
#delete()
#select()

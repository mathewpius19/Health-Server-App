import sqlite3
from flask import Flask
from flask import request
import json
import time

app=Flask(__name__)
@app.route("/Health",methods=['POST'])
def health():
    object=request.json
    username=object["Username"]
    password=object["Password"]
    conn=sqlite3.connect("Health.db")
    try:
        if password=="NULL" or not password or password.isspace():
            raise Exception
    except Exception:
        print("Password cannot be NULL")
    else:       
       
        conn.execute("create table if not exists 'user'(UID integer primary key AUTOINCREMENT,username varchar(20),password varchar(20));")
        conn.execute("insert into user(username,password) values(?,?)",(username,password))
    finally:
        conn.commit()
        return "yes"
@app.route("/login",methods=['POST']) 
def login():
    object=request.json
    username=object["Username"]
    conn=sqlite3.connect("Health.db")
    cur=conn.cursor()
    cur.execute("select exists(select username from user where username=(?))",(username,))
    for row in cur:
        rowlist=list(row)
        try:
            if rowlist[0]==0:
                raise Exception
        except Exception:
                    print("Username does not exist,Please create User and Continue")
        else:   
            conn.execute(f"create table if not exists {username} (IP_ID integer primary key AUTOINCREMENT,IP_Address varchar(20),Private_Key varchar(80));")
        finally:
            conn.commit()
            return "yes"


@app.route("/Server",methods=['POST'])
def server():
    object=request.json
    username=object["Username"]
    ip_address=object["IP Address"]
    priv_key=object["Private Key"]
    newip=ip_address.replace('.','_')
    newip="ip:"+newip
    conn=sqlite3.connect("Health.db")
    try:
        if priv_key=="NULL" or  not priv_key or priv_key.isspace():
            raise Exception
    except Exception:
            print("Private Key cannot be NULL")
    else:
        conn.execute(f'insert into {username} (IP_Address,Private_Key) values {ip_address,priv_key}')
        
    finally:
        conn.commit()
        return "yes"



@app.route("/report",methods=['POST'])
def report():
    time_epoch=time.time()
    incoming_report = request.get_json()
    print("Generating Health report")
    server_name=incoming_report["SERVER_NAME"]
    disk_free=incoming_report["free_Percnt"]
    bytes_sent=incoming_report["bytes_sent"]
    bytes_received=incoming_report["bytes_received"]
    packets_sent=incoming_report["packets_sent"]
    packets_received=incoming_report["packets_received"]
    memory_free=incoming_report["memory_Free"]
    cpu_percent=incoming_report["cpupercent"]
    cpu_total=incoming_report["cpu_total"]
    conn=sqlite3.connect("Health.db")
    conn.execute(f"create table if not exists {server_name} (HEALTH_ID integer primary key AUTOINCREMENT,Time_Epoch integer,Disk_Free varchar(80),Bytes_Sent varchar(80),Bytes_Received varchar(80),Packets_Sent varchar(80),Packets_Received varchar(80),Memory_Free varchar(80),Cpu_Usage_Percent varchar(80),Cpu_Time varchar(80));")
    conn.execute(f'insert into {server_name} (Time_Epoch,Disk_Free,Bytes_Sent,Bytes_Received,Packets_Sent,Packets_Received,Memory_Free,Cpu_Usage_Percent,Cpu_Time) values {time_epoch,disk_free,bytes_sent,bytes_received,packets_sent,packets_received,memory_free,cpu_percent,cpu_total}')
    conn.commit()
    return {'message': 'success'}


if __name__ ==("__main__"):
    app.run(debug=True,port=8080)

import sqlite3
from flask import Flask,redirect,url_for
from flask import request
import json
import sys
import Health as Hel

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
    except Exception as e:
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
    conn=sqlite3.connect("Health.db")
    try:
        if priv_key=="NULL" or  not priv_key or priv_key.isspace():
            raise Exception
    except Exception:
            print("Private Key cannot be NULL")
    else:
        conn.execute(f'insert into {username} (IP_Address,Private_Key) values {ip_address,priv_key}')
        conn.execute(f"create table if not exists {ip_address} (HEALTH_ID integer primary key AUTOINCREMENT,Disk_Free varchar(80),Bytes_Sent varchar(80),Bytes_Received varchar(80),Packets_Sent varchar(80),Packets_Received varchar(80),Memory_Free varchar(80),Cpu_Usage_Percent varchar(80),Cpu_Time varchar(80));")
        Cpu_Usage_Percent=Hel.cpupercent
        Cpu_Time=Hel.cpu_total
        Disk_Free=Hel.free_Percnt
        Bytes_Sent=Hel.bytes_sent
        Bytes_Received=Hel.bytes_received
        Packets_Sent=Hel.packets_sent
        Packets_Received=Hel.packets_received
        Memory_Free=Hel.memory_Free
        conn.execute(f'insert into {ip_address} (Disk_Free,Bytes_Sent,Bytes_Received,Packets_Sent,Packets_Received,Memory_Free,Cpu_Usage_Percent,Cpu_Time) values {Disk_Free,Bytes_Sent,Bytes_Received,Packets_Sent,Packets_Received,Memory_Free,Cpu_Usage_Percent,Cpu_Time}')
    finally:
        conn.commit()
        print(len(priv_key))
        return "yes"
       


   

if __name__ ==("__main__"):
    app.run(debug=True)

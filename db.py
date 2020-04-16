import sqlite3
from flask import Flask
from flask import request
import json
import time
import os
app=Flask(__name__)
@app.route("/Registration",methods=['POST'])
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
            conn.execute(f"create table if not exists {username}_servers (IP_ID integer primary key AUTOINCREMENT,IP_Address varchar(20),Private_Key varchar(500),Server_Name varchar(80));")
        finally:
            conn.commit()
            return "yes"


@app.route("/Server",methods=['POST'])
def server():
    object=request.json
    username=object["Username"]
    ip_address=object["IP Address"]
    priv_key=object["Private Key"]
    server_name=object["Server Name"]
    conn=sqlite3.connect("Health.db")
    try:
        if priv_key=="NULL" or  not priv_key or priv_key.isspace():
            raise Exception
    except Exception:
            print("Private Key cannot be NULL")
    else:
        conn.execute(f'insert into {username}_servers (IP_Address,Private_Key,Server_Name) values {ip_address,priv_key,server_name}')
        cur=conn.cursor()
        cur.execute(f"select Private_Key from mathew_servers where IP_Address='52.14.13.8'")
        for row in cur:
            with open("key.pem","w+") as key:
                key.write(row[0])
            firstline="-----BEGIN RSA PRIVATE KEY-----\n"
            lastline="-----END RSA PRIVATE KEY-----"
            with open("key.pem","r") as key:
                oline=key.readlines()
                oline.insert(0,firstline)
        
            with open("key.pem","w") as key:
                key.writelines(oline)
            with open("key.pem","a") as key:
                key.write("\n"+lastline)
    
    
        os.system(f"ssh ubuntu@{ip_address} -i key.pem")
        os.system('git clone https://github.com/mathewpius19/Health-Server-App.git ')
        os.system("cd Health-Server-App")
        os.system('chmod 777 requirements.sh')
        os.system('./requirements.sh')
        os.system("chmod 777 report.py")
        os.system("python3 report.py")
    finally:
        conn.commit()
        return "yes"



@app.route("/report",methods=['GET','POST'])
def report():

        if request.method=='POST':
            
            time_epoch=time.time()
            incoming_report = request.get_json()
            print("Generating Health report")
            username=incoming_report["USER_NAME"]
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
            conn.execute(f"create table if not exists {username}_{server_name} (HEALTH_ID integer primary key AUTOINCREMENT,Time_Epoch integer,Disk_Free varchar(80),Bytes_Sent varchar(80),Bytes_Received varchar(80),Packets_Sent varchar(80),Packets_Received varchar(80),Memory_Free varchar(80),Cpu_Usage_Percent varchar(80),Cpu_Time varchar(80));")
            conn.execute(f'insert into {username}_{server_name} (Time_Epoch,Disk_Free,Bytes_Sent,Bytes_Received,Packets_Sent,Packets_Received,Memory_Free,Cpu_Usage_Percent,Cpu_Time) values {time_epoch,disk_free,bytes_sent,bytes_received,packets_sent,packets_received,memory_free,cpu_percent,cpu_total}')
            conn.commit()
            return "yes"

        if request.method=='GET':
            servername=input("Enter the server you want to display")
            conn=sqlite3.connect("Health.db")    
            cur=conn.cursor()  
            details=input("Do you want all,last 5 or first 5?")
            try:
                if details=="NULL" or  not details or details.isspace() or not (details=='all' or details=='last 5' or details== 'first 5'):
                    raise Exception
            except Exception:
                print("Invalid input")
            else:
                if details=='all':
                    cur.execute(f" select * from {servername} order by HEALTH_ID")
                elif (details=='last 5'):
                   cur.execute(f" select * from {servername} order by HEALTH_ID desc limit 5")
                else:
                    cur.execute(f" select * from {servername} order by HEALTH_ID asc limit 5")

    
                for row in cur:
                    tuple1=row
                    tuple2=('Health_id','Epoch_Time','Disk_Free','Bytes_Sent','Bytes_Received','Packets_Sent','Packets_Received','Memory_Free','CPU_Usage_Percent','CPU_Time')
                    health_dict=dict(zip(tuple2,tuple1))
                    
            finally:    
                conn.commit()
                return {health_dict}


if __name__ ==("__main__"):
    app.run(host='0.0.0.0',port=80)

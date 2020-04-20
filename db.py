import sqlite3
from flask import Flask,render_template
from flask import request
import json
import time
app=Flask(__name__)

@app.route("/index",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/Registration",methods=['POST'])
def Regist_post():
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

@app.route("/Registration",methods=['GET'])
def Regist_get():
    return render_template("Registration.html")



@app.route("/login",methods=['POST']) 
def login_post():
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
            conn.execute(f"create table if not exists {username}_servers (IP_ID integer primary key AUTOINCREMENT,IP_Address varchar(20),Server_Name varchar(80));")
        finally:
            conn.commit()
            return "yes"
@app.route("/login",methods=['GET'])
def login_get():
    return render_template("Login.html")


@app.route("/Add_Server",methods=['POST'])
def add_server_post():
    object=request.json
    username=object["Username"]
    ip_address=object["IP Address"]
    server_name=object["Server Name"]
    conn=sqlite3.connect("Health.db")
    try:
        if server_name=="NULL" or  not server_name or server_name.isspace():
            raise Exception
    except Exception:
            print("Server Name cannot be NULL")
    else:
        conn.execute(f'insert into {username}_servers (IP_Address,Server_Name) values {ip_address,server_name}')
       
    finally:
        conn.commit()
        return "yes"
@app.route("/Remove_Server",methods=['POST'])
def remove_server():
    object=request.json
    username=object["Username"]
    servername=object["Server Name"]
    conn=sqlite3.connect("Health.db")
    conn.execute(f'drop table {username}_{servername}')
    conn.execute(f'delete from {username}_servers where server_name=(?)',(servername,))
    conn.commit()
    return 'yes'
@app.route("/Add_Server",methods=['GET'])
def add_server_get():
    return render_template("Server.html")

@app.route("/report",methods=['POST'])
def report():
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

@app.route("/Display/<servername>/<details>",methods=['GET'])
def display(servername,details):
    conn=sqlite3.connect("Health.db")    
    cur=conn.cursor()  
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


        health_dict={'Health_id':[],'Epoch_Time':[],'Disk_Free':[],'Bytes_Sent':[],'Bytes_Received':[],'Packets_Sent':[],'Packets_Received':[],'Memory_Free':[],'CPU_Usage_Percent':[],'CPU_Time':[]}
        for row in cur:
            health_dict['Health_id'].append(row[0])
            health_dict['Epoch_Time'].append(row[1])
            health_dict['Disk_Free'].append(row[2])
            health_dict['Bytes_Sent'].append(row[3])
            health_dict['Bytes_Received'].append(row[4])
            health_dict['Packets_Sent'].append(row[5])
            health_dict['Packets_Received'].append(row[6])
            health_dict['Memory_Free'].append(row[7])
            health_dict['CPU_Usage_Percent'].append(row[8])
            health_dict['CPU_Time'].append(row[9])
        return (health_dict)
    finally:
        conn.commit()

        


if __name__ ==("__main__"):
    app.run(host='0.0.0.0',debug=True,port=80)

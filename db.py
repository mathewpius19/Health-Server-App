import sqlite3
from flask import Flask
from flask import request
import json
import sys

app=Flask(__name__)
@app.route("/Health",methods=['POST'])
def health():
    object=request.json
    username=object["Username"]
    password=object["Password"]
    if password=="NULL" or not password:
        print("Password cannot be NULL")
        sys.exit()
    conn=sqlite3.connect("Health.db")
    conn.execute("create table user(username varchar(20),Password varchar(20));")
    conn.execute("insert into user values(?,?)",(username,password))
    conn.commit()
    return "yes"
@app.route("/Health/login",methods=['POST'])
def login():
    object=request.json
    username=object["Username"]
    conn=sqlite3.connect("Health.db")
    cur=conn.cursor()
    cur.execute("select exists(select username from user where username=(?))",(username,))
    for row in cur:
        if len(list(row))==0:
            print("Username does not exist")
            sys.exit()
    conn.commit()
    return "yes"
   

if __name__ ==("__main__"):
    app.run(debug=True)

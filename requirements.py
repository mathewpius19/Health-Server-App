import sys
import os
os.system("sudo apt install python3-pip")
os.system("pip3 install psutil")
os.system("pip3 install Flask")
servername=input("Enter server name \n")
username=input("Enter user name \n")
os.system(f"python3 report.py {servername} {username} ")





import sys
import os
#os.system("sudo apt install python3-pip")
#os.system("pip install psutil")
#os.system("pip install Flask")
servername=input("Enter server name \n")
username=input("Enter user name \n")
os.system(f"python report.py {servername} {username} ")





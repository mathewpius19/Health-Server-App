import psutil
import time
import json
'''
This program will be loaded on to the target server.
A flask app will transmit health data to the main flask app.
'''
SERVER_NAME="test_local_server"
def getHealth(): # function for generatig health report. Returns a json object.
    print('generating health report')
    report={}
    report['sever_name']=SERVER_NAME
    report['cpupercent']=psutil.cpu_percent(interval=2.0)
    report['ctime']=psutil.cpu_times()
    report['cpu_total']=report['ctime'].user+report['ctime'].system    
    report['disk_usage']=psutil.disk_usage("/")
    report['free_Percnt']=(report['disk_usage'].free/report['disk_usage '].used)/100
    report['net']=psutil.net_io_counters()
    report['bytes_sent']=report['net'].bytes_sent
    report['bytes_received']=report['net'].bytes_recv
    report['packets_sent']=report['net'].packets_sent
    report['packets_received']=report['net'].packets_recv
    report['mem']=psutil.virtual_memory()
    report['memory_Free']=report['mem'].free
    json_report=json.dumps(report)
    print(json_report)
    time.sleep(10)

if __name__=='__main__':
    print(f'starting health report stream for server :\t{SERVER_NAME}')
    while True:
        getHealth()

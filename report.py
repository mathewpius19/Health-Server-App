import psutil
import requests
import time
import sys

STATS_URL = ' http://3.134.78.37:80/report'

try:
    if len(sys.argv)<1:
        raise Exception
except Exception:
        print("Invalid Entry")

else:   
        SERVER_NAME=sys.argv[1]
        USER_NAME=sys.argv[2]
        print(SERVER_NAME,USER_NAME)

        def get_health(): 

            print('generating health report')

            cpu_percent = psutil.cpu_percent(interval=2.0)
            ctime = psutil.cpu_times()
            disk_usage = psutil.disk_usage("/")
            net_io_counters = psutil.net_io_counters()
            virtual_memory = psutil.virtual_memory()    

            # The keys in this dict should match the db cols
            report = dict (
                USER_NAME=USER_NAME,
                SERVER_NAME=SERVER_NAME,
                cpupercent = cpu_percent,
                cpu_total = ctime.user + ctime.system,
                free_Percnt=(disk_usage.percent),
                bytes_sent = net_io_counters.bytes_sent,
                bytes_received = net_io_counters.bytes_recv,
                packets_sent = net_io_counters.packets_sent,
                packets_received = net_io_counters.packets_recv,

                memory_Free = virtual_memory.free,
                )

            return report
if __name__=='__main__':


    #print(f'starting health report stream for server :\t{SERVER_NAME}')

    while True:
        report = get_health()
        r = requests.post(STATS_URL, json=report)
        time.sleep(10)
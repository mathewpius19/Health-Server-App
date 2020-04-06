import psutil

STATS_URL = ' http://127.0.0.1:8080/report'
SERVER_NAME="test_local_server"

def get_health(): 

    print('generating health report')

    cpu_percent = psutil.cpu_percent(interval=2.0)
    ctime = psutil.cpu_times()
    disk_usage = psutil.disk_usage("/")
    net_io_counters = psutil.net_io_counters()
    virtual_memory = psutil.virtual_memory()    

    # The keys in this dict should match the db cols
    report = dict (
        SERVER_NAME="Test_Local_Server",
        cpupercent = cpu_percent,
        cpu_total = ctime.user + ctime.system,
        free_Percnt=(disk_usage.free/disk_usage.used)/100,
        bytes_sent = net_io_counters.bytes_sent,
        bytes_received = net_io_counters.bytes_recv,
        packets_sent = net_io_counters.packets_sent,
        packets_received = net_io_counters.packets_recv,

        memory_Free = virtual_memory.free,
        )

    return report

if __name__=='__main__':
    import time
    import requests

    print(f'starting health report stream for server :\t{SERVER_NAME}')

    while True:
        report = get_health()
        r = requests.post(STATS_URL, json=report)

        time.sleep(20)
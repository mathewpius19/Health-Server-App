import psutil


cpupercent=psutil.cpu_percent(interval=2.0)
ctime=psutil.cpu_times()
cpu_total=ctime.user+ctime.system
print(cpupercent,cpu_total)

d=psutil.disk_usage("/")
free_Percnt=(d.free/d.used)/100
print(free_Percnt)

net=psutil.net_io_counters()
bytes_sent=net.bytes_sent
bytes_received=net.bytes_recv
packets_sent=net.packets_sent
packets_received=net.packets_recv
print(bytes_sent,bytes_received,packets_sent,packets_received)

mem=psutil.virtual_memory()
memory_Free=mem.free
print(memory_Free)



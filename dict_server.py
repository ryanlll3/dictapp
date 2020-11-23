"""
Dict Server
Function: logical handle
Model: Multi_processing, TCP
"""

from socket import *
from multiprocessing import Process
import signal, sys

# Global vairable

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)


#receive request from clients and handle the request
def request(c):
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)


# Built network
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    # Handle Zombie Process
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # Keep waiting for cent to connect
    print('Listening to the port 8000...')
    while True:
        try:
            c,addr = s.accept()
            print('connected from ', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('server exit...')
        except Exception as e:
            print(e)
            continue
        # Create subprocess for client
        p = Process(target=request,args=(c,))
        p.daemon = True #child process exit if parent process exit
        p.start()

if __name__ == '__main__':
    main()

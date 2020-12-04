"""
Dict Server
Function: logical handle
Model: Multi_processing, TCP

client protocol:
Register - R
    Client: Input register info
            Send request
            Receive feedback
    Server: Receive request
            verify user exist and allow to register
            store user info to db
            feedback to client - user

Login - L
Query Word - Q
History - H
Exit - E
"""

from socket import *
from multiprocessing import Process
import signal, sys, time
from mysql import Database

# Global vairable

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

# Create DB Object
db = Database(database='dict')


#receive request from clients and handle the request


def do_register(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name,passwd):
        c.send(b"OK")
    else:
        c.send(b'Fail')


def do_login(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name,passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

#query word
def do_query(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    #insert history
    db.insert_history(name,word)
    mean = db.query(word)
    if not mean:
        c.send('Not Found Word'.encode())
    else:
        msg = "%s %s" % (word,mean)
        c.send(msg.encode())


#history
def do_history(c,data):
    name = data.split(' ')[1]
    r = db.history(name)
    if not r:
        c.send(b'Fail')
    c.send(b'OK')
    for i in r:
        # i --> (name,word,time)
        msg = "%s %-16s %s" % i  # -16 align left, take 16 space
        time.sleep(0.1)  # avoid bytes sticky while transporting
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')  #sending end


def request(c):
    db.create_cursor()  # child process use own cursor
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if not data or data[0] == 'E':
            sys.exit()
        elif data[0] == 'R':
            do_register(c,data)
        elif data[0] == 'L':
            do_login(c,data)
        elif data[0] == 'Q':
            do_query(c,data)
        elif data[0] == 'H':
            do_history(c,data)



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
            db.close()
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

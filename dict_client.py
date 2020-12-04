"""
dict client
Function: send request according to user input, and receive results
structure: 1st level --> register, login, exit
2nd level --> query word, history, logout
"""

from socket import *
from getpass import getpass # use terminal to enable this package
import sys

# Server Address
ADDR = ('127.0.0.1',8000)
# Build client network
s = socket()
s.connect(ADDR)


def do_query(name):
    while True:
        word = input('Word:')
        if word == '##':
            break
        msg = "Q %s %s" % (name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)


# query history
def do_history(name):
    msg = "H " + name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('NO history found for you.')



# 2nd level login operation

def login(name):
    while True:
        print("""
        ===================Query=================
        1.Query Word        2.History            3.Logout
        ===========================================
        """)
        cmd = input('Input Option(1,2,3):')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print('Please input the listed number.')


def do_register():
    while True:
        name = input('User:')
        passwd = getpass()
        passwd1 = getpass('Again:')
        if passwd != passwd1:
            print('# Password not consistent!')
            continue
        if ' ' in name or ' ' in passwd:
            print("user,password doesn't allow space.")
            continue
        msg = "R %s %s" % (name, passwd)
        s.send(msg.encode())  # send it to server
        data = s.recv(128).decode()  # receive results from server
        if data == 'OK':
            print('Regised successfully')
            login(name)
        else:
            print('Register Failure')
        return

def do_login():
    while True:
        name = input('User:')
        passwd = getpass()
        msg = "L %s %s" % (name, passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print('Login Successfully')
            login(name)
        else:
            print('Login Failed')
        return


def main():
    while True:
        print("""
        ===================Welcome=================
        1.Register        2.Login            3.Exit
        ===========================================
        """)
        cmd = input('Input Option(1,2,3):')
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            sys.exit("Byebye")
        else:
            print('Please input the listed number.')

if __name__ == '__main__':
    main()


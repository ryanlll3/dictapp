"""
dict client
Function: send request according to user input, and receive results
structure: 1st level --> register, login, exit
2nd level --> query word, history, logout
"""

from socket import *
from getpass import getpass # use terminal to enable this package


# Server Address
ADDR = ('127.0.0.1',8000)

# Build client network
def main():
    s = socket()
    s.connect(ADDR)
    while True:
        print("""
        ===================Welcome=================
        1.Register        2.Login            3.Quit
        ===========================================
        """)
        cmd = input('Input Option(1,2,3):')
        if cmd == '1':
            s.send(cmd.encode())
        elif cmd == '2':
            pass
        elif cmd == '3':
            pass
        else:
            print('Please input the listed number.')



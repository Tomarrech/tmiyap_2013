__author__ = 'issahar'
# telnet program example
import socket
import select
import sys
import telnetlib

#main function
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host'

    while 1:
        socket_list = [s]
        print socket_list
        # Get the list sockets which are readable
        #read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        #print read_sockets, write_sockets, error_sockets
        for sock in socket_list:
            #incoming message from remote server
            if sock == s:
                #s.send("GET")
                data = sock.recv(4096)
                if not data:
                    print 'Connection closed'
                    sys.exit()
                else:
                    print data
            #user entered a message
            else:
                msg = raw_input("Input text\n")
                s.send(msg)
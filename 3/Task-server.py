__author__ = 'issahar'
#coding: utf-8
import socket

flag = b"{0123456789abcdef0123456789ABCDEF}"
sigma = False


def main():
    sock = socket.socket()
    sock.bind(("192.168.1.3", 14900))
    sock.listen(10)
    conn, addr = sock.accept()
    conn.settimeout(10)
    print "connected", addr
    get_data(conn)
    conn.close()


def get_data(conn):

    while True:
        data = conn.recv(64)
        if not data:
            print "No data"
            break
        else:
            udata = data.decode("utf-8")
            print("Data: \n" + udata)
            #sigma = True
            break
    check_flag(sigma, conn)



def check_flag(sigma, conn):
    if sigma is True:
        print "Good work"
        conn.send(b"Good, now you can get  your flag...\n")
        conn.send(flag)
    else:
        print "Error"
        conn.send(b"File is not correct, try again!")


if __name__ == "__main__":
    main()
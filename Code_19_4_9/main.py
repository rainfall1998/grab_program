from socket import *
import threading


def trans(sock1, sock2, BUFSIZ):
    while True:
        try:
            data = sock1.recv(BUFSIZ)
        except OSError:
            break
        if not data:
            sock1.close()
        else:
            try:
                sock2.send(data)
            except OSError:
                sock1.close()
                break


if __name__ == '__main__':
    HOST = '172.19.161.25'
    POST = 7890
    ADDR = (HOST, POST)
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.bind(ADDR)
    tcp.listen(3)

    Users = []
    Addrs = []
    Trans = []
    while len(Users) != 2:
        tcpCli, addr = tcp.accept()
        Users.append(tcpCli)
    trans1 = threading.Thread(target=trans, args=(Users[0], Users[1], 1024))
    trans1.start()

    while True:
        try:
            data = Users[1].recv(1024)
        except OSError:
            break
        if not data:
            Users[1].close()
        else:
            try:
                Users[0].send(data)
            except OSError:
                Users[1].close()
                break
    tcp.close()

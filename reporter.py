import socket
import pickle
class Reporter:
    def __init__(self, ip, port):
        self.sock=socket.socket()
        self.sock.connect((ip, port))

    def report(self, data: dict):
        if type(data)!=dict:
            raise TypeError('require dict')
        self.sock.send(pickle.dumps(data))


if __name__=="__main__":
    rp=Reporter('127.0.0.1', 9090)
    rp.report({'hello':'world'})
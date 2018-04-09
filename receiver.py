import datetime
import socket
import socketserver
import pickle
import pymongo


"""
connect to local mongoDB
assume noauth=true
"""
db_conn = pymongo.MongoClient()

"""
write dict data to local mongodb
"""
def writeDB(data: dict, dbset: str):
    db_conn['message'][dbset].save(data)


"""
check auth info, return identity name
"""
def auth(input):
    return 'unknown'


"""
add trusted ips
"""

trusted_ip = {
    '127.0.0.1': 'LOCAL'
}


class Handler(socketserver.BaseRequestHandler):
    """
    Process dict message from single client
    """

    def handle(self):

        # identify ip address

        identity = 'unknown'
        ip = self.request.getpeername()[0]
        if ip in trusted_ip.keys():
            identity = trusted_ip[ip]
            print('connection from trusted ip: ', ip)


        # receive data frame by frame

        while True:
            try:
                data = self.request.recv(1024)

                # load dict object from bytes

                obj = pickle.loads(data)

                if type(obj) == dict:

                    # set time

                    obj['time'] = datetime.datetime.now()

                    # check auth info

                    if 'auth' in obj.keys():
                        identity = auth(obj['auth'])
                        obj.pop('auth')

                    print(obj)

                    # log into database

                    if len(obj) > 0:
                        writeDB(obj, identity)

            except EOFError as e:
                break

            except Exception as e:
                print(e)


server = socketserver.ThreadingTCPServer(('', 6666), Handler)
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.serve_forever()

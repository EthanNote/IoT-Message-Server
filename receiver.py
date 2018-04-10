import datetime
import socket
import socketserver
import pickle
import pymongo
# from webserver import broadcast

class Receiver(socketserver.BaseRequestHandler):
    """
    connect to local mongoDB
    assume noauth=true
    """
    db_conn = pymongo.MongoClient()
    event_callback=None

    """
    write dict data to local mongodb
    """
    def writeDB(data: dict, dbset: str):
        Receiver.db_conn['message'][dbset].save(data)


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
    """
    Process dict message from single client
    """

    host_port=9000

    def notify(self, message):
        pass


    def handle(self):

        # identify ip address

        identity = 'unknown'
        ip = self.request.getpeername()[0]
        if ip in Receiver.trusted_ip.keys():
            identity = Receiver.trusted_ip[ip]
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
                        identity = Receiver.auth(obj['auth'])
                        obj.pop('auth')

                    # log into database
                    if len(obj) > 0:
                        Receiver.writeDB(obj, identity)
                        self.notify(obj)


            except EOFError as e:
                break

            except Exception as e:
                print(e)

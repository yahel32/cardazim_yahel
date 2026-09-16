import socket

class Listener:
    def __init__(self, port,host,backlog=1000):
        self.port = port
        self.host = host
        self.backlog = backlog

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

    def __repr__(self):
        return "Listener(port="+str(self.port)+', host="'+self.host+'", backlog='+self.backlog+")"

    def start(self):
        self.socket.listen()

    def stop(self):
        self.socket.close()

    def accept(self):
        client_socket, client_address = self.socket.accept()
        return client_socket

    def __enter__(self,port,host,backlog=1000):
        listener = Listener(self,port,host,backlog)
        listener.start()
        return listener

    def __exit__(self):
        self.stop()
        

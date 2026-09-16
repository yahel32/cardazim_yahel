import socket
import connection
class Listener:
    def __init__(self, port,host,backlog=1000):
        self.port = port
        self.host = host
        self.backlog = backlog

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.listening = False 

    def __repr__(self):
        return f"Listener(host='{self.host}', port={self.port}, backlog={self.backlog})"

    def start(self):
        if not self.listening:
            self.socket.listen(self.backlog)
            self.listening = True

    def stop(self):
        self.socket.close()
        self.listening = False

    def accept(self):
        if not self.listening:
            self.start()
        client_socket, client_address = self.socket.accept()
        return connection.Connection(client_socket)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.stop()
        

import socket
import struct

class Connection:
    def __init__(self, connection: socket.socket):
        """
        create the connection using a socket
        """
        self.remote_ip, self.remote_port = connection.getpeername()
        self.local_ip, self.local_port = connection.getsockname()
        self.socket = connection


    def __repr__(self):
        local = self.local_ip+":"+str(self.local_port)
        remote = self.remote_ip+":"+str(self.remote_port)
        return "<Connection from "+local+" to "+remote+">"

    def send_message(self, message:bytes):
        """
        send message using the agreed protocol
        """
        msg_size = len(message)
        size_bytes = struct.pack('<I', msg_size)
        final_packet =size_bytes+message

        self.socket.sendall(final_packet)

    def receive_message(self):
        """
        receive a message and checks it using the protocol
        """
        msg = b''
        while True:
            # receive data first 4 bytes from the client
            data=self.socket.recv(1024)
            msg+=data
            if not data: # client disconnected or finished sending
                if len(msg)<4:
                    raise Exception("closed before full transmition")
                elif len(msg)>=4:#check length
                    length_bytes = msg[:4]
                    length = int.from_bytes(length_bytes, byteorder='little')
                    if len(msg) == 4+length:#correct
                        return msg[4:].decode("utf-8")
                    else:#wrong length
                        raise Exception("closed before full transmition")

    @classmethod
    def connect(cls,host,port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((host, port))
        return Connection(connection)

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self.connect(self.host,self.port)
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        self.socket.close()


            


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
        expected_length = None
        while True:
            
            data=self.socket.recv(1024)
            if not data:
                raise Exception("closed before full transmission")
            msg+=data
            if expected_length is None and len(msg) >= 4:
                expected_length = struct.unpack('<I', msg[:4])[0]
            if expected_length is not None:
                if len(msg) >= 4 + expected_length:
                    actual_message = msg[4:4 + expected_length]
                    return actual_message.decode("utf-8")

    @classmethod
    def connect(cls,host,port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((host, port))
        return Connection(connection)

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        self.close()


            


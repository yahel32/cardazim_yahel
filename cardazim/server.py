import socket
import sys
import argparse
import threading
import struct

def handle_client(client_socket,client_address):
    """
    recieves the information from the client and prints to screen
    """

    msg = b''
    expected_length = None
    with client_socket:
        while True:
            data= client_socket.recv(4096)
            if not data:
                raise Exception("client disconnected or wrong length")
            msg+=data
            
            if expected_length is None and len(msg) >= 4:
                expected_length = struct.unpack('<I', msg[:4])[0]

            if expected_length is not None:
                if len(msg) >= 4 + expected_length:
                    actual_message = msg[4:4 + expected_length]
                    return actual_message.decode("utf-8")


def run_server(ip,port):
    """
    starting the server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target = handle_client, args=(client_socket,client_address))
            client_thread.daemon = True
            client_thread.start()
    

def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help="the server's ip")
    parser.add_argument('server_port', type=int,
                        help="the server's port")
    return parser.parse_args()

def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    run_server(args.server_ip,args.server_port)
    print('Done.')

if __name__=="__main__":
    sys.exit(main())


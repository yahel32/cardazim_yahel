import socket
import sys
import argparse
import threading

def handle_client(client_socket,client_address):
    """
    recieves the information from the client and prints to screen
    """

    msg = b''
    with client_socket:
        while True:
            data= client_socket.recv(4096)
            msg+=data
            if len(data)>=4:
                length = int.from_bytes(data[:4], byteorder='little')
                if len(data)-4==length:
                    print("Received data:", msg[4:length+4].decode("utf-8"))
                    return
            if not data: # client disconnected or wrong length
                raise Exception("client disconnected or wrong length")

def run_server(ip,port):
    """
    starting the server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()#accept new connection
            client_thread = threading.Thread(target = handle_client, args=(client_socket,client_address))#open thread for it
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


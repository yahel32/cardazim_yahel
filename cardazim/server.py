import socket
import sys
import argparse

def run_server(ip,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            msg = b''
            with client_socket:
                while True:
                    # receive data from the client (buffer size 1024 bytes)
                    data= client_socket.recv(4096)

                    
                    if not data: # client disconnected
                        print("Received data:", msg.decode("utf-8"))
                        break
                    msg+=data
    

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
    # try:
    run_server(args.server_ip,args.server_port)
    print('Done.')
    # except Exception as error:
    #     print(f'ERROR: {error}')
    #     return 1

if __name__=="__main__":
    sys.exit(main())


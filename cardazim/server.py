import socket
import sys
import argparse
import threading
import listener
import connection


def handle_client(conn_obj):
    """
    recieves the information from the client and prints to screen
    """

    with conn_obj:
        try:
            message = conn_obj.receive_message()
            
            print("Received data:", message)
            
        except Exception as e:
            print(f"Error handling client {conn_obj.remote_ip}: {e}")

def run_server(ip,port):
    """
    creating and running the server
    """
    with listener.Listener(port,ip) as server:
        while True:
            conn = server.accept() 
            client_thread = threading.Thread(target = handle_client, args=(conn,))
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


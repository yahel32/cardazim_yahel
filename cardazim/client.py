import argparse
import sys



###########################################################
####################### YOUR CODE #########################
###########################################################

import struct
import socket
def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    msg_bytes = data.encode('utf-8')
    msg_size = len(msg_bytes)
    size_bytes = struct.pack('<I', msg_size)
    final_packet = size_bytes+msg_bytes

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
         client_socket.connect((server_ip, server_port))
         print("Connected to server")
         client_socket.sendall(final_packet)

    except ConnectionRefusedError:
        print("Connection failed")
    finally:
        client_socket.close()
        print("Connection closed")



###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help="the server's ip")
    parser.add_argument('server_port', type=int,
                        help="the server's port")
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    send_data(args.server_ip, args.server_port, args.data)
    print('Done.')


if __name__ == '__main__':
    sys.exit(main())

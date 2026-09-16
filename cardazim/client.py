import argparse
import sys
import connection



###########################################################
####################### YOUR CODE #########################
###########################################################

import struct
import socket
def send_data(server_ip, server_port, data):
    '''
    Send data to server(listener) using connection
    '''
    with connection.Connection.connect(server_ip, server_port) as conn:
        data_bytes = data.encode('utf-8')
        conn.send_message(data_bytes)



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

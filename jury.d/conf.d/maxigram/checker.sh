#!/usr/bin/env python3

import errno
import json
import socket
import sys
from hashlib import sha512
import time
from datetime import datetime as dt


# put-get flag to service success
def service_up():
    print("[service is up] - 101")
    exit(101)


# service is available (available tcp connect) but protocol could not put/get flag
def service_corrupt():
    print("[service is corrupt] - 102")
    exit(102)


# waited time (for example: 5 sec) but service did not have time to reply
def service_mumble():
    print("[service is mumble] - 103")
    exit(103)


# service is not available (maybe blocked port or service is down)
def service_down():
    print("[service is down] - 104")
    exit(104)


def send_request(sock, **kwargs):
    # print(kwargs)
    sock.send(json.dumps(dict(**kwargs)).encode())
    time.sleep(.5)
    data = sock.recv(1024).decode()
    # print(f'  {data}')
    if 'invalid input' in data:
        service_corrupt()
    return data


def put_flag():
    username = sha512('{}sec'.format(f_id).encode()).hexdigest()[:10]
    password = sha512('{}sec'.format(flag).encode()).hexdigest()[:10]
    s = None
    # try put
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
    except socket.timeout:
        service_down()
    except Exception:
        service_down()
    try:
        send_request(s, username=username, create_user=True, password=password)
        send_request(s, username=username, password=password)
        send_request(s, username=username,
                     room_name=f_id,
                     room_type='1',
                     create_room=True,
                     users=[username])
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        send_request(s, username=username, password=password)
        send_request(s, username=username,
                     message=flag,
                     room=f_id,
                     dt=str(dt.now()))
        s.close()
        service_up()
    except socket.timeout:
        print('timeout')
        service_corrupt()
    except socket.error as serr:
        if serr.errno == errno.ECONNREFUSED:
            print('connrefused')
            service_corrupt()
        else:
            print(serr)
            service_corrupt()
    except Exception as e:
        print(e)
        service_corrupt()


def check_flag():
    username = sha512('{}sec'.format(f_id).encode()).hexdigest()[:10]
    password = sha512('{}sec'.format(flag).encode()).hexdigest()[:10]
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
    except socket.timeout:
        print('timeout')
        service_down()
    except Exception:
        service_down()
    try:
        send_request(s, username=username, password=password)
        data = send_request(s, username=username, history=True)
        data = json.loads(data)
        s.close()
        if flag in (msg.get('message') for msg in data.get('history')):
            service_up()
        else:
            service_corrupt()
    except socket.timeout:
        print('timeout')
        service_corrupt()
    except socket.error as serr:
        if serr.errno == errno.ECONNREFUSED:
            print('connrefused')
            service_down()
        else:
            print(serr)
            service_corrupt()
    except Exception as e:
        print(e)
        service_corrupt()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('\nUsage:\n\t{} <host> (put|check) <flag_id> <flag>\n'.format(sys.argv[0]))
        exit(1)

    host, command, f_id, flag = sys.argv[1:]
    port = 8888

    if command == 'put':
        put_flag()
        check_flag()
    elif command == 'check':
        check_flag()
    else:
        print('Wrong command!')
        exit(1)

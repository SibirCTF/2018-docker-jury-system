#!/usr/bin/python3
import sys
import random
import time
import socket
import hashlib
# put-get flag to service success
def service_up():
    print ("[service is worked] - 101")
    exit(101)

# service is available (available tcp connect) but protocol wrong could not put/get flag
def service_corrupt():
    print ("[service is corrupt] - 102")
    exit(102)

# waited time (for example: 5 sec) but service did not have time to reply
def service_mumble():
    print ("[service is mumble] - 103")
    exit(103)

# service is not available (maybe blocked port or service is down)
def service_down():
    print ("[service is down] - 104")
    exit(104)

if len(sys.argv) != 5:
    print("\nUsage:\n\t" + sys.argv[0] + " <host> (put|check|put1|check1) <flag_id> <flag>\n")
    print("Example:\n\t" + sys.argv[0] + " \"127.0.0.1\" put \"abcdifghr\" \"123e4567-e89b-12d3-a456-426655440000\" \n")
    print("\n")
    exit(0)

host = sys.argv[1]
port = 5003
command = sys.argv[2]
f_id = sys.argv[3]
flag = sys.argv[4]

def put_flag():
    global host, port, f_id, flag
    try:
        sock = socket.socket()
        sock.connect((host,port))
        data = sock.recv(1024).decode('utf-8')
        print(data)
        sock.send(('/CREATE '+f_id+' '+f_id+' '+flag+'\n').encode('utf-8'))
        print('create sended')
        data = sock.recv(1024).decode('utf-8')
        print(data)
        if "Error" in data:
            service_corrupt()
        elif "Success" in data:
            sock.send(('/USER '+f_id+'\n').encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            print(data)
            sock.send(('/PASS '+flag+'\n').encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            print(data)
            if "Success" in data:
                return
        service_down()
    except Exception as e:
        print("Error: ")
        print(e)
        service_corrupt()

def put_flag1():
    global host, port, f_id, flag
    try:
        sock1=socket.socket()
        sock2=socket.socket()
        sock1.connect((host,port))
        data1=sock1.recv(1024).decode('utf-8')
        sock2.connect((host,port))
        data2=sock2.recv(1024).decode('utf-8')
        sha1=hashlib.sha1()
        sha1.update((f_id+'_1').encode('utf-8'))
        pass1=sha1.hexdigest()
        sock1.send(('/CREATE '+f_id+'_1'+' '+f_id+'_1'+' '+pass1+'\n').encode('utf-8'))
        data1 = sock1.recv(1024).decode('utf-8')
        print(data1)
        sha2=hashlib.sha1()
        sha2.update((f_id+'_2').encode('utf-8'))
        pass2=sha2.hexdigest()
        sock2.send(('/CREATE '+f_id+'_2'+' '+f_id+'_2'+' '+pass2+'\n').encode('utf-8'))
        data2 = sock2.recv(1024).decode('utf-8')
        print(data2)
        if "Error" in data1 or "Error" in data2:
            service_corrupt()
        elif "Success" in data1 and "Success" in data2:
            sock1.send(('/USER '+f_id+'_1'+'\n').encode('utf-8'))
            data1 = sock1.recv(1024).decode('utf-8')
            print(data1)
            sock1.send(('/PASS '+pass1+'\n').encode('utf-8'))
            data1 = sock1.recv(1024).decode('utf-8')
            print(data1)
            sock2.send(('/USER '+f_id+'_2'+'\n').encode('utf-8'))
            data2 = sock2.recv(1024).decode('utf-8')
            print(data2)
            sock2.send(('/PASS '+pass2+'\n').encode('utf-8'))
            data2 = sock2.recv(1024).decode('utf-8')
            print(data2)
            if "Success" in data1 and "Success" in data2:
                sock1.send(("/MSG "+f_id+"_2"+" flag is "+flag+'\n').encode('utf-8'))
                data_with_flag=sock2.recv(1024).decode('utf-8')
                if flag in data_with_flag:
                    service_up()
                else:
                    service_corrupt()
        service_down()
    except Exception as e:
        print("Error: ")
        print(e)
        service_corrupt()

def check_flag1():
    global host, port, f_id, flag
    try:
        sock1=socket.socket()
        sock1.connect((host,port))
        data1=sock1.recv(1024).decode('utf-8')
        print(data1)
        sock1.send(('/USER '+f_id+'_1'+'\n').encode('utf-8'))
        data1=sock1.recv(1024).decode('utf-8')
        print(data1)
        sha1=hashlib.sha1()
        sha1.update((f_id+'_1').encode('utf-8'))
        pass1=sha1.hexdigest()
        sock1.send(('/PASS '+pass1+'\n').encode('utf-8'))
        data1 = sock1.recv(1024).decode('utf-8')
        print(data1)
        
        sock2=socket.socket()
        sock2.connect((host,port))
        data2=sock2.recv(1024).decode('utf-8')
        print(data2)
        sock2.send(('/USER '+f_id+'_2'+'\n').encode('utf-8'))
        data2=sock2.recv(1024).decode('utf-8')
        print(data2)
        sha2=hashlib.sha1()
        sha2.update((f_id+'_2').encode('utf-8'))
        pass2=sha2.hexdigest()
        sock2.send(('/PASS '+pass2+'\n').encode('utf-8'))
        data2 = sock2.recv(1024).decode('utf-8')
        print(data2)
        if "Error" in data1 or "Error" in data2:
            service_corrupt()
        elif "Success" in data1 and "Success" in data2:
            sock2.send(("/RESTORE private").encode('utf-8'))
            data_with_flag = sock2.recv(1024).decode('utf-8')
            if flag in data_with_flag:
                service_up()
            else:
                service_corrupt()
        service_down()
    except Exception as e:
        print(e)
        service_corrupt()
    service_down()

def check_flag():
    global host, port, f_id, flag

    try:
        sock=socket.socket()
        sock.connect((host,port))
        sock.recv(1024)
        sock.send(('/USER '+f_id+'\n').encode('utf-8'))
        sock.recv(1024)
        sock.send(('/PASS '+flag+'\n').encode('utf-8'))
        data = sock.recv(1024).decode('utf-8')
        if "Error" in data:
            service_corrupt()
        elif "Success" in data:
            service_up()
        service_down()
    except Exception as e:
        print(e)
        service_corrupt()
    service_down()

def f(string):
    res=0
    for i in string:
        res+=ord(i)
    return res%2==0

if f(f_id):
   if command=="put":
        put_flag()
        check_flag()
   elif command=="check":
        check_flag()
else:
    if command=="put":
        put_flag1()
        check_flag1()
    elif command=="check":
        check_flag1()
    

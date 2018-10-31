#!/usr/bin/python3
import sys
import time
import errno
import requests
import os
import random
import re
import hashlib
import json
from faker import Faker
fake = Faker()

workdir = os.path.abspath(__file__)[:-18]

# put-get flag to service success
def service_up():
    print("[service is worked] - 101")
    exit(101)

# service is available (available tcp connect) but protocol wrong could not put/get flag
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

def get_pass_from_fid(password):
    password = hashlib.md5(password.encode('UTF-8')).hexdigest()
    return password

if len(sys.argv) != 5:
    print("\nUsage:\n\t" + sys.argv[0] + " <host> (put|check) <flag_id> <flag>\n")
    print("Example:\n\t" + sys.argv[0] + " \"127.0.0.1\" put \"abcdifghr\" \"123e4567-e89b-12d3-a456-426655440000\" \n")
    print("\n")
    exit(0)

host = sys.argv[1]
port = 80
command = sys.argv[2]
raw_password = sys.argv[3]
login = sys.argv[4]

# will be mumble (2) - for test jury
# while True: time.sleep(10);

public_name = fake.first_name()
email = fake.free_email()

def register(host, port, login, email, public_name, password):
    try:
        avatarname = random.choice(os.listdir(workdir+'avatars/'))
        avatar = {'picture': (avatarname, open(workdir+'avatars/' + avatarname, 'rb'), "image/png")}
        data = {
            'inputLogin': login,
            'inputEmail': email,
            'inputPublicName': public_name,
            'inputPassword1': password,
            'inputPassword2': password,
            'register':'True'
        }
        r = requests.post('http://{}:{}/registration.php'.format(host, port), data = data, files=avatar, allow_redirects=False, timeout=3)
        if r.status_code != 200:
            service_corrupt()
        with open('{}data/{}.json'.format(workdir,raw_password), 'w') as data:
                  data.write(json.dumps({'public_name':public_name, 'email':email}))
    except requests.exceptions.ReadTimeout as e:
        print(e)
        service_mumble()
    except requests.exceptions.ConnectTimeout as e:
        print(e)
        service_down()
    except requests.exceptions.ConnectionError as e:
        print(e)
        service_down()
    except Exception as e:
        print(e)
        service_corrupt()

def sign_in(host, port, login, password):
    try:
        data = {
            'inputEmailorLogin': login,
            'inputPassword': password,
            'signin':'True'
        }
        r = requests.post('http://{}:{}/login.php'.format(host, port), data = data, allow_redirects=False, timeout=3)
        if r.status_code != 200:
            service_corrupt()
        cookies = r.cookies
        
        return cookies
    except requests.exceptions.ReadTimeout as e:
        print(e)
        service_mumble()
    except requests.exceptions.ConnectTimeout as e:
        print(e)
        service_down()
    except requests.exceptions.ConnectionError as e:
        print(e)
        service_down()
    except Exception as e:
        print(e)
        service_corrupt()


def check_flag(host, port, login, password):
    try:
        with open('{}data/{}.json'.format(workdir, raw_password), 'r') as data:
            tmp = json.loads(data.read())
            public_name = tmp['public_name']
            email = tmp['email']
        cookies = sign_in(host, port, login, password)
        r = requests.get('http://{}:{}/user_info.php'.format(host, port), cookies=cookies, allow_redirects=False, timeout=3)
        try:
            if re.findall(r'Login: ([a-f0-9]{8,8}-[a-f0-9]{4,4}-[a-f0-9]{4,4}-[a-f0-9]{4,4}-[a-f0-9]{12,12})', r.text)[0] != login or\
                re.findall(r'>Name: (\w+?)<', r.text)[0] != public_name or\
                re.findall(r'>Email: ([\s\S]+?)<', r.text)[0] != email:
                service_corrupt()
        except IndexError as e:
            print(e)
            service_corrupt()

        sections = [
            'anime',
            'bullshit',
            'cosplay',
            'manga'
        ]
        theme = fake.word().capitalize()
        message = fake.paragraph(nb_sentences=5)

        
        thread_image_name = random.choice(os.listdir(workdir+'images/'))
        thread_image = {'picture': (thread_image_name, open(workdir+'images/' + thread_image_name, 'rb'))}
        data = {
            'theme': theme,
            'message': message,
            'save':'True'
        }
        
        r = requests.post('http://{}:{}/threads.php?section={}'.format(host, port, random.choice(sections)), data = data, files=thread_image, cookies=cookies, allow_redirects=False, timeout=3)
        if r.status_code != 200:
            service_corrupt()
        try:
            thread_id = re.findall(r'Thread created successfully. "(\d+)"', r.text)[0]
        except IndexError as e:
            print(e)
            service_corrupt()
        time.sleep(0.25)
        try:
            r = requests.get('http://{}:{}/thread.php?id={}'.format(host, port, thread_id), cookies=cookies, allow_redirects=False, timeout=3)
            if r.status_code != 200:
                service_corrupt()
            if re.findall(r'Неверный id треда!', r.text)[0]:
                service_corrupt()
            try:
                if re.findall(r'>Name: (\w+?)<', r.text)[0] != public_name or\
                    re.findall(r'>Email: ([\s\S]+?)<', r.text)[0] != email:
                    service_corrupt()
            except IndexError as e:
                print(e)
                service_corrupt()
            
        except IndexError:
            pass
        
    except IndexError as e:
        print(e)
        service_corrupt()
    except requests.exceptions.ReadTimeout as e:
        print(e)
        service_mumble()
    except requests.exceptions.ConnectTimeout as e:
        print(e)
        service_down()
    except requests.exceptions.ConnectionError as e:
        print(e)
        service_down()
    except Exception as e:
        print(e)
        service_corrupt()


if command == "put":
    register(host, port, login, email, public_name, get_pass_from_fid(raw_password))
    time.sleep(0.25)
    check_flag(host, port, login, get_pass_from_fid(raw_password))
    service_up()

if command == "check":
    check_flag(host, port, login, get_pass_from_fid(raw_password))
    service_up()


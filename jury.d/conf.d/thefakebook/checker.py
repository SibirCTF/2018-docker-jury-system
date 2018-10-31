#!/usr/bin/env python3

import os
import requests
from sys import argv
from hashlib import sha256, md5
from random import choice
import shutil
import re

os.chdir(os.path.dirname(__file__))

# For edit
PIC_DIR = 'memes/'
FLAG_PIC_DIR = 'flag_memes/'

# For service, do not touch
TIME_OUT = 5
PORT = 8000
FILES = os.listdir(PIC_DIR)
STATUS_CODE = {
    'INVALID ARGVS': 110,
    'SUCCESS': 101,
    'CORRUPT': 102,
    'MUMBLE': 103,
    'DOWN': 104}


class MyException(Exception):
    pass


def registration(hostname, f_id, flag, add_id):
    """
    Регистрируем пользователя

    :param hostname: адрес
    :param port: порт
    :return: имя пользователя, почтовый ящик и пароль
    """
    nickname = 'user_{num}{id}'.format(
        num=sha256(str(f_id).encode()).hexdigest()[:4] + md5(
            flag.encode()).hexdigest()[:4],
        id=add_id)
    passwd = sha256((f_id + str(add_id)).encode()).hexdigest()[:7] + md5(
        flag.encode()).hexdigest()[:7]
    email = '{nick}@trusty.mail'.format(nick=nickname)

    client = requests.session()
    client.get(
        'http://{hostname}:{port}/index'.format(hostname=hostname, port=PORT),
        timeout=TIME_OUT)

    csrf_token = client.cookies['csrftoken']
    payload = {'csrfmiddlewaretoken': csrf_token,
               'name': nickname,
               'status': choice(range(1, 6)),
               'email': email,
               'pass': passwd,
               'terms': 1}

    resp = client.post(
        'http://{hostname}:{port}/register'.format(hostname=hostname,
                                                   port=PORT),
        data=payload,
        headers=dict(
            Referer='http://{hostname}:{port}/index'.format(hostname=hostname,
                                                            port=PORT)),
        timeout=TIME_OUT)

    if resp.status_code >= 400: raise MyException('Vse idet ko dnu')
    print('Registration code: \033[92m{status}\033[0m'.format(
        status=resp.status_code))

    return nickname, email, passwd


def authorization(hostname, email, passwd):
    """
    Авторизуемся в сервисе

    :param hostname: адрес
    :param port: порт
    :param email: почта
    :param passwd: пароль
    :return: сессия
    """
    client = requests.session()
    client.get(
        'http://{hostname}:{port}/index'.format(hostname=hostname, port=PORT),
        timeout=TIME_OUT)
    csrf_token = client.cookies['csrftoken']
    payload = {'csrfmiddlewaretoken': csrf_token,
               'email': email,
               'pass': passwd}

    resp = client.post(
        'http://{hostname}:{port}/login'.format(hostname=hostname, port=PORT),
        data=payload,
        headers=dict(
            Referer='http://{hostname}:{port}/login'.format(hostname=hostname,
                                                            port=PORT)),
        timeout=TIME_OUT)
    if resp.status_code >= 400: raise MyException('Vse idet ko dnu')
    print('Auth code: \033[93m{status}\033[0m'.format(status=resp.status_code))

    return client


def check_an_avatar(hostname, client):
    """
    Проверяем доступность аватарки

    :param hostname: адрес
    :param port: порт
    :param client: сессия
    :return: статус код
    """
    request = client.get(
        'http://{hostname}:{port}/profile'.format(hostname=hostname,
                                                  port=PORT), timeout=TIME_OUT)
    image_url = re.findall(r'\<img\ width\=\"150pt\"\ src\=\"(.+?)\"\>',
                           request.content.decode("utf-8"))
    if image_url:
        request = client.get(
            'http://{hostname}:{port}{picture}'.format(hostname=hostname,
                                                       port=PORT,
                                                       picture=image_url[0]),
            timeout=TIME_OUT)

    return request.status_code


def add_meta_info_in_picture(file, f_id, flag):
    """
    Делаем копию изображения и добавляем флаг в метаданные

    :param file: картинка, путь вместе с папкой
    :param f_id: id флага
    :param flag: флаг
    :return: путь до новой картинки
    """
    new_file = str(f_id + '3') + '.jpg'
    shutil.copyfile('{file}'.format(file=file),
                    '{dir}{new_file}'.format(dir=FLAG_PIC_DIR,
                                             new_file=new_file))
    os.popen(
        'exiftool -Title="Hey, flag there: {flag}" -Author="Keva" -overwrite_original {file}'.format(
            flag=flag, file=FLAG_PIC_DIR + new_file))

    return FLAG_PIC_DIR + new_file


def put(hostname, f_id, flag):
    """
    Регистрируем двух пользователей.
    Добавляемся в друзья от имени первого пользователя и
                                                отправляем флаг второму.

    :param hostname: адрес
    :param port: порт
    :param f_id: id флага
    :param flag: флаг string
    :return: статус success
    """
    try:
        print('Start put')
        user1_nick, user1_email, user1_passwd = registration(hostname, f_id,
                                                             flag,
                                                             1)
        print(user1_email, user1_passwd)
        user2_nick, user2_email, user2_passwd = registration(hostname, f_id,
                                                             flag,
                                                             2)
        print(user2_email, user2_passwd)
        client = authorization(hostname, user1_email, user1_passwd)
        resp = client.get(
            'http://{hostname}:{port}/profile'.format(hostname=hostname,
                                                      port=PORT),
            timeout=TIME_OUT)
        print('Profile code: \033[92m{status}\033[0m'.format(
            status=resp.status_code))
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')
        csrf_token = client.cookies['csrftoken']

        payload = {'csrfmiddlewaretoken': csrf_token}
        picture = PIC_DIR + choice(FILES)
        if ord(f_id[-1]) % 5 == 0:
            picture = add_meta_info_in_picture(picture, f_id, flag)

        files = {'picture': open(picture, 'rb')}

        resp = client.post(
            'http://{hostname}:{port}/profile/pic_edit'.format(
                hostname=hostname,
                port=PORT),
            data=payload,
            files=files,
            timeout=TIME_OUT)

        print('Upload picture code: \033[92m{status}\033[0m'.format(
            status=resp.status_code))
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        resp = check_an_avatar(hostname, client)
        print('Check avatar: \033[96m{status}\033[0m'.format(
            status=resp))
        if resp >= 400: raise MyException('Vse idet ko dnu')

        payload = {'csrfmiddlewaretoken': csrf_token,
                   'search_text': user2_nick}

        resp = client.post(
            'http://{hostname}:{port}/search'.format(hostname=hostname,
                                                     port=PORT),
            data=payload,
            headers=dict(
                Referer='http://{hostname}:{port}/search'.format(
                    hostname=hostname,
                    port=PORT)),
            timeout=TIME_OUT)
        print('Search code: \033[92m{status}\033[0m'.format(
            status=resp.status_code))
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        search_user = \
            re.findall(
                r'<a href="/profile/(\d+)">{name}'.format(name=user2_nick),
                resp.text)[0]
        client.get(
            'http://{hostname}:{port}/profile/{user}/add_to_friend'.format(
                hostname=hostname,
                port=PORT,
                user=search_user),
            timeout=TIME_OUT)
        client.get(
            'http://{hostname}:{port}/messages/{user}'.format(
                hostname=hostname,
                port=PORT,
                user=search_user),
            timeout=TIME_OUT)

        csrf_token = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken': csrf_token,
                   'subject': 'Here the Flag',
                   'text': flag}

        resp = client.post(
            'http://{hostname}:{port}/messages/{user}'.format(
                hostname=hostname,
                port=PORT,
                user=search_user),
            data=payload,
            headers=dict(
                Referer='http://{hostname}:{port}/messages/{user}'.format(
                    hostname=hostname,
                    port=PORT,
                    user=search_user)),
            timeout=TIME_OUT)
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')
        print('Messages code: \033[92m{status}\033[0m'.format(
            status=resp.status_code))
        print('\033[92mSuccess {}\033[0m'.format(STATUS_CODE['SUCCESS']))
        exit(STATUS_CODE['SUCCESS'])
    except requests.exceptions.Timeout:
        print('\033[96mMumble {}\033[0m'.format(STATUS_CODE['MUMBLE']))
        exit(STATUS_CODE['MUMBLE'])
    except requests.exceptions.ConnectionError:
        print('\033[93mDown {}\033[0m'.format(STATUS_CODE['DOWN']))
        exit(STATUS_CODE['DOWN'])
    except MyException:
        print('\033[91mCorrupt {}\033[0m'.format(STATUS_CODE['CORRUPT']))
        exit(STATUS_CODE['CORRUPT'])
    except Exception as error:
        print('Всё очень плохо :c ' + str(error))


def check(hostname, f_id, flag):
    """
    Авторизуемся под вторым пользователем, заходим в сообщения и получаем флаг
    """
    try:
        print('Start check')
        user1_nick = 'user_{num}1'.format(
            num=sha256(str(f_id).encode()).hexdigest()[:4] + md5(
                flag.encode()).hexdigest()[:4])
        passwd = sha256(str(f_id + '2').encode()).hexdigest()[:7] + md5(
            flag.encode()).hexdigest()[:7]
        email = '{nick}@trusty.mail'.format(nick='user_{num}2'.format(
            num=sha256(str(f_id).encode()).hexdigest()[:4] + md5(
                flag.encode()).hexdigest()[:4]))

        client = authorization(hostname, email, passwd)

        resp = client.get(
            'http://{hostname}:{port}/profile'.format(hostname=hostname,
                                                      port=PORT),
            timeout=TIME_OUT)
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        csrf_token = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken': csrf_token}

        files = {'picture': open(PIC_DIR + choice(FILES), 'rb')}

        resp = client.post(
            'http://{hostname}:{port}/profile/pic_edit'.format(
                hostname=hostname,
                port=PORT),
            data=payload,
            files=files,
            timeout=TIME_OUT)

        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        resp = check_an_avatar(hostname, client)
        print('Check avatar: \033[96m{status}\033[0m'.format(
            status=resp))
        if resp >= 400: raise MyException('Vse idet ko dnu')

        csrf_token = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken': csrf_token,
                   'search_text': user1_nick}

        resp = client.post(
            'http://{hostname}:{port}/search'.format(hostname=hostname,
                                                     port=PORT),
            data=payload,
            headers=dict(
                Referer='http://{hostname}:{port}/search'.format(
                    hostname=hostname,
                    port=PORT)),
            timeout=TIME_OUT)

        print('Search code: \033[96m{status}\033[0m'.format(
            status=resp.status_code))

        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')
        search_user = \
            re.findall(
                r'<a href="/profile/(\d+)">{name}'.format(name=user1_nick),
                resp.text)
        if not search_user:
            raise MyException('Vse idet ko dnu')

        search_user = search_user[0]

        resp = client.get(
            'http://{hostname}:{port}/profile/{user}/add_to_friend'.format(
                hostname=hostname,
                port=PORT,
                user=search_user),
            timeout=TIME_OUT)
        print('Add to friend code: \033[96m{status}\033[0m'.format(
            status=resp.status_code))
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        resp = client.get(
            'http://{hostname}:{port}/messages/{user}'.format(
                hostname=hostname,
                port=PORT,
                user=search_user),
            timeout=TIME_OUT)

        if flag in resp.content.decode():
            print('Get flag: %s' % flag)
        if resp.status_code >= 400: raise MyException('Vse idet ko dnu')

        print('\033[92mSuccess {}\033[0m'.format(STATUS_CODE['SUCCESS']))
        exit(STATUS_CODE['SUCCESS'])
    except requests.exceptions.Timeout:
        print('\033[96mMumble {}\033[0m'.format(STATUS_CODE['MUMBLE']))
        exit(STATUS_CODE['MUMBLE'])
    except requests.exceptions.ConnectionError:
        print('\033[93mDown {}\033[0m'.format(STATUS_CODE['DOWN']))
        exit(STATUS_CODE['DOWN'])
    except MyException:
        print('\033[91mCorrupt {}\033[0m'.format(STATUS_CODE['CORRUPT']))
        exit(STATUS_CODE['CORRUPT'])
    except Exception as error:
        print('Всё очень плохо :c ' + str(error))


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[2] == "put":
            put(argv[1], argv[3], argv[4])
        elif argv[2] == "check":
            check(argv[1], argv[3], argv[4])
    print('Invalid argvs')
    exit(STATUS_CODE['INVALID ARGVS'])

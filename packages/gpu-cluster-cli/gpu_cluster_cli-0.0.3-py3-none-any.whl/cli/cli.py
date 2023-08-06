import click
import requests
import json
import getpass
import pickle
import os
import sys
import re
import pkg_resources
from cli import config
from threading import Thread
from executor import execute
from terminaltables import SingleTable
from pyfiglet import Figlet

HOST = "http://" + config.HOST['host'] + ":" + str(config.HOST['port'])
COOKIEPATH = os.path.join(os.path.expanduser('~'), 'gpu_cli_cookie.txt')
MAX_GPU_PER_USER = 1

class MyException(Exception):
    pass

class LoginException(Exception):
    def __init__(self):
        super().__init__("Failed to get session info. Please log in.")

class PermissionException(Exception):
    def __init__(self):
        super().__init__("You have no permission.")

class ConnectionException(Exception):
    def __init__(self):
        super().__init__("Unable to connect API server.")


def save_cookie(session):
    with open(COOKIEPATH, 'wb') as f:
        pickle.dump(session.cookies, f)


def load_cookie(session):
    with open(COOKIEPATH, 'rb') as f:
        session.cookies.update(pickle.load(f))


def response_parser(response):
    if response.status_code == 401:
        raise LoginException
    elif response.status_code == 403:
        raise PermissionException
    elif response.status_code == 200:
        return json.loads(response.content)


def check_version():
    res = requests.get(url=HOST+"/auth/checkversion")

    if res.status_code == 200:
        curr_version = pkg_resources.require('gpu-cluster-cli')[0].version
        parsed_curr_version = list(map(int, curr_version.split(".")))
        req_version = json.loads(res.content)['version']
        parsed_req_version = list(map(int, req_version.split(".")))

        if parsed_curr_version < parsed_req_version:
            print("You should upgrade santa to version {}".format(req_version))
            sys.exit()

    else:
        raise ConnectionException


def check_login(session):
    try:
        load_cookie(session)
    except:
        raise LoginException

    res = session.get(url=HOST+"/auth/checksession")
    username = json.loads(res.content)['user']
    
    if username is None:
        raise LoginException

    print("User: {}".format(username))
    return username


def check_level(session):
    try:
        load_cookie(session)
    except:
        raise LoginException


    res = session.get(url=HOST+"/auth/checklevel")
    userlevel = json.loads(res.content)['level']

    if userlevel is None:
        raise LoginException

    return userlevel


def translate(message):
    message = message.replace("pod", "container")
    message = message.replace("Pod", "Container")
    message = message.replace("POD", "CONTAINER")
    return message


@click.group()
def cli():
    check_version()


@cli.command()
def register():
    username = None
    password = None
    password_re = None

    version = pkg_resources.require("gpu-cluster-cli")[0].version
    f = Figlet(font='banner3-D')
    print(f.renderText('Santa'))
    print("v. {}".format(version))

    print('-' * 18, '  Register  ', '-' * 18)
    print()

    while not username:
        username = input('Input username: ')

        if username == "unknown":
            print("Username 'unknown' is prohibited.")
            username = None

    while not password:
        password = getpass.getpass('Input password: ')

    while not password_re:
        password_re = getpass.getpass('Input password again: ')

    print()
    print('-' * 50)

    if password != password_re:
        print('Passwords does not match.')
    else:
        res = requests.post(
            url=HOST+"/auth/register",
            data={
                'username': username,
                'password': password
            })
        parsed_result = response_parser(res)

        if parsed_result is not None:
            print(parsed_result['message'])


@cli.command()
def login():
    version = pkg_resources.require("gpu-cluster-cli")[0].version
    f = Figlet(font='banner3-D')
    print(f.renderText('Santa'))
    print("v. {}".format(version))

    sess = requests.session()

    username = None
    password = None

    print('-' * 19, '  Login  ', '-' * 20)
    print()

    while not username:
        username = input('Input username: ')

    while not password:
        password = getpass.getpass('Input password: ')

    print()
    print('-' * 50)

    res = sess.post(
        url=HOST+"/auth/login",
        data={
            'username': username,
            'password': password
        })
    parsed_result = response_parser(res)

    if parsed_result is not None:
        print(parsed_result['message'])

    save_cookie(sess)


@cli.command()
def logout():
    sess = requests.session()
    username = check_login(sess)

    sess.get(url=HOST+"/auth/logout")
    os.remove(COOKIEPATH)

    print('User {} has logged out.'.format(username))
    print('-' * 50)


@cli.command()
def changepw():
    sess = requests.session()
    username = check_login(sess)

    curr_password = None
    new_password = None
    new_password_re = None

    print('-' * 14, '  Change password  ', '-' * 15)
    print()

    while not curr_password:
        curr_password = getpass.getpass('Input current password: ')

    while not new_password:
        new_password = getpass.getpass('Input new password: ')

    while not new_password_re:
        new_password_re = getpass.getpass('Input new password again: ')

    print()
    print('-' * 50)

    if new_password != new_password_re:
        print('New passwords does not match.')
    else:
        res = sess.post(
            url=HOST+"/auth/changepw",
            data={
                'curr_password': curr_password,
                'new_password': new_password
            })
        parsed_result = response_parser(res)

        if parsed_result is not None:
            print(parsed_result['message'])


@cli.command()
def changelevel():
    sess = requests.session()
    username = check_login(sess)
    userlevel = check_level(sess)

    if userlevel == 'admin':
        target_username = None
        target_userlevel = None

        print('-' * 13, '  Change user level  ', '-' * 14)
        print()

        while not target_username:
            target_username = input('Input username to change: ')

        while not target_userlevel:
            target_userlevel = input('Input user level (admin, superuser, normal): ')


        print()
        print('-' * 50)

        if target_userlevel in ['admin', 'superuser', 'normal']:
            res = sess.post(
                url=HOST+"/auth/changetype",
                data={
                    'username': target_username,
                    'usertype': target_userlevel
                })
            parsed_result = response_parser(res)

            if parsed_result is not None:
                print(parsed_result['message'])

        else:
            print("Invalid userlevel")

    else:
        raise PermissionException


@cli.command()
def deleteuser():
    sess = requests.session()
    username = check_login(sess)
    userlevel = check_level(sess)

    if userlevel == 'admin':
        target_username = None

        print('-' * 13, '  Change user level  ', '-' * 14)
        print()

        while not target_username:
            target_username = input('Input username to delete: ')

        check = input('Proceed to delete user [{}]? (yes/no): '.format(target_username))

        print()
        print('-' * 50)

        if check == "yes":
            res = sess.post(
                url=HOST+"/auth/deleteuser",
                data={
                    'username': target_username,
                })
            parsed_result = response_parser(res)

            if parsed_result is not None:
                print(parsed_result['message'])

    else:
        raise PermissionException


@cli.command()
def getinfo():
    sess = requests.session()
    username = check_login(sess)

    print('-' * 12, '  GPU, container Info  ', '-' * 13)
    print()

    res = sess.get(url=HOST+"/getinfo")
    parsed_result = response_parser(res)

    if parsed_result is not None:
        if parsed_result['status'] == 'Success':
            pod_data = [['#', 'user', 'container_name', 'container_id', 'ports', 'GPUs', 'status']]
            for i, pod in enumerate(parsed_result['pods']):
                pod_row = [i + 1]
                pod_row.extend(pod)
                pod_data.append(pod_row)
            pod_table = SingleTable(pod_data)
            pod_table.inner_row_border = True
            print("###", parsed_result['message'])
            print(pod_table.table)
            print()

            user_data = [['user', 'GPUs']]
            for k in parsed_result['userGPUs'].keys():
                user_data.append([k, parsed_result['userGPUs'][k]])
            user_table = SingleTable(user_data)
            print("### GPU usage per user")
            print(user_table.table)
            print()

            gpu_data = [
                ['In use', 'Total GPUs'],
                [parsed_result['using'], parsed_result['total']]
            ]
            gpu_table = SingleTable(gpu_data)
            print("### GPU status")
            print(gpu_table.table)

        else:
            print(translate(parsed_result['message']))


@cli.command()
def getgpu():
    sess = requests.session()
    username = check_login(sess)
    images = sorted([
        (
            "10.81.208.115:9000/lgcns/ai_workspace",
            "1.0_cuda9_cudnn7_tf1.8"
        ),
        (
            "nvidia/cuda",
            "9.0-cudnn7-devel-ubuntu16.04",
        ),
        (
            "nvidia/cuda",
            "8.0-cudnn6-devel-ubuntu16.04"
        )
    ])

    print('-' * 18, '  Get GPU  ', '-' * 19)
    print()

    info_res = sess.get(url=HOST+"/getinfo")
    parsed_info = response_parser(info_res)

    if parsed_info is not None:
        if parsed_info['status'] == 'Success':
            gpu_data = [
                ["In use", "Total GPUs"],
                [parsed_info['using'], parsed_info['total']]
            ]
            gpu_table = SingleTable(gpu_data)
            print("### GPU status")
            print(gpu_table.table)

            gpu_limit = min(MAX_GPU_PER_USER, parsed_info['total'] - parsed_info['using'])

            while True:
                try:
                    num_gpu = int(input('Input number of GPUs you need (0 ~ {}): '.format(gpu_limit)))

                    if num_gpu < 0:
                        raise ValueError
                    elif num_gpu > gpu_limit:
                        print("Insufficient GPUs.\n")
                    else:
                        print()
                        break
                except ValueError:
                    print("Invalid input.\n")

            image_data = [["#", "Repository", "Tag"]]

            for i, img in enumerate(images):
                image_data.append([i + 1, img[0], img[1]])

            image_table = SingleTable(image_data)
            image_table.inner_row_border = True
            print("### Images")
            print(image_table.table)

            image_count = len(images)

            while True:
                try:
                    image_idx = int(input('Select docker image (1 ~ {}): '.format(image_count)))

                    if image_idx < 1 or image_idx > image_count:
                        raise ValueError
                    else:
                        image_idx -= 1
                        print()
                        break
                except ValueError:
                    print("Invalid input.\n")

            pod_name_checker = re.compile(r'(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?')

            while True:
                pod_name = input('Input container name: ')

                if pod_name_checker.match(pod_name).group(1) == pod_name:
                    break
                else:
                    print("Container name must be an empty string or consist of alphanumeric characters, '-', '_' or '.'.")
                    print("And must start and end with an alphanumeric character.")
                    print("ex) 'MyValue',  or 'my_value',  or '12345'")
                    print()

            while True:
                ports_str = input((
                            "\nInput ports to use.\n"
                            "  SSH port 22 will be given in default.\n"
                            "  Ports should be between [1024 ~ 49151].\n"
                            "  Seperate ports by comma.\n"
                            "  ex) 6006,8888\n"
                            "ports: "))

                if ports_str:
                    try:
                        ports = set(map(int, ports_str.split(",")))

                        for port in ports:
                            if port < 1024 or port > 49151:
                                raise MyException

                        ports_param = ",".join(str(p) for p in ports)
                        print()
                        break

                    except (ValueError, MyException):
                        print("Invalid port.")

                else:
                    ports_param = None
                    break

            create_res = sess.post(
                url=HOST+"/getgpu",
                data={
                    'pod_name': pod_name,
                    'image': images[image_idx][0] + ":" + images[image_idx][1],
                    'num_gpu': num_gpu,
                    'ports': ports_param
                    })

            parsed_create = response_parser(create_res)

            if parsed_create is not None:
                print(translate(parsed_create['message']))
        else:
            print(translate(parsed_info['mesaage']))
        

@cli.command()
def returngpu():
    sess = requests.session()
    username = check_login(sess)

    print('-' * 17, '  Return GPU  ', '-' * 17)
    print()

    info_res = sess.get(url=HOST+"/getinfo")
    parsed_info = response_parser(info_res)

    if parsed_info is not None:
        if parsed_info['status'] == 'Success':
            pod_list = parsed_info['pods']

            pod_data = [['#', 'user', 'container_name', 'container_id', 'ports', 'GPUs', 'status']]
            for i, pod in enumerate(pod_list):
                pod_row = [i + 1]
                pod_row.extend(pod)
                pod_data.append(pod_row)
            pod_table = SingleTable(pod_data)
            pod_table.inner_row_border = True
            print("###", parsed_info['message'])
            print(pod_table.table)

            if pod_list:
                while True:
                    try:
                        pod_index = int(input("Select container (1~{}): ".format(len(pod_list))))

                        if pod_index < 1 or pod_index > len(pod_list):
                            raise MyException

                        pod_id = pod_list[pod_index-1][2]
                        break

                    except (ValueError, MyException):
                        print("Invalid input.\n")

                try:
                    delete_res = sess.get(
                            url=HOST+"/returngpu",
                            data={'pod_id': pod_id},
                            timeout=0.5)

                    parsed_delete = response_parser(delete_res)
                    print(translate(parsed_delete))

                except requests.exceptions.ReadTimeout:
                    print("Request for deleting container sent.")
                    print("It could take about a minute to clearly deleted.")

            else:
                print("No container to return.")

        else:
            print(translate(parsed_info['message']))


def main():
    try:
        cli()
    except (LoginException, PermissionException, ConnectionException) as e:
        print(e)
    except requests.exceptions.ConnectionError:
        print("Unable to connect API server.")
        sys.exit()

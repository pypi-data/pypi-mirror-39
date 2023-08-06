import click
import requests
import json
import getpass
import pickle
import os
import sys
import pkg_resources
from executor import execute
from terminaltables import AsciiTable
from threading import Thread

HOST = 'http://10.81.208.171:16384'
COOKIEPATH = os.path.join(os.path.expanduser('~'), 'gpu_cli_cookie.txt')

class MyException(Exception):
    pass


def save_cookie(session):
    with open(COOKIEPATH, 'wb') as f:
        pickle.dump(session.cookies, f)

def load_cookie(session):
    with open(COOKIEPATH, 'rb') as f:
        session.cookies.update(pickle.load(f))


def response_parser(response):
    if response.status_code == 401:
        print("You must log in first.")
        sys.exit()
    elif response.status_code == 403:
        print("You have no permission.")
        sys.exit()
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
            print("You should upgrade gpu-cli to version {}".format(req_version))
            sys.exit()

    else:
        print("Unable to connect API server.")
        sys.exit()


def check_login(session):
    try:
        load_cookie(session)
    except:
        print("Failed to get session info. Please login first.")
        sys.exit()

    res = session.get(url=HOST+"/auth/checksession")
    username = json.loads(res.content)['user']
    
    if username is None:
        print("Invalid user info. Please login again.")
        sys.exit()

    return username


def check_level(session):
    try:
        load_cookie(session)
    except:
        print("Failed to get session info. Please login first.")
        sys.exit()

    res = session.get(url=HOST+"/auth/checklevel")
    userlevel = json.loads(res.content)['level']

    if userlevel is None:
        print("Invalid user info. Please login again.")
        sys.exit()

    return userlevel


def translate(message):
    message = message.replace("pod", "container")
    message = message.replace("Pod", "Container")
    message = message.replace("POD", "CONTAINER")
    return message


@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
@click.option('--hostname')
@click.option('--user', default='root')
def open_ssh(hostname, user):
    execute('ssh %s@%s' % (user, hostname))


@cli.command()
def register():
    username = None
    password = None
    password_re = None

    print('-' * 18, '  Register  ', '-' * 18)
    print()

    while not username:
        username = input('Input username: ')

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

    print('User:', username)
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

        print('User:', username)
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
        print("You have no permission.")


@cli.command()
def deleteuser():
    sess = requests.session()
    username = check_login(sess)
    userlevel = check_level(sess)

    if userlevel == 'admin':
        target_username = None

        print('User:', username)
        print('-' * 13, '  Change user level  ', '-' * 14)
        print()

        while not target_username:
            target_username = input('Input username to delete')

        check = input('Proceed to delete user [{}]? (yes/no)'.format(target_username))

        print()
        print('-' * 50)

        if check == "yes":
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
        print("You have no permission.")


@cli.command()
def getinfo():
    sess = requests.session()
    username = check_login(sess)

    print('User:', username)
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
            pod_table = AsciiTable(pod_data)
            pod_table.inner_row_border = True
            print(pod_table.table)

            user_data = [['user', 'GPUs']]
            for k in parsed_result['userGPUs'].keys():
                user_data.append([k, parsed_result['userGPUs'][k]])
            user_table = AsciiTable(user_data)
            print(user_table.table)

            gpu_data = [
                ['In use', 'Total GPUs'],
                [parsed_result['using'], parsed_result['total']]
            ]
            gpu_table = AsciiTable(gpu_data)
            print(gpu_table.table)

        else:
            print(parsed_result['message'])


@cli.command()
def getgpu():
    sess = requests.session()
    username = check_login(sess)

    print('User:', username)
    print('-' * 18, '  Get GPU  ', '-' * 19)
    print()

    pod_name = input('Input container name: ')
    ports_str = input((
                "\nInput ports to use.\n"
                "  SSH port 22 will be given in default.\n"
                "  Ports should be between 1024 ~ 49151.\n"
                "  Seperate ports by comma.\n"
                "  ex) 6006,8888\n"
                "ports: "))
    print()

    if ports_str:
        try:
            ports = set(map(int, ports_str.split(",")))

            for port in ports:
                if port < 1024 or port > 49151:
                    raise MyException

            ports_param = ",".join(str(p) for p in ports)

        except (ValueError, MyException):
            print("Invalid port.")
            sys.exit()

    else:
        ports_param = None
 
    res = sess.post(
        url=HOST+"/getgpu",
        data={
            'pod_name': pod_name,
            'image': "10.81.208.115:9000/lgcns/ai_workspace:1.0_cuda9_cudnn7_tf1.8",
            'num_gpu': 1,
            'ports': ports_param
            })

    parsed_result = response_parser(res)

    if parsed_result is not None:
        print(translate(parsed_result['message']))
        

@cli.command()
def returngpu():
    sess = requests.session()
    username = check_login(sess)

    print('User:', username)
    print('-' * 17, '  Return GPU  ', '-' * 17)
    print()

    info_res = sess.get(url=HOST+"/getinfo")
    parsed_info = response_parser(info_res)

    if parsed_info is not None:
        if parsed_info['status'] == 'Success':
            pod_list = parsed_info['pods']

            pod_data = [['#', 'user', 'container_name', 'container_id', 'ports', 'GPUs']]
            for i, pod in enumerate(pod_list):
                pod_row = [i + 1]
                pod_row.extend(pod)
                pod_data.append(pod_row)
            pod_table = AsciiTable(pod_data)
            pod_table.inner_row_border = True
            print(pod_table.table)

            if pod_list:
                pod_index_str = input("Select container (1~{}) :".format(len(pod_list)))

                try:
                    pod_index = int(pod_index_str)
                    if pod_index < 1 or pod_index > len(pod_list):
                        raise MyException

                    pod_id = pod_list[pod_index-1][2]
                except (ValueError, MyException):
                    print("Invalid input.")
                    sys.exit()

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
            print(translate(parsed_info['message']))

    
def main():
    try:
        check_version()
        print('-' * 50)
        print(pkg_resources.require("gpu-cluster-cli")[0])
        cli()
    except requests.exceptions.ConnectionError:
        print("Unable to connect API server.")
        sys.exit()

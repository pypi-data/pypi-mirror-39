#!/usr/bin/env python
import sys
import os
import requests
import tarfile
import subprocess
import platform
import psutil
import threading
import socket
import exit
from pathlib import Path

username = ''
servername = ''

VERSION = sys.version_info.major

DATAPATH = '/usr/share/vpnkit/'

# for stop check internet timer
CHECK_STATUS = True

INTERNET_STATUS = False

CHECK_DEF_EXISTS = 'default'

if VERSION != 2:
    CHECK_DEF_EXISTS = bytes(CHECK_DEF_EXISTS, 'utf-8')


# Choosing action when  vpn tunnel up (exit or try new connection)
def NextChoose():

    global INTERNET_STATUS

    if VERSION == 2:
        choose = raw_input("Choose [close|new]: ") or 'new'
    else:
        choose = input("Choose [close|new]: ") or 'new'

    if choose == 'close':
        if INTERNET_STATUS:
            global CHECK_STATUS
            CHECK_STATUS = False
            exit.kill_proc('client.conf')
            exit.del_route(servername)
        sys.exit(1)

    elif choose == 'new':
        if INTERNET_STATUS:
            CHECK_STATUS = False
            exit.kill_proc('client.conf')
            exit.del_route(servername)
        exit.add_def_ip()
        start()

    elif choose != ' ':
        print("Operation '" + choose + "' not found")
        NextChoose()


# start openvpn and delete default route  from ip route table
def startOpenVpn():

    global servername
    check_up = 'Initialization Sequence Completed'

    if VERSION != 2:
        check_up = bytes(check_up, 'utf-8')

    exit.kill_proc('client.conf')
    exit.del_route(servername)

    print ("Your config must be in :" + DATAPATH)
    p = subprocess.Popen(['sudo', 'openvpn', '--config', DATAPATH + 'client.conf'], stdout=subprocess.PIPE)

    internet_on(servername)

    while True:
        output = p.stdout.readline()

        if output == '' and p.poll() is not None:
            break

        if output:
            print (output.strip().decode('utf-8'))

        if check_up in output:
            pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
            for line in pl.splitlines():
                if CHECK_DEF_EXISTS in line:
                    fields = line.strip().split()
                    global def_ip
                    def_ip = fields[2]
            d = subprocess.call(
                ['sudo', 'ip', 'route', 'del', 'default'],
                stdout=subprocess.PIPE)
            NextChoose()
            break


# getting certificates for openvpn from the server by username
def getCertificate(username, servername):
    try:
        # d = subprocess.call(['sudo','rm','-r','*.tar.gz'])
        req = requests.get('http://' + servername + '/download/' + username + '/', allow_redirects=True)
        if req.status_code == 200:
            open(username + '.tar.gz', 'wb').write(req.content)
            tar = tarfile.open(username + '.tar.gz', "r")
            tar.extractall()
            print('Certificates received')
            return True
        else:
            if req.content:
                data = req.json()
            else:
                print ('Error download certificates.Please check settings.')
            return False
    except Exception as e:
        print (e)
        print ('Error download certificates.Please check settings.')
        start()


def save_settings():
    settings = username + '\n' + servername + '\n'+def_ip.decode("utf-8")
    open(DATAPATH+'settings.ini', 'w').write(settings)


# start vpnkit client. User can choose action
def start():
    global username
    global servername

    if VERSION == 2:
        startChoose = raw_input("Choose operations[start(default)|new|settings|exit]: ").replace(" ", "") or 'start'
    else:
        startChoose = input("Choose operations[start(default)|new|settings|exit]: ").replace(" ", "") or 'start'

    if startChoose == 'new':

        if VERSION == 2:
            username = raw_input("Enter username: ").replace(" ", "")
            servername = raw_input("Enter server address: ").replace("http://", "")
        else:
            username = input("Enter username: ").replace(" ", "")
            servername = input("Enter server address: ").replace("http://", "")

        save_settings()

        result = getCertificate(username, servername)
        if result:
            startOpenVpn()
        elif not result:
            start()

    elif startChoose == 'start':
        result = getCertificate(username, servername)
        if result:
            startOpenVpn()
        elif not result:
            start()

    elif startChoose == 'exit':
        if INTERNET_STATUS:
            global CHECK_STATUS
            CHECK_STATUS = False
        sys.exit(1)

    elif startChoose == 'settings':
        print ('Username:' + username)
        print ('Server:' + servername)
        start()

    elif startChoose != ' ':
        print("Operation '" + startChoose + "' not found")
        start()


def internet_enter_on():
    #  check internet connection on start vpnkit
    try:
        requests.get('http://216.58.192.142', timeout=1)
        global INTERNET_STATUS
        INTERNET_STATUS = True
        return True
    except Exception as err:
        return False


def internet_on(servername):
    #  check internet connection
    global INTERNET_STATUS

    t = threading.Timer(3.0, internet_on,[servername])
    t.start()

    if not CHECK_STATUS:
        t.cancel()
    else:
        try:
            requests.get('http://216.58.192.142', timeout=1)
            INTERNET_STATUS = True
            return True
        except Exception as err:
            pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
            for line in pl.splitlines():
                if CHECK_DEF_EXISTS in line:
                    fields = line.strip().split()
                    global def_ip
                    def_ip = fields[2]
                    # delete default route to avoid several instance openvpn conflict
                    d = subprocess.call(
                        ['sudo', 'ip', 'route', 'del', 'default'],
                        stdout=subprocess.PIPE)

                    # add route for traffic to openvpn reconnect
                    p = subprocess.call(
                        ['sudo', 'ip', 'route', 'add', servername, 'via', def_ip],
                        stdout=subprocess.PIPE)
            INTERNET_STATUS = False
            return False
        except socket.timeout as e:
            pass


def get_settings():
    global username
    global servername
    global def_ip
    settings_file = DATAPATH + 'settings.ini'
    file = Path(DATAPATH + 'settings.ini')

    pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if CHECK_DEF_EXISTS in line:
            fields = line.strip().split()
            def_ip = fields[2]

    # check if file exists and it's empty
    if file.is_file() and os.stat(settings_file).st_size != 0:
        with open(DATAPATH + 'settings.ini') as fp:
                settings = fp.read().splitlines()
                username = settings[0]
                servername = settings[1]
    else:
        open(DATAPATH+'settings.ini', 'w').write(username + '\n' + servername + '\n' + def_ip.decode("utf-8"))

# check vpnkit already starts  or not
def check_start_status():
    proc_name = 'vpnkit'
    count_proc = 0
    if VERSION != 2:
        proc_name = bytes(proc_name, 'utf-8')

    pl = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if proc_name in line:
            count_proc += 1
    if count_proc > 4:
        print ("VpnKit is already started")
        sys.exit(1)


def main():
    # check internet connection status for start openvpn
    result = internet_enter_on()
    # check vpnkit already starts  or not
    check_start_status()
    if result:
        get_settings()
        # change dir . Openvpn can find certificates.
        os.chdir(DATAPATH)
        start()
    else:
        print("No internet connection or you were disconnected")
        sys.exit(1)


if __name__ == '__main__':
    main()

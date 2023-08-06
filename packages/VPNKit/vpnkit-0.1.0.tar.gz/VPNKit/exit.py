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

DATAPATH = '/usr/share/vpnkit/'

VERSION = sys.version_info.major

DEF_IP = '192.168.1.1'


#adding default route for up connection
def add_def_ip():
    global DEF_IP
    def_ip_exists = False
    check_def_exists = 'default'
    if VERSION != 2:
        check_def_exists = bytes(check_def_exists, 'utf-8')

    pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if check_def_exists in line:
            def_ip_exists = True
    if not def_ip_exists:
        p = subprocess.call(
            ['sudo', 'ip', 'route', 'add', 'default', 'via', DEF_IP],
            stdout=subprocess.PIPE)
        print('Default connection up')


# get pid of necessary process
def get_proc_pid(p):
    pid = p.pid
    return str(pid)


def get_procs_by_pid(pids, include_self=True):
    procs = []
    for p in psutil.process_iter():
        if (get_proc_pid(p) in pids and
                (os.getpid() != p.pid or include_self)):
            procs.append(p)
    return procs


def kill_proc(name, timeout=1):
    pl = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE).communicate()[0]
    pids = []
    if VERSION != 2:
        name = bytes(name, 'utf-8')
    for line in pl.splitlines():
        if name in line:
            pids.append((line.split()[1]).decode("utf-8"))
    if len(pids) != 0:
        procs = get_procs_by_pid(pids, include_self=False)

        if len(procs) > 0:
            for p in procs:
                p.kill()
            _, procs = psutil.wait_procs(procs)

        if len(procs) > 0:
            print('Failed')
        else:
            print('Process openvpn kill')


def del_route(route):
    d = subprocess.call(
        ['sudo', 'ip', 'route', 'del', route ],
        stdout=subprocess.PIPE)


def main():
    global DEF_IP

    with open(DATAPATH + 'settings.ini') as fp:
        settings = fp.read().splitlines()
        DEF_IP = settings[2]

    try:
        kill_proc('client.conf')
    except Exception as e:
        print(e)
        print('Process openvpn  don\'t kill')
    add_def_ip()


if __name__ == '__main__':
    main()

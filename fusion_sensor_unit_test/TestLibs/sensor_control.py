#!/usr/bin/env python

import socket
import time
import os
import sys


class bcolors:
    COMMAND = '\033[94m'
    REPLY = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./sensor_control.py HOSTNAME PORTNUMBER \n this program is to remotely control the worker modules of fusion sensor"
        sys.exit(0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    sock.connect((host, port))
    while True:
        sys.stdout.write(bcolors.COMMAND + '>>> ' + bcolors.ENDC)
        cmd = sys.stdin.readline()
        if cmd == "exit\n":
            break
        sock.send(cmd)
        buf = sock.recv(1024)
        buf = buf.replace("STATE_STARTED", bcolors.OKGREEN + "STATE_STARTED" + bcolors.ENDC)
        buf = buf.replace("true", bcolors.OKGREEN + "true" + bcolors.ENDC)
        buf = buf.replace("STATE_STOPPED", bcolors.FAIL + "STATE_STOPPED" + bcolors.ENDC)
        buf = buf.replace("false", bcolors.FAIL + "false" + bcolors.ENDC)
        buf = buf.replace("null", bcolors.FAIL + "null" + bcolors.ENDC)
        buf = buf.replace("EOM", '')
        print bcolors.REPLY + "<<<\n" + bcolors.ENDC + buf
    sock.close()

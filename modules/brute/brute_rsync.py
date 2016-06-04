#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
from lib.rsynclib import *
import time
import socket
import re


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'rsync brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check rsync password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.rsync_connect(ip, port, username, password)
        return

    def get_ver(self, host):
        debugging = 0
        r = rsync(host)
        r.set_debuglevel(debugging)
        return r.server_protocol_version

    def rsync_connect(self, ip, port, username, password):
        creak = 0
        try:
            ver = self.get_ver(ip)  # get rsync module
            fp = socket.create_connection((ip, port), timeout=8)
            fp.recv(99)

            fp.sendall(ver.strip('\r\n')+'\n')
            time.sleep(3)
            fp.sendall('\n')
            resp = fp.recv(99)

            modules = []
            for line in resp.split('\n'):
                modulename = line[:line.find(' ')]
                if modulename:
                    if modulename != '@RSYNCD:':
                        modules.append(modulename)

            if len(modules) != 0:
                for modulename in modules:
                    self.alert("find %s module in %s at %s" % (modulename, ip, port))

                    rs = rsync(ip)
                    res = rs.login(module=modulename, user=username, passwd=password)
                    if re.findall('.*OK.*', res):
                        rs.close()
                        creak = 1
                        self.alert('rsync login successful:%s:%s:%s:%s:%s' % (ip, port, modulename, username, password))
                    if re.findall('.*Unknown.*', res):
                        creak = 2
            else:
                creak = 3

        except Exception, e:
            pass
        return creak

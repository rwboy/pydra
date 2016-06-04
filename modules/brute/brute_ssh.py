#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import paramiko


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 22, True, 'the target host port')
        self.register_option('username', 'root', True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'ssh brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check ssh password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.ssh_connect(ip, port, username, password)
        return

    def ssh_connect(self, ip, port, username, password):
        self.verbose('trying brute ssh:%s:%s:%s:%s' % (ip, port, username, password))
        crack = 0
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password)
            crack = 1
            self.alert('ssh login successful:%s:%s:%s:%s' % (ip, port, username, password))
            client.close()
        except Exception, e:
            if e[0] == 'Authentication failed.':
                self.verbose("%s ssh service 's %s:%s login fail " % (ip, username, password))
            else:
                self.verbose("connect %s ssh service at %s login fail " % (ip, port))
                crack = 2
        return crack

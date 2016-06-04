#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
from lib.vnclib import *


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 5900, True, 'the target host port')
        self.register_option('pass', 'password', True, 'the password that you want to check')
        self.info = {
            'Name': 'vnc brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check vnc password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        password = self.options['pass']
        self.vnc_connect(ip, port,  password)
        return

    def vnc_connect(self, ip, port, password):
        crack = 0
        try:
            v = VNC()
            v.connect(ip, port, 10)
            code, mesg = v.login(password)
            if mesg == 'OK':
                self.alert('vnc login successful: %s:%s:%s' % (ip, port, password))
                crack = 1
        except Exception, e:
            crack = 2
            self.debug(e)
            pass
        return crack

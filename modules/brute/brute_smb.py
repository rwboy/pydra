#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
from impacket.smbconnection import *


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 445, False, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'smb brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check smb password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.smb_connect(ip, port, username, password)
        return

    def smb_connect(self, ip, port, username, password):
        self.verbose('trying smb brute:%s:%s:%s:%s' % (ip, port, username, password))
        crack = 0
        try:
            smb1 = SMBConnection('*SMBSERVER', ip)
            smb1.login(username, password)
            smb1.logoff()
            self.alert('smb login successful:%s:%s:%s:%s' % (ip, port, username, password))
            crack = 1
        except Exception, e:
            self.debug("%s smb 's %s:%s login fail: %s " % (ip, username, password, e))
        return crack

#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
from ftplib import FTP
import core.framework


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 21, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, False, 'the password that you want to check')
        self.info = {
            'Name': 'ftp brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check ftp password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.ftp_connect(ip, port, username, password)
        return

    def ftp_connect(self, ip, port, username, password):
        try:
            self.verbose('trying brute ftp %s:%s:%s:%s' % (ip, port, username, password))
            f = FTP()
            f.connect(ip, str(port))
            f.login(user=username, passwd=password)
            banner = self.to_unicode(f.getwelcome())
            n_list = self.to_unicode(f.nlst())
            self.alert('ftp login successful at %s:%s:%s:%s' % (ip, port, username, password))
            f.close()
        except Exception, e:
            self.debug(e)

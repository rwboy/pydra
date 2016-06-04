#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import pymssql


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'mssql brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check mssql password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.mssql_connect(ip, port, username, password)
        return

    def mssql_connect(self, ip, port, username, password):
        crack = 0
        try:
            db = pymssql.connect(host=str(ip)+':'+str(port), user=username, password=password)
            if db:
                crack = 1
                self.alert('mssql brute successful:%s:%s:%s:%s' % (ip, port, username, password))
            db.close()
        except Exception, e:
            self.debug("%s sql service 's %s:%s login fail! %s " % (ip, username, password, e))
        return crack


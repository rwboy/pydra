#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import MySQLdb


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 3306, True, 'the target host port')
        self.register_option('username', 'root', True, 'the target username')
        self.register_option('pass', None, False, 'the password that you want to check')
        self.info = {
            'Name': 'mysql brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check mysql password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.mysql_connect(ip, port, username, password)
        return

    def mysql_connect(self, ip, port, username, password):
        crack = 0
        self.verbose('trying brute mysql: %s:%s:%s:%s' % (ip, port, username, password))
        try:
            db = MySQLdb.connect(ip, username, str(password), port=port)
            if db:
                self.alert('mysql login successful: %s:%s:%s:%s' % (ip, port, username, password))
                crack = 1
            db.close()
        except Exception, e:
            if e[0] == 1045:
                self.verbose("%s mysql's %s:%s login fail:%s" % (ip, username, password, e))
            else:
                self.verbose("connect %s mysql service at %s login fail:%s " % (ip, port, e))
                crack = 2
        return crack

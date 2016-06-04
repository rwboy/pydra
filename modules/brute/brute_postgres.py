#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import psycopg2
import re


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 5432, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, False, 'the password that you want to check')
        self.info = {
            'Name': 'postgres brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check postgres password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.postgres_connect(ip, port, username, password)
        return

    def postgres_connect(self, ip, port, username, password):
        crack = 0
        self.verbose('trying brute postgers %s:%s:%s:%s' % (ip, port, username, password))
        try:
            db = psycopg2.connect(user=username, password=password, host=ip, port=port)
            if db:
                self.alert('postgres login successful: %s:%s:%s:%s' % (ip, port, username, password))
                crack = 1
            db.close()
        except Exception, e:
            if re.findall(".*Password.*", e[0]):
                self.verbose("%s postgres's %s:%s login fail: %s" %(ip, username, password, e))
                crack = 2
            else:
                self.verbose("connect %s postgres service at %s login fail: %s " %(ip, port, e))
                crack = 3
            pass
        return crack

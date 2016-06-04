#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import pymongo


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'mongodb brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check mongodb password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.mongodb_connect(ip, port, username, password)
        return

    def mongodb_connect(self, ip, port, username, password):
        crack = 0
        db = None
        try:
            self.verbose('trying mongodb %s:%s:%s:%s' % (ip, port, username, password))
            connection = pymongo.Connection(ip, port)
            db = connection.admin
            db.collection_names()
            self.alert('%s mongodb service at %s allow login Anonymous login!!\r\n' % (ip, port))
            crack = 1

        except Exception, e:
            if e[0] == 'database error: not authorized for query on admin.system.namespaces':
                try:
                    r = db.authenticate(username, password)
                    if r:
                        crack = 2
                    else:
                        crack = 3
                        print "%s mongodb service 's %s:%s login fail " % (ip, username, password)
                except Exception, e:
                    pass

            else:
                self.debug('%s mongodb service at %s not connect' % (ip, port))
                crack = 4
        return crack

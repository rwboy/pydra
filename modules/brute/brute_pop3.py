#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import poplib


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'pop3 brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'pop3 ftp password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.pop3_connect(ip, port, username, password)
        return

    def pop3_connect(self, ip, port, username, password):
        try:
            pp = poplib.POP3(ip)
            #pp.set_debuglevel(1)
            pp.user(username)
            pp.pass_(password)
            (mail_count, size) = pp.stat()
            pp.quit()
            if mail_count:
                self.alert("%s pop3 at %s has weaken password!!-------%s:%s\r\n" % (ip, port, username, password))
        except Exception, e:
            self.debug("%s pop3 service 's %s:%s login fail:%s " % (ip, username, password, e))
            pass

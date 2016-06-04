#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific package
import core.framework
import telnetlib


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', 23, True, 'the target host port')
        self.register_option('username', 'root', True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'telnet brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check telnet password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.telnet_connect(ip, port, username, password)
        return

    def telnet_connect(self, ip, port, username, password):
        crack = 0
        try:
            self.verbose('trying telnet brute:%s:%s:%s:%s' % (ip, port, username, password))
            finish = ':~$ '
            tn = telnetlib.Telnet(ip, port, timeout=10)
            tn.set_debuglevel(2)
            tn.read_until('login: ')
            tn.write(username + '\n')
            tn.read_until('password: ')
            tn.write(password + '\n')
            tn.read_until(finish)
            tn.write('ls\n')
            crack = 1
            self.alert('telnet login successful:%s:%s:%s:%s' % (ip, port, username, password))
            tn.read_until(finish)
            tn.close()
        except Exception, e:
            crack = 2
            self.debug('telnet login failed:%s:%s:%s:%s:%s' % (ip, port, username, password, e))
            pass
        return crack

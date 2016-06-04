#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
import ldap


class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
        self.info = {
            'Name': 'ldap brute module',
            'Author': 'Mohism',
            'Version': 'v0.0.1',
            'Description': 'check ldap password'
            }

    def module_pre(self):
        value = None
        return value

    def module_run(self):
        ip = self.options['host']
        port = self.options['port']
        username = self.options['username']
        password = self.options['pass']
        self.ldap_connect(ip, port, username, password)
        return

    def ldap_connect(self, ip, username, password, port):
        try:
            ldap_path = 'ldap://'+ip+':'+port+'/'
            l = ldap.initialize(ldap_path)
            re = l.simple_bind(username, password)
            if re == 1:
                self.alert('ldap successful at %s:%s:%s:%s' % (ip, port, username, password))
        except Exception, e:
            if e[0]['desc'] == "Can't contact LDAP server":
                self.debug("Can't contact LDAP server")
            pass

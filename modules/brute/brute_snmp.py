#!/usr/bin/env python
# !-*- coding: utf-8 -*-
# packages required for framework integration
import core.module
# module specific packages
import core.framework
from pysnmp.entity.rfc3413.oneliner import cmdgen

class Module(core.module.Module):
    def __init__(self, params):
        core.module.Module.__init__(self, params)
        self.register_option('host', None, True, 'the target host ip')
        self.register_option('port', None, True, 'the target host port')
        self.register_option('username', None, True, 'the target username')
        self.register_option('pass', None, True, 'the password that you want to check')
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

    def snmp_connect(self,ip,key):
        crack =0
        try:
            errorIndication, errorStatus, errorIndex, varBinds =\
                cmdgen.CommandGenerator().getCmd(
                    cmdgen.CommunityData('my-agent',key, 0),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    (1,3,6,1,2,1,1,1,0)
                )
            if varBinds:
                crack=1
        except:
            pass
        return crack

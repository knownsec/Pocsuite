#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os
import ast
import json
import urllib
import getpass
try:
    from pocsuite.lib.request.basic import req as requests
except:
    import requests
import ConfigParser
from .rcGen import initial


class ZoomEye():
    def __init__(self, confPath=None):
        self.plan = self.token = None
        self.headers = self.username = self.password = None
        self.resources = {}

        if confPath:
            self.confPath = confPath
            self.parser = ConfigParser.ConfigParser()
            self.parser.read(self.confPath)
            try:
                self.username = self.parser.get('Telnet404', 'Account')
                self.password = self.parser.get('Telnet404', 'Password')
            except:
                pass

    def newToken(self):
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username, self.password)
        try:
            req = requests.post('https://api.zoomeye.org/user/login', data=data, )
            content = json.loads(req.content)
            if req.status_code != 401 and "access_token" in content:
                self.token = content['access_token']
                self.headers = {'Authorization': 'JWT %s' % self.token}
                return True
        except Exception as ex:
            pass
        return False

    def resourceInfo(self):
        req = requests.get('https://api.zoomeye.org/resources-info', headers=self.headers, )
        content = json.loads(req.content)
        if 'plan' in content:
            self.plan = content['plan']
            self.resources['web-search'] = content['resources']['web-search']
            self.resources['host-search'] = content['resources']['host-search']
            return True
        return False

    def search(self, dork, page=1, resource='web'):
        req = requests.get(
            'https://api.zoomeye.org/{}/search?query={}&page={}&facet=app,os'.format(resource, urllib.quote(dork), page + 1),
            headers=self.headers
        )
        content = json.loads(req.content)
        if 'matches' in content:
            if resource == 'web':
                return [match['site'] for match in content['matches']]
            else:
                anslist = []
                for match in content['matches']:
                    ans = match['ip']
                    if 'portinfo' in match:
                        ans += ':' + str(match['portinfo']['port'])
                    anslist.append(ans)
                return anslist
        else:
            return []

    def write_conf(self):
        if not self.parser.has_section("Telnet404"):
            self.parser.add_section("Telnet404")

        username = raw_input("Telnet404 email account:")
        password = getpass.getpass("Telnet404 password:")
        self.parser.set("Telnet404", "Account", username)
        self.parser.set("Telnet404", "Password", password)
        self.username = username
        self.password = password
        self.parser.write(open(self.confPath, "w"))


class Seebug():
    def __init__(self, confPath=None):
        self.headers = self.username = self.password = None

        if confPath:
            self.confPath = confPath
            self.parser = ConfigParser.ConfigParser()
            self.parser.read(self.confPath)
            try:
                self.username = self.parser.get('Telnet404', 'Account')
                self.password = self.parser.get('Telnet404', 'Password')
            except:
                pass

    def newToken(self):
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username, self.password)
        try:
            req = requests.post('https://api.zoomeye.org/user/login', data=data, )
            content = json.loads(req.content)
            if req.status_code != 401 and "access_token" in content:
                self.token = content['access_token']
                self.headers = {'Authorization': 'JWT %s' % self.token}
                return True
        except Exception as ex:
            pass
        return False

    def static(self):
        req = requests.get('https://www.seebug.org/api/user/poc_list', headers=self.headers)
        self.stats = ast.literal_eval(req.content)
        if 'detail' in self.stats:
            return False
        return 'According to record total %s PoC purchased' % len(self.stats)

    def seek(self, keyword):
        req = requests.get('https://www.seebug.org/api/user/poc_list?q=%s' % keyword, headers=self.headers, )
        self.pocs = ast.literal_eval(req.content)
        return '%s purchased poc related to keyword "%s"' % (len(self.pocs), keyword)

    def retrieve(self, ID):
        req = requests.get('https://www.seebug.org/api/user/poc_detail?id=%s' % ID, headers=self.headers, )
        try:
            ret = ast.literal_eval(req.content)
        except:
            ret = json.loads(req.content)
        return ret

    def write_conf(self):
        if not self.parser.has_section("Telnet404"):
            self.parser.add_section("Telnet404")

        username = raw_input("Telnet404 email account:")
        password = getpass.getpass("Telnet404 password:")
        self.parser.set("Telnet404", "Account", username)
        self.parser.set("Telnet404", "Password", password)
        self.username = username
        self.password = password
        self.parser.write(open(self.confPath, "w"))

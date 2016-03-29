#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os
import ast
import json
import urllib
import requests
import ConfigParser

currentUserHomePath = os.path.expanduser('~')

def initial():
    _ = """[zoomeye]\nusername = Your ZoomEye Username\npassword = Your ZoomEye Password\n\n[token]\nseebug = Your Seebug Token"""
    if not os.path.isfile(currentUserHomePath + '/.pocsuiterc'):
        with open(currentUserHomePath + '/.pocsuiterc', 'w') as fp:
            fp.write(_)

initial()


class ZoomEye():
    def __init__(self, confPath=currentUserHomePath + '/.pocsuiterc'):
        self.confPath = confPath
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.confPath)

        self.username = self.parser.get('zoomeye', 'Username')
        self.password = self.parser.get('zoomeye', 'Password')

        self.plan = None
        self.token = None
        self.headers = None
        self.resources = {}

    def newToken(self):
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username, self.password)
        req = requests.post('http://api.zoomeye.org/user/login', data=data)
        content = json.loads(req.content)
        if req.status_code != 401 and "access_token" in content:
            self.token = content['access_token']
            self.headers = {'Authorization': 'JWT %s' % self.token}
            return True
        return False

    def resourceInfo(self):
        req = requests.get('http://api.zoomeye.org/resources-info', headers=self.headers)
        content = json.loads(req.content)
        if 'plan' in content:
            self.plan = content['plan']
            self.resources['web-search'] = content['resources']['web-search']
            self.resources['host-search'] = content['resources']['host-search']
            return True
        return False

    def search(self, dork, page=1, resource='web'):
        req = requests.get('http://api.zoomeye.org/{}/search?query="{}"&page={}&facet=app,os'\
                        .format(resource, urllib.quote(dork), page + 1), headers=self.headers)
        content = json.loads(req.content)
        if 'matches' in content:
            return [match['ip'] for match in content['matches']]
        else:
            return []

    def write_conf(self):
        if not self.parser.has_section("zoomeye"):
            self.parse.add_section("zoomeye")

        username = raw_input("ZoomEye Email:")
        password = raw_input("ZoomEye Password:")
        self.parser.set("zoomeye", "Username", username)
        self.parser.set("zoomeye", "Password", password)
        self.username = username
        self.password = password
        self.parser.write(open(self.confPath, "r+"))


class Seebug():
    def __init__(self, confPath=currentUserHomePath + '/.pocsuiterc'):
        self.confPath = confPath
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.confPath)

        self.token = self.parser.get('token', 'seebug')
        self.headers = {'Authorization': 'Token %s' % self.token}

    def static(self):
        req = requests.get('https://www.seebug.org/api/user/poc_list', headers=self.headers)
        self.stats = ast.literal_eval(req.content)
        if 'detail' in self.stats:
            return False
        return 'According to record total %s PoC purchased' % len(self.stats)

    def seek(self, keyword):
        req = requests.get('https://www.seebug.org/api/user/poc_list?q=%s' % keyword, headers=self.headers)
        # [{"id", "name"}]
        # {"detail": msg}
        self.pocs = ast.literal_eval(req.content)
        return '%s purchased poc related to keyword "%s"' % (len(self.pocs), keyword)

    def retrieve(self, ID):
        req = requests.get('https://www.seebug.org/api/user/poc_detail?id=%s' % ID, headers=self.headers)
        # {"code", "name"}
        return ast.literal_eval(req.content)

    def write_conf(self):
        if not self.parser.has_section("token"):
            self.parse.add_section("token")

        token = raw_input("Seebug Token:")
        self.parser.set("token", "seebug", token)
        self.token = token
        self.parser.write(open(self.confPath, "r+"))


if __name__ == "__main__":
    a = ZoomEye()
    # print a.resourceInfo()
    print a.newToken()
    # a.search('port:21')

    # b = Seebug()
    # b.static()
    # b.seek('redis')
    # b.retrieve(89339)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import ast
import json
import requests
import ConfigParser


class ZoomEye():
    def __init__(self, confPath='conf.ini'):
        self.confPath = confPath
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.confPath)
        self.token = self.parser.get('token', 'zoomeye')

        self.plan = None
        self.resources = {}
        self.headers = {'Authorization': 'JWT %s' % self.token}

    def newToken(self, user='zuile@qq.com', pwd='zuile'):
        data = '{{"username": "{}", "password": "{}"}}'.format(user, pwd)
        req = requests.post('http://api.zoomeye.org/user/login', data=data)
        content = json.loads(req.content)
        if req.status_code != 401 and "access_token" in content:
            self.token = content['access_token']
            self.parser.set('token', 'zoomeye', self.token)
            self.parser.write(open(self.confPath, 'w'))

        return self.token

    def resourceInfo(self):
        req = requests.get('http://api.zoomeye.org/resources-info', headers=self.headers)
        content = json.loads(req.content)
        if 'plan' in content:
            self.plan = content['plan']
            self.resources['whois'] = content['resources']['whois']
            self.resources['web-search'] = content['resources']['web-search']
            self.resources['host-search'] = content['resources']['host-search']

        return self.resources

    def search(self, dork, resource='web'):
        req = requests.get('http://api.zoomeye.org/{}/search?query="{}"&page=1&facet=app,os'\
                        .format(resource, dork), headers=self.headers)
        content = json.loads(req.content)
        if 'matches' in content:
            return [match['ip'] for match in content['matches']]


class Seebug():
    def __init__(self, confPath='conf.ini'):
        self.confPath = confPath
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.confPath)

        self.token = self.parser.get('token', 'seebug')
        self.headers = {'Authorization': 'Token %s' % self.token}

    def static(self):
        req = requests.get('https://www.seebug.org/api/user/poc_list', headers=self.headers)
        self.stats = ast.literal_eval(req.content)
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


if __name__ == "__main__":
    a = ZoomEye()
    # print a.resourceInfo()
    # print a.newToken()
    # a.search('port:21')

    b = Seebug()
    # b.static()
    # b.seek('redis')
    # b.retrieve(89339)

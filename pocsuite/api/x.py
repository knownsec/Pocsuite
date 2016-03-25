#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
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
        self.headers = {'Authorization': 'JWT %s' % self.token}

    def static():
        pass

    def fetchPoC():
        pass


if __name__ == "__main__":
    a = ZoomEye()
    print a.resourceInfo()
    print a.newToken()
    # a.search('port:21')

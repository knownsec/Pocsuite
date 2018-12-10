#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""


import requests
import getpass


class ZoomEye(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

        self.token = ''
        self.zoomeye_login_api = "https://api.zoomeye.org/user/login"
        self.zoomeye_dork_api = "https://api.zoomeye.org/{}/search"

    def login(self):
        """Please access https://www.zoomeye.org/api/doc#login
        """
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username,
                                                               self.password)
        resp = requests.post(self.zoomeye_login_api, data=data)
        if resp and resp.status_code == 200 and 'access_token' in resp.json():
            self.token = resp.json().get('access_token')
        return self.token

    def dork_search(self, dork, page=0, resource='web', facet=['ip']):
        """Search records with ZoomEye dorks.

        param: dork
               ex: country:cn
               access https://www.zoomeye.org/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """
        result = []
        if isinstance(facet, (tuple, list)):
            facet = ','.join(facet)

        zoomeye_api = self.zoomeye_dork_api.format(resource)
        headers = {'Authorization': 'JWT %s' % self.token}
        params = {'query': dork, 'page': page + 1, 'facet': facet}
        resp = requests.get(zoomeye_api, params=params, headers=headers)
        if resp and resp.status_code == 200 and 'matches' in resp.json():
            matches = resp.json().get('matches')
            # total = resp.json().get('total')  # all matches items num
            result = matches

            # Every match item incudes the following information:
            # geoinfo
            # description
            # check_time
            # title
            # ip
            # site
            # system
            # headers
            # keywords
            # server
            # domains

        return result

    def resources_info(self):
        """Resource info shows us available search times.

        host-search: total number of available host records to search
        web-search: total number of available web records to search
        """
        data = None
        zoomeye_api = "https://api.zoomeye.org/resources-info"
        headers = {'Authorization': 'JWT %s' % self.token}
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'plan' in resp.json():
            data = resp.json()

        return data


def show_site_ip(data):
    if data:
        for i in data:
            print(i.get('site'), i.get('ip'))


def show_ip_port(data):
    if data:
        for i in data:
            print(i.get('ip'), i.get('portinfo').get('port'))


def zoomeye_api_test():
    zoomeye = ZoomEye()
    zoomeye.username = raw_input('ZoomEye Username: ')
    zoomeye.password = getpass.getpass(prompt='ZoomEye Password: ')
    zoomeye.login()
    print(zoomeye.resources_info())

    data = zoomeye.dork_search('solr')
    show_site_ip(data)

    data = zoomeye.dork_search('country:cn')
    show_site_ip(data)

    data = zoomeye.dork_search('solr country:cn')
    show_site_ip(data)

    data = zoomeye.dork_search('solr country:cn', resource='host')
    show_ip_port(data)


# zoomeye_api_test()

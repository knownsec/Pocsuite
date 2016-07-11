#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""


import requests
import ast


class Seebug(object):
    def __init__(self, token=None):
        """Seebug api needs a valid token from https://www.seebug.org/.
        """
        self.token = token
        self.seebug_poclist_api = 'https://www.seebug.org/api/user/poc_list'
        self.seebug_pocinfo_api = 'https://www.seebug.org/api/user/poc_detail'

    def poc_search(self, keyword=None):
        """Search poc(s) with seebug keyword

        param: keyword
               if no keyword is specified, poc(s) list will return,
               if a valid keyword, specific poc(s) will return.
        """
        pocs = []
        headers = {'Authorization': 'Token {}'.format(self.token)}
        resp = requests.get(self.seebug_poclist_api, params={'q': keyword},
                            headers=headers)

        if resp and resp.status_code == 200:
            pocs = ast.literal_eval(resp.content)
        return pocs

    def poc_list(self):
        """Get available poc(s) related to the seebug api
        """
        return self.poc_search()  # no keyword will return poc(s) list

    def poc_detail(self, ssvid):
        """Get the poc details by ssvid. The details include code and name.

        param: ssvid
               a ssvid, a seebug poc.
               ex: https://www.seebug.org/vuldb/ssvid-89715, 89715 is a ssvid.
        """
        detail = None
        headers = {'Authorization': 'Token {}'.format(self.token)}
        resp = requests.get(self.seebug_pocinfo_api, params={'id': int(ssvid)},
                            headers=headers)
        if resp and resp.status_code == 200:
            detail = resp.json()
        return detail

    def poc_code(self, ssvid):
        """Get the poc code by ssvid

        param: ssvid
               a ssvid, a seebug poc.
               ex: https://www.seebug.org/vuldb/ssvid-89715, 89715 is a ssvid.
        """
        code = None
        detail = self.poc_detail(ssvid)
        if detail and 'code' in detail:
            code = detail.get('code')
        return code


def seebug_api_test():
    seebug = Seebug()
    seebug.token = raw_input('[*] Seebug API Token: ')
    print seebug.poc_search('redis')
    print seebug.poc_list()
    print seebug.poc_detail(89715)
    print seebug.poc_code(89715)


# seebug_api_test()

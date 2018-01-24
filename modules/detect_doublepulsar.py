#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import socket

from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
from pocsuite.api.utils import url2ip


class TestPOC(POCBase):
    name = "Doublepulsar后门"
    vulID = ''
    author = ['seebug']
    vulType = 'Buffer Overflow'
    version = '1.0'
    references = ['http://paper.seebug.org/279/']
    desc = '''Doublepulsar backdoor'''

    vulDate = ''
    createDate = '2017-04-14'
    updateDate = '2016-04-14'

    appName = 'Windows'
    appVersion = '2003'
    appPowerLink = ''
    samples = []

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        """verify mode"""
        # Packets
        negotiate_protocol_request = binascii.unhexlify(
            "00000085ff534d4272000000001853c00000000000000000000000000000fffe00004000006200025043204e4554574f524b2050524f4752414d20312e3000024c414e4d414e312e30000257696e646f777320666f7220576f726b67726f75707320332e316100024c4d312e325830303200024c414e4d414e322e3100024e54204c4d20302e313200")
        session_setup_request = binascii.unhexlify(
            "00000088ff534d4273000000001807c00000000000000000000000000000fffe000040000dff00880004110a000000000000000100000000000000d40000004b000000000000570069006e0064006f007700730020003200300030003000200032003100390035000000570069006e0064006f007700730020003200300030003000200035002e0030000000")
        tree_connect_request = binascii.unhexlify(
            "00000060ff534d4275000000001807c00000000000000000000000000000fffe0008400004ff006000080001003500005c005c003100390032002e003100360038002e003100370035002e003100320038005c00490050004300240000003f3f3f3f3f00")
        trans2_session_setup = binascii.unhexlify(
            "0000004eff534d4232000000001807c00000000000000000000000000008fffe000841000f0c0000000100000000000000a6d9a40000000c00420000004e0001000e000d0000000000000000000000000000")
        timeout = 30
        ip = url2ip(self.url)
        result = {}

        # Connect to socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(float(timeout) if timeout else None)
        host = ip
        port = 445
        s.connect((host, port))

        # Send/receive negotiate protocol request
        s.send(negotiate_protocol_request)
        s.recv(1024)

        # Send/receive session setup request
        s.send(session_setup_request)
        session_setup_response = s.recv(1024)

        # Extract user ID from session setup response
        user_id = session_setup_response[32:34]

        # Replace user ID in tree connect request packet
        modified_tree_connect_request = list(tree_connect_request)
        modified_tree_connect_request[32] = user_id[0]
        modified_tree_connect_request[33] = user_id[1]
        modified_tree_connect_request = "".join(modified_tree_connect_request)

        # Send tree connect request
        s.send(modified_tree_connect_request)
        tree_connect_response = s.recv(1024)

        # Extract tree ID from response
        tree_id = tree_connect_response[28:30]

        # Replace tree ID and user ID in trans2 session setup packet
        modified_trans2_session_setup = list(trans2_session_setup)
        modified_trans2_session_setup[28] = tree_id[0]
        modified_trans2_session_setup[29] = tree_id[1]
        modified_trans2_session_setup[32] = user_id[0]
        modified_trans2_session_setup[33] = user_id[1]
        modified_trans2_session_setup = "".join(modified_trans2_session_setup)

        # Send trans2 sessions setup request
        s.send(modified_trans2_session_setup)
        final_response = s.recv(1024)

        s.close()

        # Check for 0x51 response to indicate DOUBLEPULSAR infection
        if final_response[34] == "\x51":
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url

        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)

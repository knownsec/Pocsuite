#!/usr/bin/env python
# encoding: utf-8
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import socket
import struct
import threading
import time
import sys
import random
from optparse import OptionParser

# 注意：使用raw socket需要setcap给python进程发raw包的权限
# sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python2.7

ETH_P_IP = 0x0800  # Internet Protocol Packet


def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += ord(data[i]) + (ord(data[i + 1]) << 8)

    if n:
        s += ord(data[i + 2])

    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff

    return s


def recv(event, src, dst, srcp, dstp, buff, timeout):
    """
        event: should be set when a packet is sent
        src: source ip
        dst: destination ip
        srcp: source port
        dstp: destination port
        buff: buffer for received data
    """
    sock = socket.socket(socket.AF_PACKET,
                         socket.SOCK_DGRAM,
                         socket.htons(ETH_P_IP))
    sock.settimeout(timeout)
    event.wait()

    while True:
        try:
            data, sa_ll = sock.recvfrom(65535)
            if sa_ll[1] == ETH_P_IP and sa_ll[2] == socket.PACKET_HOST:
                break  # break if we captured incoming ip packet,
        except socket.timeout as e:
            print 'socket.timeout:', e
            sock.close()
            return
        except socket.error as e:
            print 'socket.error:', e
            sock.close()
            return
    sip = data[12:16]  # src ip
    dip = data[16:20]  # dst ip
    sp = data[20:22]  # src port
    dp = data[22:24]  # dst port

    if (sip == dst and dip == src and sp == dstp and dp == srcp):
        buff.append(data)  # return received packet
        event.clear()
    sock.close()


def send(ip, tcp, payload="", retry=1, timeout=1):
    if timeout <= 0:
        # Avoid entering an infinite waiting loop
        timeout = 0.1
    response = []
    event = threading.Event()
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_RAW,
                         socket.IPPROTO_RAW)
    # Extracting identifiers
    # ip
    src = ip.source
    dst = ip.destination
    # port
    srcp = struct.pack("!H", tcp.srcp)
    dstp = struct.pack("!H", tcp.dstp)

    tcp.payload = payload
    packet = ip.pack() + tcp.pack(ip.source, ip.destination) + payload

    for i in range(retry):
        t = threading.Thread(target=recv,
                             args=(event, src, dst, srcp,
                                   dstp, response, timeout)
                             )
        t.start()
        try:
            sock.sendto(packet, (socket.inet_ntoa(dst), 0))
        except Exception as e:
            print e
        event.set()
        t.join()
        if not event.isSet():
            break

    if event.isSet():
        return None
    else:
        return response[0]


class layer():
    pass


class ETHER(object):
    def __init__(self, src, dst, typ=ETH_P_IP):
        self.src = src
        self.dst = dst
        self.typ = typ

    def pack(self):
        ethernet = struct.pack(
            '!6s6sH',
            self.dst,
            self.src,
            self.typ
        )
        return ethernet


class IP(object):
    def __init__(self, source, destination, payload='', proto=socket.IPPROTO_TCP):
        self.version = 4
        self.ihl = 5  # Internet Header Length
        self.tos = 0  # Type of Service
        self.tl = 20 + len(payload)
        self.id = 0  # random.randint(0, 65535)
        self.flags = 0  # Don't fragment
        self.offset = 0
        self.ttl = 64
        self.protocol = proto
        self.checksum = 2  # will be filled by kernel
        self.source = socket.inet_aton(source)
        self.destination = socket.inet_aton(destination)

    def pack(self):
        ver_ihl = (self.version << 4) + self.ihl
        flags_offset = (self.flags << 13) + self.offset
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                ver_ihl,
                                self.tos,
                                self.tl,
                                self.id,
                                flags_offset,
                                self.ttl,
                                self.protocol,
                                self.checksum,
                                self.source,
                                self.destination)
        self.checksum = checksum(ip_header)
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                ver_ihl,
                                self.tos,
                                self.tl,
                                self.id,
                                flags_offset,
                                self.ttl,
                                self.protocol,
                                socket.htons(self.checksum),
                                self.source,
                                self.destination)
        return ip_header

    def unpack(self, packet):
        _ip = layer()
        _ip.ihl = (ord(packet[0]) & 0xf) * 4
        iph = struct.unpack("!BBHHHBBH4s4s", packet[:_ip.ihl])
        _ip.ver = iph[0] >> 4
        _ip.tos = iph[1]
        _ip.length = iph[2]
        _ip.ids = iph[3]
        _ip.flags = iph[4] >> 13
        _ip.offset = iph[4] & 0x1FFF
        _ip.ttl = iph[5]
        _ip.protocol = iph[6]
        _ip.checksum = hex(iph[7])
        _ip.src = socket.inet_ntoa(iph[8])
        _ip.dst = socket.inet_ntoa(iph[9])
        _ip.list = [
            _ip.ihl,
            _ip.ver,
            _ip.tos,
            _ip.length,
            _ip.ids,
            _ip.flags,
            _ip.offset,
            _ip.ttl,
            _ip.protocol,
            _ip.src,
            _ip.dst]
        return _ip


class TCP(object):
    def __init__(self, srcp, dstp, seqn=1):
        self.srcp = srcp
        self.dstp = dstp
        self.seqn = seqn
        self.ackn = 0
        self.offset = 5  # Data offset: 5x4 = 20 bytes
        self.reserved = 0
        self.urg = 0
        self.ack = 0
        self.psh = 0
        self.rst = 0
        self.syn = 1
        self.fin = 0
        self.window = socket.htons(5840)
        self.checksum = 0
        self.urgp = 0
        self.payload = ""

    def pack(self, source, destination):
        data_offset = (self.offset << 4) + 0
        flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5)
        tcp_header = struct.pack('!HHLLBBHHH',
                                 self.srcp,
                                 self.dstp,
                                 self.seqn,
                                 self.ackn,
                                 data_offset,
                                 flags,
                                 self.window,
                                 self.checksum,
                                 self.urgp)
        # pseudo header fields
        source_ip = source
        destination_ip = destination
        reserved = 0
        protocol = socket.IPPROTO_TCP
        total_length = len(tcp_header) + len(self.payload)
        # Pseudo header
        psh = struct.pack("!4s4sBBH",
                          source_ip,
                          destination_ip,
                          reserved,
                          protocol,
                          total_length)
        psh = psh + tcp_header + self.payload
        tcp_checksum = checksum(psh)
        tcp_header = struct.pack("!HHLLBBH",
                                 self.srcp,
                                 self.dstp,
                                 self.seqn,
                                 self.ackn,
                                 data_offset,
                                 flags,
                                 self.window)
        tcp_header += struct.pack('H', tcp_checksum) + struct.pack('!H', self.urgp)
        return tcp_header

    def unpack(self, packet):
        cflags = {  # Control flags
            32: "U",
            16: "A",
            8: "P",
            4: "R",
            2: "S",
            1: "F"
        }
        _tcp = layer()
        _tcp.thl = (ord(packet[12]) >> 4) * 4
        _tcp.options = packet[20:_tcp.thl]
        _tcp.payload = packet[_tcp.thl:]
        tcph = struct.unpack("!HHLLBBHHH", packet[:20])
        _tcp.srcp = tcph[0]  # source port
        _tcp.dstp = tcph[1]  # destination port
        _tcp.seq = tcph[2]  # sequence number
        _tcp.ack = hex(tcph[3])  # acknowledgment number
        _tcp.flags = ""
        for f in cflags:
            if tcph[5] & f:
                _tcp.flags += cflags[f]
        _tcp.window = tcph[6]  # window
        _tcp.checksum = hex(tcph[7])  # checksum
        _tcp.urg = tcph[8]  # urgent pointer
        _tcp.list = [
            _tcp.srcp,
            _tcp.dstp,
            _tcp.seq,
            _tcp.ack,
            _tcp.thl,
            _tcp.flags,
            _tcp.window,
            _tcp.checksum,
            _tcp.urg,
            _tcp.options,
            _tcp.payload]
        return _tcp


class UDP(object):
    def __init__(self, src, dst, payload=''):
        self.src = src
        self.dst = dst
        self.payload = payload
        self.checksum = 0
        self.length = 8  # UDP Header length

    def pack(self, src, dst, proto=socket.IPPROTO_UDP):
        length = self.length + len(self.payload)
        pseudo_header = struct.pack(
            '!4s4sBBH',
            socket.inet_aton(src), socket.inet_aton(dst), 0,
            proto, length
        )
        self.checksum = checksum(pseudo_header)
        packet = struct.pack('!HHHH', self.src, self.dst, length, 0)
        return packet


def main():
    parser = OptionParser()
    parser.add_option("-s", "--src", dest="src", type="string",
                      help="Source IP address", metavar="IP")
    parser.add_option("-d", "--dst", dest="dst", type="string",
                      help="Destination IP address", metavar="IP")
    options, args = parser.parse_args()
    if options.dst is None:
        parser.print_help()
        sys.exit()
    else:
        dst_host = socket.gethostbyname(options.dst)
    if options.src is None:
        # Get the current Network Interface
        src_host = socket.gethostbyname(socket.gethostname())
    else:
        src_host = options.src

    print("[+] Local Machine: %s" % src_host)
    print("[+] Remote Machine: %s" % dst_host)
    data = "TEST!!"
    print("[+] Data to inject: %s" % data)
    # IP Header
    ipobj = IP(src_host, dst_host)
    # TCP Header
    tcpobj = TCP(1234, 80)
    response = send(ipobj, tcpobj, iface="eth0", retry=1, timeout=0.3)
    if response:
        ip = ipobj.unpack(response)
        response = response[ip.ihl:]
        tcp = tcpobj.unpack(response)
        print "IP Header:", ip.list
        print "TCP Header:", tcp.list


if __name__ == "__main__":
    main()

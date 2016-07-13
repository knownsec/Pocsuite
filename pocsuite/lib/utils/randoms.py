#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""

import random


upperAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerAlpha = "abcdefghijklmnopqrstuvwxyz"
numerals = "0123456789"
allchars = [chr(_) for _ in xrange(0x00, 0xFF + 0x01)]


def rand_base(length, bad, chars):
    '''generate a random string with chars collection'''
    cset = (set(chars) - set(list(bad)))
    if len(cset) == 0:
        return ""
    chars = [list(cset)[random.randrange(len(cset))] for i in xrange(length)]
    chars = map(str, chars)
    return "".join(chars)


def rand_char(bad='', chars=allchars):
    '''generate a random char with chars collection'''
    return rand_base(1, bad, chars)


def rand_text(length, bad='', chars=allchars):
    '''generate a random string (cab be with unprintable chars)'''
    return rand_base(length, bad, chars)


def rand_text_alpha(length, bad=''):
    '''generate a random string with alpha chars'''
    chars = upperAlpha + lowerAlpha
    return rand_base(length, bad, set(chars))


def rand_text_alpha_lower(length, bad=''):
    '''generate a random lower string with alpha chars'''
    return rand_base(length, bad, set(lowerAlpha))


def rand_text_alpha_upper(length, bad=''):
    '''generate a random upper string with alpha chars'''
    return rand_base(length, bad, set(upperAlpha))


def rand_text_alphanumeric(length, bad=''):
    '''generate a random string with alpha and numerals chars'''
    chars = upperAlpha + lowerAlpha + numerals
    return rand_base(length, bad, set(chars))


def rand_text_numeric(length, bad=''):
    '''generate a random string with numerals chars'''
    return rand_base(length, bad, set(numerals))


def rand_item_from_iters(iter):
    '''choose a random item from iters'''
    return rand_base(1, '', iter)

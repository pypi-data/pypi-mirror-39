# -*- coding: utf-8 -*-
from __future__ import absolute_import

import hashlib
import time
import urllib


class THQS(object):
    '''
    代码来自官方文档 demo
    https://doc.bokecc.com/live/dev/liveapi/#toc_3 附录2: HTTP通信加密算法
    '''
    def __init__(self, api_key):
        self.api_key = api_key

    def urlencode(self, params):
        '对请求的字段进行urlencode，返回值是包含所有字段的list'
        l = []
        #遍历字典，进行quote_plus操作，并把所有字段拼成list
        for k, v in params.iteritems():
            qk = urllib.quote_plus(str(k))
            qv = urllib.quote_plus(str(v))
            url_param = '%s=%s' % (qk, qv)
            l.append(url_param)
        l.sort()
        return '&'.join(l)

    def encrypt(self, params):
        qs = self.urlencode(params)

        qftime = 'time=%d' % int(time.time())
        salt = 'salt=%s' % self.api_key
        qftail = '&%s&%s' % (qftime, salt)
        qf = qs + qftail
        hashqf = 'hash=%s' % (hashlib.new('md5', qf).hexdigest().upper())
        thqs = '&'.join((qs, qftime, hashqf))
        return thqs

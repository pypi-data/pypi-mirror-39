# -*- coding: utf-8 -*-
import logging
import requests

from . import exceptions
from .utils import THQS


class APIMixin(object):

    def __init__(self, userid, api_key):
        self.userid = userid
        self.api_key = api_key
        self.thqs = THQS(api_key)

    def get_url(self, path):
        api_prefix = self.get_api_prefix()
        return '{}{}'.format(api_prefix, path)

    def get_api_prefix(self):
        return NotImplementedError

    def request(self, url, params, method='get', timeout=3):
        if not isinstance(params, dict):
            raise exceptions.CCSDKInvalidParamException()
        # TODO: 目前看到的都是get接口
        if method != 'get':
            raise NotImplementedError()
        url = '{}?{}'.format(url, self.thqs.encrypt(params))
        response = requests.get(url, timeout=timeout)
        data = response.json()
        if data['result'] != 'OK':
            logging.error('[CCSDK request error]: %s', data)
            raise exceptions.CCServerException(str(data))
        return data

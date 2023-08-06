# -*- coding: utf-8 -*-

class CCSDKException(Exception):
    pass


class CCSDKInvalidParamException(CCSDKException):
    pass


class CCServerException(CCSDKException):
    pass

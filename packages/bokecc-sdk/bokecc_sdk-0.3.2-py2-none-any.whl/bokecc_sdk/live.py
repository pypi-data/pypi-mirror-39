# -*- coding: utf-8 -*-
'''
直播类接口
https://doc.bokecc.com/live/dev/liveapi/
版本: 2.3.1
日期: 2018-11-23
'''
from __future__ import absolute_import

import arrow

from . import constants
from . import exceptions
from .mixins import APIMixin


class LiveAPI(APIMixin):

    def get_api_prefix(self):
        return 'http://api.csslcloud.net/api/'

    def room_create(self, name, desc, templatetype, authtype,
            publisherpass, assistantpass, playpass=None, checkurl=None,
            barrage=0, foreignpublish=0, openlowdelaymode=0, showusercount=1,
            openhostmode=0, warmvideoid='', livestarttime='',
            playerbackgroundhint='', manuallyrecordmode=0,
            clientdocpermissions=0, repeatedloginsetting=0, maxaudiencenum=0,
            documentdisplaymode=1, openlivecountdown=0, showlectueronlinenum=1,
            showassistonlinenum=1):
        '''
        创建直播间
        通过该接口可以创建直播间，接口请求地址为：
        http://api.csslcloud.net/api/room/create
        userid  CC账户ID
        name    直播间名称
        desc    直播间描述
        templatetype    直播模板类型，请求模板信息接口可获得模板类型的详细信息。
        authtype    验证方式，0：接口验证，需要填写下面的checkurl；1：密码验证，需要填写下面的playpass；2：免密码验证
        publisherpass   推流端密码，即讲师密码
        assistantpass   助教端密码
        playpass    播放端密码  可选
        checkurl    验证地址    可选
        barrage 是否开启弹幕。0：不开启；1：开启    可选，默认为0
        foreignpublish  是否开启第三方推流。0：不开启；1：开启  可选，默认为0
        openlowdelaymode    开启直播低延时模式。0为关闭；1为开启    可选，默认为关闭
        showusercount   在页面显示当前在线人数。0表示不显示；1表示显示  可选，默认显示当前人数，模板一暂不支持此设置
        openhostmode    开启主持人模式，"0"表示不开启；"1"表示开启  可选，默认不开启，开通主持人模式权限后方可使用
        warmvideoid 插播暖场视频，填写同一账号下云点播视频vid   可选，默认关闭；参数值为空，表示关闭
        livestarttime   直播开始时间；格式：yyyy-MM-dd HH:mm:ss 可选，默认为空
        playerbackgroundhint    播放器提示语。未直播时播放器将显示该提示语  可选，最多15个字符
        manuallyrecordmode  手动录制模式。0：关闭；1：开启  可选，默认关闭
        clientdocpermissions    讲师文档权限。0：关闭；1：开启  可选，默认关闭；
        repeatedloginsetting    重复登录设置；0：允许后进入者登录;1:禁止后进入者登录，对讲师端和观看端生效  可选，默认0
        maxaudiencenum  直播间并发人数上限  可选，默认为0，表示不做限制
        documentdisplaymode 文档显示模式。1：适合窗口;2:适合宽度    可选，适合窗口
        openlivecountdown   倒计时功能。0：关闭；1：开启    可选，默认关闭
        showlectueronlinenum    讲师端显示在线人数。0：不显示；1：显示  可选，默认显示
        showassistonlinenum    助教主持人端显示在线人数。0：不显示；1：显示可选，默认显示
        '''
        url = self.get_url('room/create')
        authtype = constants.LiveAuthType(authtype).value
        templatetype = constants.LiveTemplateType(templatetype).value
        params = {
            'userid': self.userid, 'name': name, 'desc': desc, 'templatetype': templatetype,
            'authtype': authtype, 'publisherpass': publisherpass, 'assistantpass': assistantpass,
            'playpass': playpass, 'checkurl': checkurl, 'barrage': barrage,
            'foreignpublish': foreignpublish, 'openlowdelaymode': openlowdelaymode,
            'showusercount': showusercount, 'openhostmode': openhostmode,
            'warmvideoid': warmvideoid, 'livestarttime': livestarttime,
            'playerbackgroundhint': playerbackgroundhint, 'manuallyrecordmode': manuallyrecordmode,
            'clientdocpermissions': clientdocpermissions, 'repeatedloginsetting': repeatedloginsetting,
            'maxaudiencenum': maxaudiencenum, 'documentdisplaymode': documentdisplaymode,
            'openlivecountdown': openlivecountdown, 'showlectueronlinenum': showlectueronlinenum,
            'showassistonlinenum': showassistonlinenum
        }
        response = self.request(url, params, method='get')
        return response

    def room_update(self, roomid, name, desc, templatetype, authtype,
            publisherpass, assistantpass, playpass=None, checkurl=None,
            barrage=0, openlowdelaymode=0, showusercount=1,
            warmvideoid='', livestarttime='', playerbackgroundhint='', manuallyrecordmode=0,
            clientdocpermissions=0, repeatedloginsetting=0, maxaudiencenum=0,
            documentdisplaymode=1, openlivecountdown=0, showlectueronlinenum=1,
            showassistonlinenum=1):
        '''
        编辑直播间
        通过该接口可以编辑直播间的信息，接口请求地址为：
        http://api.csslcloud.net/api/room/update
        roomid  直播间id
        userid  CC账户ID
        name    直播间名称
        desc    直播间描述
        templatetype    直播模板类型，请求模板信息接口可获得模板类型的详细信息。
        authtype    验证方式，0：接口验证，需要填写下面的checkurl；1：密码验证，需要填写下面的playpass；2：免密码验证
        publisherpass   推流端密码，即讲师密码
        assistantpass   助教端密码
        playpass    播放端密码  可选
        checkurl    验证地址    可选
        barrage 是否开启弹幕。0：不开启；1：开启
        openlowdelaymode    开启直播低延时模式。0为关闭；1为开启    可选
        showusercount   在页面显示当前在线人数，0表示不显示；1表示显示  可选，默认显示当前人数，模板一暂不支持此设置
        warmvideoid 插播暖场视频，填写同一账号下云点播视频vid   可选，默认关闭；参数值为空，表示关闭
        livestarttime   直播开始时间；格式；yyyy-MM-dd HH:mm:ss 可选
        playerbackgroundhint    播放器提示语。未直播时播放器将显示该提示语  可选，最多15个字符
        manuallyrecordmode  手动录制模式。0：关闭；1：开启  可选，默认关闭
        clientdocpermissions    讲师文档权限。0：关闭；1：开启  可选，默认开启
        repeatedloginsetting    重复登录设置；0：允许后进入者登录;1:禁止后进入者登录，对讲师端和观看端生效  可选，默认0
        maxaudiencenum  直播间并发人数上限  可选，默认为0，表示不做限制
        documentdisplaymode 文档显示模式。1：适合窗口;2:适合宽度    可选，适合窗口
        openlivecountdown   开启倒计时功能。0：不开启；1：开启  可选，默认不开启
        showlectueronlinenum    讲师端显示在线人数。0：不显示；1：显示  可选，默认显示
        showassistonlinenum 助教主持人端显示在线人数。0：不显示；1：显示    可选，默认显示
        '''
        url = self.get_url('room/update')
        authtype = constants.LiveAuthType(authtype).value
        templatetype = constants.LiveTemplateType(templatetype).value
        params = {
            'roomid': roomid, 'userid': self.userid, 'name': name, 'desc': desc, 'templatetype': templatetype,
            'authtype': authtype, 'publisherpass': publisherpass, 'assistantpass': assistantpass,
            'playpass': playpass, 'checkurl': checkurl, 'barrage': barrage,
            'openlowdelaymode': openlowdelaymode, 'showusercount': showusercount,
            'warmvideoid': warmvideoid, 'livestarttime': livestarttime,
            'playerbackgroundhint': playerbackgroundhint, 'manuallyrecordmode': manuallyrecordmode,
            'clientdocpermissions': clientdocpermissions, 'repeatedloginsetting': repeatedloginsetting,
            'maxaudiencenum': maxaudiencenum, 'documentdisplaymode': documentdisplaymode,
            'openlivecountdown': openlivecountdown, 'showlectueronlinenum': showlectueronlinenum,
            'showassistonlinenum': showassistonlinenum
        }
        response = self.request(url, params, method='get')
        return response

    def room_close(self, roomid):
        '''
        关闭直播间
        过该接口将直播间关闭，接口请求地址为：
        http://api.csslcloud.net/api/room/close
        roomid    直播间id
        userid    CC账户ID
        '''
        url = self.get_url('room/close')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_info(self, pagenum=50, pageindex=1):
        '''
        获取直播间列表
        通过该接口可以获取用户的直播间列表信息
        http://api.csslcloud.net/api/room/info
        userid  CC账户ID
        pagenum 每页显示的个数  可选，系统默认值为50
        pageindex   页码    可选，系统默认值为1
        '''
        url = self.get_url('room/info')
        params = {'userid': self.userid, 'pagenum': pagenum, 'pageindex': pageindex}
        response = self.request(url, params, method='get')
        return response

    def room_search(self, roomid):
        '''
        获取直播间信息
        通过该接口可以获取直播间的信息，接口请求地址为:
        http://api.csslcloud.net/api/room/search
        roomid    直播间id
        userid    CC账户ID
        '''
        url = self.get_url('room/search')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_code(self, roomid):
        '''
        获取直播间代码
        通过该接口可以获取直播间的代码信息，包括观看地址信息、客户端登陆地址、
        助教端登录地址、推流地址(只有第三方推流直播间才可以获得)。接口请求地址为:
        http://api.csslcloud.net/api/room/code
        roomid    直播间id
        userid    CC账户ID
        '''
        url = self.get_url('room/code')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def live_info(self, roomid, pagenum=50, pageindex=1, starttime='', endtime=''):
        '''
        获取直播列表, 某直播间的直播列表，如果有合并视频也会在列表中
        通过该接口获取指定直播间下历史直播信息，接口请求地址为:
        http://api.csslcloud.net/api/v2/live/info
        roomid    直播间id
        userid    CC账户ID
        pagenum 每页显示的个数  可选，系统默认值为50
        pageindex   页码    可选，系统默认值为1
        starttime   查询起始时间,如需按时间范围查询可添加该参数和下面的endtime参数，该查询是按直播的开始时间作为查询条件的。    可选，如果填写该参数则endtime参数必填；格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-01 12:30:00"
        endtime 查询截止时间    可选 ，如果填写该参数则starttime必填；格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-02 12:30:00"
        '''
        url = self.get_url('v2/live/info')
        params = {
            'userid': self.userid, 'roomid': roomid, 'pagenum': pagenum, 'pageindex': pageindex
        }
        if starttime or endtime:
            if not starttime and endtime:
                raise exceptions.CCSDKInvalidParamException()
            starttime = arrow.get(starttime).format('YYYY-MM-DD HH:mm:ss')
            endtime = arrow.get(endtime).format('YYYY-MM-DD HH:mm:ss')
            params['starttime'] = starttime
            params['endtime'] = endtime
        response = self.request(url, params, method='get')
        return response

    def record_info(self, roomid, pagenum=50, pageindex=1, starttime='', endtime='', liveid=''):
        '''
        查询回放列表, 如果有合并视频也会在列表中
        通过该接口可以分页获取回放列表的信息，接口请求地址为：
        http://api.csslcloud.net/api/v2/record/info
        roomid    直播间id
        userid    CC账户ID
        pagenum 每页显示的个数  可选，系统默认值为50
        pageindex   页码    可选，系统默认值为1
        starttime   查询起始时间,如需按时间范围查询可添加该参数和下面的endtime参数，该查询是按直播的开始时间作为查询条件的。    可选，如果填写该参数则endtime参数必填；格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-01 12:30:00"
        endtime 查询截止时间    可选 ，如果填写该参数则starttime必填；格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-02 12:30:00"
        liveid 直播id可选，将只查询该直播下的回放信息
        '''
        url = self.get_url('v2/record/info')
        params = {
            'userid': self.userid, 'roomid': roomid, 'pagenum': pagenum, 'pageindex': pageindex
        }
        if starttime or endtime:
            if not starttime and endtime:
                raise exceptions.CCSDKInvalidParamException()
            starttime = arrow.get(starttime).format('YYYY-MM-DD HH:mm:ss')
            endtime = arrow.get(endtime).format('YYYY-MM-DD HH:mm:ss')
            params['starttime'] = starttime
            params['endtime'] = endtime
        if liveid:
            params['liveid'] = liveid
        response = self.request(url, params, method='get')
        return response

    def record_search(self, recordid):
        '''
        查询回放信息
        通过该接口获取单个回放信息，接口请求地址为:
        http://api.csslcloud.net/api/v2/record/search
        roomid    直播间id
        recordid    recordid
        '''
        url = self.get_url('v2/record/search')
        params = {'userid': self.userid, 'recordid': recordid}
        response = self.request(url, params, method='get')
        return response

    def live_merge(self, roomid, recordids):
        '''
        合并回放接口, 合并需要时间，需要接回调
        通过该接口可以对同一直播间下相同模板类型的回放进行合并，接口请求地址为：
        http://api.csslcloud.net/api/live/merge
        userid  CC账户ID    必须
        roomid  直播间id    必须
        recordids   回放ID集合  必须，中间以英文逗号间隔，最多支持3个回放合并
        '''
        url = self.get_url('live/merge')
        if len(recordids.split(',')) > 3:
            raise exceptions.CCSDKInvalidParamException()
        params = {'userid': self.userid, 'roomid': roomid, 'recordids': recordids}
        response = self.request(url, params, method='get')
        return response

    def rooms_broadcasting(self, roomid):
        '''
        获取正在直播的直播间列表
        该接口可获取用户账号下所有正在进行直播的直播间列表，接口请求地址为:
        http://api.csslcloud.net/api/rooms/broadcasting
        userid    CC账户ID
        '''
        url = self.get_url('rooms/broadcasting')
        params = {'userid': self.userid}
        response = self.request(url, params, method='get')
        return response

    def rooms_publishing(self, roomids):
        '''
        获取直播间直播状态
        通过该接口获取直播间的直播状态，接口请求地址为:
        http://api.csslcloud.net/api/rooms/publishing
        roomids 直播间id（以英文逗号,区分)，批量查询直播间数量不能超过100个
        userid  CC账户ID
        '''
        url = self.get_url('rooms/publishing')
        if len(roomids.split(',')) > 100:
            raise exceptions.CCSDKInvalidParamException()
        params = {'userid': self.userid, 'roomids': roomids}
        response = self.request(url, params, method='get')
        return response

    def statis_connections(self, roomid, starttime, endtime):
        '''
        获取直播间连接数
        通过该接口可以获取直播间的连接数统计信息，接口请求地址为:
        http://api.csslcloud.net/api/statis/connections
        roomid  直播间id
        userid  CC账户ID
        starttime   开始时间，精确到秒，例："2015-01-02 12:30:00"
        endtime 结束时间，精确到秒，例："2015-01-02 13:30:00"
        '''
        url = self.get_url('statis/connections')
        starttime = arrow.get(starttime).format('YYYY-MM-DD HH:mm:ss')
        endtime = arrow.get(endtime).format('YYYY-MM-DD HH:mm:ss')
        params = {
            'userid': self.userid, 'roomid': roomid,
            'starttime': starttime, 'endtime': endtime
        }
        response = self.request(url, params, method='get')
        return response

    def statis_useraction(self, roomid, starttime, endtime):
        '''
        获取直播间连接数
        通过该接口可以获取直播间的连接数统计信息，接口请求地址为:
        http://api.csslcloud.net/api/statis/useraction
        roomid  直播间id
        userid  CC账户ID
        starttime   查询起始时间，格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-01 12:30:00"
        endtime 查询截止时间，格式：yyyy-MM-dd HH:mm:ss ，endtime和starttime相差不能超过7天
        '''
        url = self.get_url('statis/useraction')
        start = arrow.get(starttime)
        end = arrow.get(endtime)
        if (end - start).days > 7:
            raise exceptions.CCSDKInvalidParamException()
        starttime = start.format('YYYY-MM-DD HH:mm:ss')
        endtime = end.format('YYYY-MM-DD HH:mm:ss')
        params = {
            'userid': self.userid, 'roomid': roomid,
            'starttime': starttime, 'endtime': endtime
        }
        response = self.request(url, params, method='get')
        return response

    def statis_userview(self, liveid):
        '''
        获取观看直播的统计信息, 注意，如果live是合并类型的，cc会返回一个报错
        通过该接口可获取观看直播的统计信息，接口请求地址为:
        http://api.csslcloud.net/api/statis/userview
        liveid  直播id
        userid  CC账户ID
        '''
        url = self.get_url('statis/userview')
        params = {'userid': self.userid, 'liveid': liveid}
        response = self.request(url, params, method='get')
        return response

    def statis_replay_useraction(self, recordid, pagenum=50, pageindex=1):
        '''
        获取单个直播回放的观看统计信息
        通过该接口可以获取单个直播观看回放的用户登录，退出行为统计。接口请求地址为:
        http://api.csslcloud.net/api/v2/statis/replay/useraction
        recordid    录制id
        userid  CC账户ID
        pageindex   可选，查询页码，默认为1
        pagenum 可选，单页所查询的数据条数，默认为50，最大阈值为1000
        '''
        url = self.get_url('v2/statis/replay/useraction')
        if pagenum > 1000:
            raise exceptions.CCSDKInvalidParamException()
        params = {'userid': self.userid, 'recordid': recordid, 'pagenum': pagenum, 'pageindex': pageindex}
        response = self.request(url, params, method='get')
        return response

    def statis_replay(self, starttime, endtime, pagenum=50, pageindex=1):
        '''
        获取所有直播回放的观看统计信息
        通过该接口可以获取观看直播回放的用户登录，退出行为统计。接口请求地址为：
        http://api.csslcloud.net/api/v2/statis/replay
        userid  CC账户ID    必须
        starttime   查询起始时间    必须，格式：yyyy-MM-dd HH:mm:ss ，例："2015-01-01 12:30:00"
        endtime 查询截止时间    必须，格式：yyyy-MM-dd HH:mm:ss ，endtime和starttime相差不能超过7天
        pageindex   查询页码    可选，默认为1
        pagenum 单页所查询的数据条数    可选，默认为50，最大阈值为1000
        '''
        url = self.get_url('v2/statis/replay')
        if pagenum > 1000:
            raise exceptions.CCSDKInvalidParamException()
        start = arrow.get(starttime)
        end = arrow.get(endtime)
        if (end - start).days > 7:
            raise exceptions.CCSDKInvalidParamException()
        starttime = start.format('YYYY-MM-DD HH:mm:ss')
        endtime = end.format('YYYY-MM-DD HH:mm:ss')
        params = {
            'userid': self.userid, 'starttime': starttime, 'endtime': endtime,
            'pagenum': pagenum, 'pageindex': pageindex
        }
        response = self.request(url, params, method='get')
        return response

    def viewtemplate_info(self):
        '''
        获取直播间模板信息
        http://api.csslcloud.net/api/viewtemplate/info
        userid   CC账户ID
        '''
        url = self.get_url('viewtemplate/info')
        params = {'userid': self.userid}
        response = self.request(url, params, method='get')
        return response

    def get_auto_login_url(self, url, name, token, login_type):
        '''
        url 为 room_code 中拿到的各个url,
        观众直播、回放，助教，主持人都为viewername, viewertoken
        讲师为publishname, publishpassword

        观看直播登录示例
        https://view.csslcloud.net/api/view/index?roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        观看回放登录示例
        http://view.csslcloud.net/api/view/callback?recordid=xxx&roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        助教端自动登陆
        https://view.csslcloud.net/api/view/assistant?roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        主持人自动登陆
        https://view.csslcloud.net/api/view/manage?roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        讲师端自动登陆
        https://view.csslcloud.net/api/view/lecturer?roomid=xxx&userid=xxx&publishname=xxx&publishpassword=xxx
        '''
        login_type = constants.LiveAutoLoginType(login_type)
        if login_type != constants.LiveAutoLoginType.lecturer:
            return '{}&autoLogin=true&viewername={}&viewertoken={}'.format(url, name, token)
        return '{}&publishname={}&publishpassword={}'.format(url, name, token)

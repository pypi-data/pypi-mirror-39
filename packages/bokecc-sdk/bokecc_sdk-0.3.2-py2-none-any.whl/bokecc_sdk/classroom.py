# -*- coding: utf-8 -*-
'''
云课堂API相关
https://doc.bokecc.com/class/developer/classapi/
日期: 2018-09-07
'''
from __future__ import absolute_import

import arrow

from . import constants
from . import exceptions
from .mixins import APIMixin


class ClassRoomAPI(APIMixin):

    def get_api_prefix(self):
        return 'https://ccapi.csslcloud.net/api/'

    def room_create(self, name, room_type, templatetype, publisherpass, assist_pass,
            audience_authtype=1, audience_pass=None, talker_authtype=1,
            talker_pass=None, inspector_authtype=1, inspector_pass=None,
            white_list=None, desc='', mergetype=2,
            max_users=None, max_streams=None, video_mode=1, talker_bitrate=200,
            publisher_bitrate=200, classtype=1, presenter_out=0,
            light_mark=0, show_exit=1, ppt_support=0, ppt_display=0,
            screen_lock=0, desktop_audio=0, manual_record=0,
            record_bitrate=500, warm_open='0', helper_switch=0,
            record_switch=0, assist_switch=0):
        '''
        创建直播间, templatetype使用8时会500
        https://ccapi.csslcloud.net/api/room/create
        userid  字符串  用户账号ID  必须
        name    字符串  直播间名称 长度限制 <= 100  必须
        room_type   整型    房间类型 1:视频群聊 2:小班课    必须
        publisherpass   字符串  老师端密码 长度限制 <= 64   必须
        assist_pass 字符串  助教端密码 长度限制 <= 64   可选，默认为用户账号ID
        audience_authtype   整型    旁听认证方式 0:接口验证 1:密码 2:免密码 3:白名单    可选, 默认为1
        audience_pass   字符串  旁听密码 长度限制 <= 256    可选, 默认为用户ID，认证方式为接口认证时，此处填写接口认证地址
        talker_authtype 整型    互动学员认证方式 0:接口验证 1: 密码 2:免密码 3:白名单   可选 默认为为1
        talker_pass 字符串  互动学员认证密码 长度限制 <= 256    可选, 默认为用户账号ID，认证方式为接口认证时，此处填写接口认证地址
        inspector_authtype  整型    隐身者认证方式 0:接口验证 1: 密码 2:免密码  可选 默认为为1
        inspector_pass  字符串  隐身者认证密码 长度限制 <= 256  可选, 默认为用户账号ID, 认证方式为接口认证时，此处填写接口认证地址
        white_list  字符串  如果互动者开启了白名单，则此处填写json化的用户名/密码，如 "{"user": "123"}" 可选
        desc    字符串  直播间简介 长度限制 <= 10000    可选
        templatetype    整型    模版类型 1:讲课模式 2:主视角模式 4:平铺模式 8:1v1模式 16:双师模式   可选，默认为8
        mergetype   整型    合流模式 1:主视角模式 2:平铺模式 3:覆盖模式 可选, 默认为2
        max_users   整型    最大支持人数(进入房间人数), 不能超过账户允许上限    可选, 默认为账户允许上限
        max_streams 整型    互动人数上限(实际连麦人数), 不能超过账户允许上限    可选, 默认为房间max_users上限
        video_mode  整型    连麦音视频模式 1:音视频 2.仅音频    可选, 默认为1
        talker_bitrate  整型    学生端码率 不超2000 可选, 默认为200
        publisher_bitrate   整型    老师端码率 不超2000 可选, 默认为200
        classtype   整型    连麦模式 1:点名 2:自由 3:自动   可选, 默认为1
        presenter_out   布尔型  非直播状态下踢出老师    可选，默认为false
        light_mark  整型    跑马灯 0: 关闭 1: 开启  可选, 默认为0
        show_exit   整型    页面是否 显示退出按钮, 0 隐藏 1 可选 默认为1
        ppt_support 布尔型  是否支持ppt 可选
        ppt_display 布尔型  ppt显示样式 0: 适应窗口 1: 适应宽度，默认为0    可选
        screen_lock 整型    桌面锁屏 0:未开通 1:开通 2:开启 3:关闭，默认为0 可选
        desktop_audio   整型    桌面分享声音 0: 关闭 1: 开启, 默认为0   可选
        manual_record   整型    手动录制 0: 关闭 1: 开启, 默认为0   可选
        record_bitrate  整型    回放清晰度 速度优先:500 画质优先:0，默认速度优先    可选
        warm_open   字符串  暖场视频 '0': 关闭, '1': 开启，默认关闭 可选
        helper_switch   整型    直播助手开关 0: 关闭 1:开启，默认关闭   可选
        record_switch   整型    录屏助手开关 0: 关闭 1:开启，默认关闭   可选
        assist_switch   整型    助教开关 0: 关闭 1:开启，默认关闭   可选
        '''
        url = self.get_url('room/create')
        templatetype = constants.ClassRoomTemplateType(templatetype).value
        if max_users and not max_streams:
            max_streams = max_users
        params = {
            'userid': self.userid, 'name': name, 'room_type': room_type, 'publisherpass': publisherpass,
            'assist_pass': assist_pass, 'audience_authtype': audience_authtype,
            'audience_pass': audience_pass, 'talker_authtype': talker_authtype,
            'inspector_authtype': inspector_authtype, 'inspector_pass': inspector_pass,
            'desc': desc, 'templatetype': templatetype,
            'mergetype': mergetype, 'video_mode': video_mode, 'talker_bitrate': talker_bitrate,
            'publisher_bitrate': publisher_bitrate, 'classtype': classtype, 'presenter_out': presenter_out,
            'light_mark': light_mark, 'show_exit': show_exit, 'ppt_support': ppt_support,
            'ppt_display': ppt_display, 'screen_lock': screen_lock, 'desktop_audio': desktop_audio,
            'manual_record': manual_record, 'record_bitrate': record_bitrate, 'warm_open': warm_open,
            'helper_switch': helper_switch, 'record_switch': record_switch, 'assist_switch': assist_switch
        }
        if white_list:
            params['white_list'] = white_list
        if talker_pass:
            params['talker_pass'] = talker_pass
        if max_users:
            params['max_users'] = max_users
        if max_streams:
            params['max_streams'] = max_streams
        response = self.request(url, params, method='get')
        return response

    def room_update(self, live_roomid, templatetype, name, publisherpass, assist_pass,
            audience_authtype=1, audience_pass=None, talker_authtype=1,
            talker_pass=None, inspector_authtype=1, inspector_pass=None,
            white_list=None, desc='', mergetype=2,
            max_users=None, max_streams=None, video_mode=1, talker_bitrate=200,
            publisher_bitrate=200, classtype=1, presenter_out=0,
            light_mark=0, show_exit=1, ppt_support=0, ppt_display=0,
            screen_lock=0, desktop_audio=0, manual_record=0,
            record_bitrate=500, warm_open='0', helper_switch=0,
            record_switch=0, assist_switch=0):
        '''
        更新直播间, templatetype使用8时会500
        https://ccapi.csslcloud.net/api/room/update
        userid  字符串  用户账号ID  必须
        live_roomid 字符串  房间ID  必须
        name    字符串  直播间名称  可选
        publisherpass   字符串  老师端密码 长度限制 <= 64   可选
        audience_authtype   整型    旁听认证方式 0:接口验证 1:密码 2:免密码 3:白名单    可选
        audience_pass   字符串  旁听密码 长度限制 <= 256    可选
        talker_authtype 整型    互动学员认证方式 0:接口验证 1: 密码 2:免密码 3:白名单   可选
        talker_pass 字符串  互动学员认证密码, 长度限制 <= 256   可选
        inspector_authtype  整型    隐身者认证方式 0:接口验证 1: 密码 2:免密码  可选
        inspector_pass  字符串  隐身者认证密码 长度限制 <= 256  可选
        white_list  字符串  如果互动者开启了白名单，则此处填写json化的用户名/密码，如 "{"user": "123"}" 可选
        desc    字符串  直播间简介 长度限制 <= 10000    可选
        templatetype    整型    模版类型 1:讲课模式 2:主视角模式 4:平铺模式 8:1v1模式 16:双师模式   可选
        mergetype   整型    合流模式 1:主视角模式 2:平铺模式 3:覆盖模式 可选
        max_users   整型    最大支持人数, 不能超过开通人数上限  可选
        max_streams 整型    互动人数上限, 不能超过开通人数上限  可选
        video_mode  整型    连麦音视频模式 1:音视频 2.仅音频    可选
        publisher_bitrate   整型    老师端码率 不超2000 可选
        talker_bitrate  整型    学生端码率 不超2000 可选
        audio_bitrate   整型    音频码率 默认为50   可选
        classtype   整型    连麦模式 1:点名 2:自由 3:自动   可选
        is_follow   字符串  是否跟随 主视角模式下 否: 空字符，是: streamid  可选
        allow_chat  布尔型  是否允许发言 房间级配置 可选
        allow_audio 布尔型  是否允许使用麦克风 房间级配置   可选
        allow_speak 布尔型  是否允许上麦 房间级配置 可选
        presenter_out   布尔型  非直播状态下踢出老师    可选
        ppt_support 布尔型  是否支持ppt 可选
        light_mark  整型    跑马灯 0: 关闭 1: 开启  可选
        show_exit   整型    整型 页面是否 显示退出按钮, 0: 隐藏 1:显示  可选
        desktop_audio   整型    桌面分享声音 0: 关闭 1: 开启, 默认为0   可选
        manual_record   整型    手动录制 0: 关闭 1: 开启, 默认为0   可选
        record_bitrate  整型    回放清晰度 速度优先:500 画质优先:0，默认速度优先    可选
        warm_open   字符串  暖场视频 '0': 关闭, '1': 开启，默认关闭 可选
        '''
        url = self.get_url('room/update')
        templatetype = constants.ClassRoomTemplateType(templatetype).value
        if max_users and not max_streams:
            max_streams = max_users
        params = {
            'userid': self.userid, 'name': name, 'live_roomid': live_roomid, 'publisherpass': publisherpass,
            'audience_authtype': audience_authtype,
            'audience_pass': audience_pass, 'talker_authtype': talker_authtype,
            'inspector_authtype': inspector_authtype, 'inspector_pass': inspector_pass,
            'desc': desc, 'templatetype': templatetype,
            'mergetype': mergetype, 'video_mode': video_mode, 'talker_bitrate': talker_bitrate,
            'publisher_bitrate': publisher_bitrate, 'classtype': classtype, 'presenter_out': presenter_out,
            'light_mark': light_mark, 'show_exit': show_exit, 'ppt_support': ppt_support, 'desktop_audio': desktop_audio,
            'manual_record': manual_record, 'record_bitrate': record_bitrate, 'warm_open': warm_open,
        }
        if white_list:
            params['white_list'] = white_list
        if talker_pass:
            params['talker_pass'] = talker_pass
        if max_users:
            params['max_users'] = max_users
        if max_streams:
            params['max_streams'] = max_streams
        response = self.request(url, params, method='get')
        return response

    def room_live_start(self, roomid):
        '''
        开始直播
        https://ccapi.csslcloud.net/api/room/live/start
        userid  字符串  用户ID  可选
        roomid  字符串  直播间ID    必须
        '''
        url = self.get_url('room/live/start')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_live_stop(self, roomid):
        '''
        结束直播
        https://ccapi.csslcloud.net/api/room/live/stop
        userid  字符串  用户ID  可选
        roomid  字符串  直播间ID    必须
        '''
        url = self.get_url('room/live/stop')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_close(self, roomid):
        '''
        关闭直播间
        过该接口将直播间关闭，接口请求地址为：
        https://ccapi.csslcloud.net/api/room/close
        roomid    直播间id
        userid    CC账户ID
        '''
        url = self.get_url('room/close')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_list(self, name=None, status=None, page=1, lines=50, roomid=None):
        '''
        获取账号下房间列表
        获取账号下房间列表 可以指定name status roomid为过滤参数
        https://ccapi.csslcloud.net/api/room/list
        userid  字符串  用户账号ID  必须
        name    字符串  房间名称    可选
        status  整型    房间房间状态 10:正常 20:关闭    可选
        page    整型    获取指定页  可选 默认为1
        lines   整型    分页每页数据量  可选 默认为50
        roomid  字符串  房间ID  可选
        '''
        url = self.get_url('room/list')
        params = {'userid': self.userid, 'page': page, 'lines': lines}
        if name:
            params['name'] = name
        if status:
            params['status'] = status
        if roomid:
            params['roomid'] = roomid
        response = self.request(url, params, method='get')
        return response

    def room_room_detail(self, roomid):
        '''
        获取房间信息
        https://ccapi.csslcloud.net/api/room/room_detail
        userid  字符串  用户账号ID  必须
        roomid  字符串  房间ID  必须
        '''
        url = self.get_url('room/room_detail')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response


    def room_link(self, roomid):
        '''
        获取房间登录链接
        https://ccapi.csslcloud.net/api/v1/room/link
        userid  字符串  用户账号ID  必须
        roomid  字符串  房间ID  必须
        '''
        url = self.get_url('v1/room/link')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_set_single(self, roomid, status):
        '''
        切换合流布局模式
        https://ccapi.csslcloud.net/api/room/set_single
        userid  字符串  用户账号ID  必须
        roomid  字符串  房间ID  必须
        status  整型    状态 1:主视角 2:平铺    必须
        '''
        url = self.get_url('room/set_single')
        params = {'userid': self.userid, 'roomid': roomid, 'status': status}
        response = self.request(url, params, method='get')
        return response

    def room_user_list(self, roomid):
        '''
        获取当前房间人员列表
        https://ccapi.csslcloud.net/api/v1/room/user/list
        userid  字符串  用户账号ID  必须
        roomid  字符串  房间ID  必须
        '''
        url = self.get_url('v1/room/user/list')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def room_live_stat(self, roomid):
        '''
        查询直播状态
        https://ccapi.csslcloud.net/api/v1/room/live/stat
        roomid  字符串  房间ID  必须
        '''
        url = self.get_url('v1/room/live/stat')
        params = {'userid': self.userid, 'roomid': roomid}
        response = self.request(url, params, method='get')
        return response

    def get_auto_login_url(self, url, name, token, login_type):
        '''
        url 为 room_link 中拿到的各个url,
        教师端:
            https://class.csslcloud.net/index/presenter/?roomid=FC3548C1133061D09C33DC5901307461&userid=E9607DAFB705A798&username=XXX&password=XXX&autoLogin=true
        互动者:
            https://class.csslcloud.net/index/talker/?roomid=FC3548C1133061D09C33DC5901307461&userid=E9607DAFB705A798&username=XXX&password=XXX&autoLogin=true
        旁听端:
            http://view.csslcloud.net/api/view/index?roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        回放端:
            http://view.csslcloud.net/api/view/callback/login?liveid=xxx&roomid=xxx&userid=xxx&autoLogin=true&viewername=11&viewertoken=11
        注意: 请详细比对上述URL示例
        '''
        login_type = constants.ClassRoomAutoLoginType(login_type)
        if login_type in (
                constants.ClassRoomAutoLoginType.record,
                constants.ClassRoomAutoLoginType.audience,
            ):
            return '{}&autoLogin=true&viewername={}&viewertoken={}'.format(url, name, token)
        return '{}&autoLogin=true&username={}&password={}'.format(url, name, token)

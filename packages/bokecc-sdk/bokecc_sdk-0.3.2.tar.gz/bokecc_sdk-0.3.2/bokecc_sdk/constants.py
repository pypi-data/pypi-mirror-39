# -*- coding: utf-8 -*-
from __future__ import absolute_import

from enum import IntEnum


class LiveAuthType(IntEnum):
    api = 0
    password = 1
    no_password = 2


class LiveTemplateType(IntEnum):
    video = 1 # 视频
    video_chat_qa = 2 # 视频，聊天，问答
    video_chat = 3 # 视频，聊天 3
    video_doc_chat = 4 # 视频，文档，聊天 4
    video_doc_chat_qa = 5 # 视频，文档，聊天，问答 5
    video_qa = 6 # 视频，问答 6


class LiveAutoLoginType(IntEnum):
    user = 1
    assistant = 2
    manage = 3
    lecturer = 4


class ClassRoomAutoLoginType(IntEnum):
    presenter = 1  # 教师
    assistant = 2  # 助教
    talker = 3  # 互动
    audience = 4  # 旁听
    inspector = 5  # 隐身
    record = 6  # 回放


class ClassRoomRoomType(IntEnum):
    chat = 1
    small_class = 2


class ClassRoomTemplateType(IntEnum):
    talk = 1 # 讲课模式
    main = 2 # 主视角模式
    tile = 4 # 平铺模式
    # one_to_one = 8 # 1v1模式, 使用这个会500
    two_teacher = 16 # 双师模式


class ClassRoomMergeType(IntEnum):
    main = 1 # 讲课模式
    tile = 2 # 主视角模式
    cover = 3 # 平铺模式


class ClassRoomClassType(IntEnum):
    call = 1 # 点名
    free = 2 # 自由
    auto = 3 # 自动

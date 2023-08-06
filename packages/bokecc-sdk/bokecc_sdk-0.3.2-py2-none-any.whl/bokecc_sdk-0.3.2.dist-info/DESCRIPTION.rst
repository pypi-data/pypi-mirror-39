bokecc_sdk
===
SDK for bokecc.

live.py
---
cc 云直播类接口
https://doc.bokecc.com/live/dev/liveapi/

classroom.py
---
cc 云课堂类接口
https://doc.bokecc.com/class/developer/classapi/

todo
---
TODO: live 聊天、抽奖、签到等非视频信息
TODO: 完成点播类接口
TODO: 完成云课堂聊天等接口

usage
---

    pip install bokecc_sdk

    live_api = LiveAPI(APIKEY)
    userid = USERID
    name = 'sdk测试创建直播间name密码'
    desc = 'sdk测试创建直播间desc'
    templatetype = constants.LiveTemplateType.video_doc_chat_qa.value
    authtype = constants.LiveAuthType.password.value
    publisherpass = 'tcctest'
    assistantpass = 'acctest'
    response = live_api.room_create(
        userid, name, desc, templatetype, authtype, publisherpass, assistantpass
    )


examples 目录创建 __secret.py, 填入cc的apikey

其他具体接口见 examples/live.py

回调类demo见 https://github.com/duoduo369/original/blob/master/original/misc/views.py 中的
CCAuthAPI、CallBackCCLiveStartAPI、CallBackCCLiveEndAPI、CallBackCCRecordAPI、CallBackCCOfflineWatchAPI



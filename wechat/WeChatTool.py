# author: HuYong
# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic

WECHAT_TOKEN = 'token'
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'
BaseUrl = "http://wechat.tunnel.qydev.com/wechat"
redirect_uri = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxce660ee67e094937&redirect_uri=URL&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
redirect_uri_state = redirect_uri.replace("URL",BaseUrl + "/state")
redirect_uri_control = redirect_uri.replace("URL",BaseUrl + "/control")
redirect_uri_bind = redirect_uri.replace("URL",BaseUrl + "/bind")
redirect_uri_history = redirect_uri.replace("URL",BaseUrl + "/history")
redirect_uri_nearby = redirect_uri.replace("URL",BaseUrl + "/nearby")
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

# 创建自定义菜单
wechat_instance.create_menu({
    'button':[
        {
            'type': 'view',
            'name': '附近',
            'url': redirect_uri_nearby
        },
        {
            'name': '充电',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '实时状态',
                    'url': redirect_uri_state
                },
                {
                    'type': 'view',
                    'name': '实时控制',
                    'url': redirect_uri_control
                }
            ]
        },
        {
            'name': '我的',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '绑定',
                    'url': redirect_uri_bind
                },
                {
                    'type': 'view',
                    'name': '消费记录',
                    'url': redirect_uri_history
                }
            ]
        },
    ]
})


#创建带参数的二维码
# url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKEN"
# token = wechat_instance.get_access_token().get("access_token")
# url = url.replace("TOKEN",token)
# data = "{\"expire_seconds\": 1800,\"action_name\":\"QR_LIMIT_SCENE\",\"action_info\":{\"scene\":{\"scene_id\":12}}}"
# r = requests.post(url,data)
# s = json.loads(r.text)
# ticket = s["ticket"]
# url_getImage = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=TICKET"
# url_getImage = url_getImage.replace("TICKET",ticket)
# response = requests.get(url_getImage)
# print response.read()

#
# data ={
#     "expire_seconds": 604800,
#     "action_name": "QR_SCENE",
#     "action_info": {
#         "scene": {
#             "scene_id": 123
#         }
#     }
# }
#
# d = wechat_instance.create_qrcode(data)
# response = wechat_instance.show_qrcode(d.get("ticket"))
# with open('qrcode.jpg', 'wb') as fd:
#     for chunk in response.iter_content(1024):
#         fd.write(chunk)
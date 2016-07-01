# author: HuYong
# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic
import requests
import json
import time


WECHAT_TOKEN = 'token'
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

# 创建自定义菜单
# wechat_instance.create_menu({
#     'button':[
#         {
#             'type': 'view',
#             'name': '绑定',
#             'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxce660ee67e094937&redirect_uri=http://jnsems.applinzi.com/wechat/bangding&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
#         },
#         {
#             'type': 'click',
#             'name': '消费记录',
#             'key': 'MYDATA'
#         }
#     ]
# })

#微信推送
def WeChatFinishPush(user,charge):
    name = user.username
    data = {"name": {"value": name, "color": "#173177"}, "time" : {"value":str(charge.start_time),"color" : "#173177"}}
    json = wechat_instance.send_template_message(str(user.openid),"JAk6ryroKka3T-Y-NNWeiK1ufKUGwnhSbs7CdRHFbD0", data)
    print json

def WeChatAccountPush(user,account):
    name = user.username
    data = {"name": {"value": name}, "start_time" : {"value":str(account.charge.start_time)},"end_time":{"value":str(account.charge.end_time)},"over":{"value":str(account.charge.overtime)},"over_time":{"value":str(account.charge.overtime)},"money":{"value":account.money}}
    json = wechat_instance.send_template_message(str(user.openid),"qh3B8cPGIr2joDg5izkF66qWdsDR-k6cYexwD_EXR28", data)
    print json

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


data ={
    "expire_seconds": 604800,
    "action_name": "QR_SCENE",
    "action_info": {
        "scene": {
            "scene_id": 123
        }
    }
}

d = wechat_instance.create_qrcode(data)
response = wechat_instance.show_qrcode(d.get("ticket"))
with open('qrcode.jpg', 'wb') as fd:
    for chunk in response.iter_content(1024):
        fd.write(chunk)
# author: HuYong
# coding=utf-8
from wechat_sdk import WechatBasic

# 微信推送

WECHAT_TOKEN = 'token'
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


# 充电完成推送
def WeChatPush_alreadyFinish(user, charge):
    print "**************"
    responsedata = "你好，" + user.username.encode("utf-8") + "\n你的车已经充电完毕，请尽快取车"
    data = {"data": {"value": responsedata, "color": "#173177"}}
    print data
    try:
        json = wechat_instance.send_template_message(str(user.openid), "saRJ7C92DuovutwG57V7wcvxeVoZwp04VvUWSZHOnas", data)
    except Exception,e:
        print e
    print json


# 充电完毕本次充电信息推送
def WeChatPush_payFinish(user, account):
    name = user.username
    money = account.money
    start_time = account.charge.start_time
    end_time = account.charge.end_time
    responsedata = "你好," + name.encode("utf-8") + ":\n本次充电信息：\n开始时间:" + str(start_time) + "\n结束时间:" + str(end_time)[:-7] + "\n取车超时：" + "\n充电金额:" + str(money) + "元"
    data = {"message": {"value": responsedata, "color": "#173177"}}
    json = wechat_instance.send_template_message(str(user.openid), "qG8RIocMDo7bHwhrR1bFqJ6IpULniA1qNcvcT2xzmmU", data)
    print json


# 充电异常推送
def WeChatPush_Exception(user, charge):
    responsedata = "你好，" + str(user.username) + "\n当前充电出现异常！\n异常信息：" + str(charge.message)
    data = {"data": {"value": responsedata, "color": "#173177"}}
    json = wechat_instance.send_template_message(str(user.openid), "_hX6OW53QBj44qN95totWDv6uPVzLu5ejb2Y5wpS7vU", data)
    print json


# 超时取车
def WeChatPush_delay(user):
    responsedata = "你好，" + str(user.username) + "\n由于长时间未取车占用充电车位，车或已被管理员处理。\n请自行联系管理员！"
    data = {"data": {"value": responsedata, "color": "#173177"}}
    json = wechat_instance.send_template_message(str(user.openid), "OZfofkQxfQ-RjUDvl-sfdiz2-1nn81J4CQb19QgDs-Y", data)
    print json

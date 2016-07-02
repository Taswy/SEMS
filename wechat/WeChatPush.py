# author: HuYong
# coding=utf-8


#充电完成推送
from wechat.wechat_index import wechat_instance


def WeChatPush_alreadyFinish(user,charge):
    name = user.username
    data = {"name": {"value": name, "color": "#173177"}, "time": {"value": str(charge.start_time), "color": "#173177"}}
    json = wechat_instance.send_template_message(str(user.openid), "JAk6ryroKka3T-Y-NNWeiK1ufKUGwnhSbs7CdRHFbD0", data)
    print json

#充电完毕本次充电信息推送

def WeChatPush_payFinish(user,account):
    name = user.username
    data = {"name": {"value": name}, "start_time": {"value": str(account.charge.start_time)},
            "end_time": {"value": str(account.charge.end_time)}, "over": {"value": str(account.charge.overtime)},
            "over_time": {"value": str(account.charge.overtime)}, "money": {"value": account.money}}
    json = wechat_instance.send_template_message(str(user.openid), "qh3B8cPGIr2joDg5izkF66qWdsDR-k6cYexwD_EXR28", data)
    print json


#充电异常推送

def WeChatPush_Exception(user,charge):
    pass
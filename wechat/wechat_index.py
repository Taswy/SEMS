# author: HuYong
# coding=utf-8
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import TextMessage, EventMessage
from models.models import User,Charge,Account


WECHAT_TOKEN = 'token'
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # POST
    # 解析本次请求的 XML 数据
    wechat_instance.parse_data(data=request.body)
    message = wechat_instance.get_message()
    if isinstance(message,TextMessage):
        response = wechat_instance.response_text("发送的内容是：\t"+message.content.encode("utf-8"))
        return HttpResponse(response, content_type="application/xml")
    elif isinstance(message, EventMessage):
        if message.type == "click":
            if message.key == "MYDATA":
                openid = message.source
                count = User.objects.filter(openid=openid).count()
                if count > 0:
                    user = User.objects.get(openid=openid)
                    chargeList = Charge.objects.filter(user=user)
                    result = ""
                    for charge in chargeList:
                        account = Account.objects.get(charge=charge)
                        print account
                        print account.charge.start_time
                        print account.charge.end_time
                        result = result + "充电时间：\n"+str(account.charge.start_time)+"---"+str(account.charge.end_time)+"\n充电费用："+str(account.money)+"\n*************\n"
                    print result
                    reply = result
                else:
                    reply = "请先绑定！"
                response = wechat_instance.response_text(reply)
                return HttpResponse(response, content_type="application/xml")







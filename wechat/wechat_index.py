# author: HuYong
# coding=utf-8
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import TextMessage, EventMessage
from models.models import User

WECHAT_TOKEN = 'token'
AppID = 'wx0f12120163cbea26'
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
    if isinstance(message, TextMessage):
        response = wechat_instance.response_text("智能电动车管理系统！")
        return HttpResponse(response, content_type="application/xml")
    elif isinstance(message, EventMessage):
        print message.type
        if message.type == "location":  # 接收用户的位置信息，并实时更新
            longitude = message.longitude
            latitude = message.latitude
            openid = message.source
            try:
                user = User.objects.get(openid=openid)
                user.longitude = float(longitude)
                user.latitude = float(latitude)
                user.save()
                print user.longitude
            except:
                pass
        elif message.type == "subscribe":  # 首次推送
            response = wechat_instance.response_text("这是智能电动车管理系统！\n详情请查看首页！")
            return HttpResponse(response, content_type="application/xml")

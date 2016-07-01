#coding=utf-8
import json
import django
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import time
from models.models import User, Charge, Ammeter, Account, AmmeterGroup
from wechat.wechatTest import WeChatFinishPush, WeChatAccountPush

'''
URL ：/checkStudent
POST数据示例:{"card_number":"5sdf87e4"}
返回数据示例 ：
1) {"student_number":1030412535, "username":"胡勇", "result": 1} 学生存在且已经注册，返回学号
2）{"student_number":1030412535, "username":None, "result": 0 , "message":"你的账号未注册"} 学生存在但并未注册
3）{"student_number":1030412535, "username":"胡勇", "result": 0 ,"message":"你的账号被封啦"} result为2时账号异常，提示message。
4）{"student_number":None, "result":0,"message":"序列号没有对应的学号"} 序列号没有对应的学号
5) {"result":-1,message:"Exception"} 异常错误返回-1
'''
def checkStudent(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            card_number = r["card_number"]
            user = User.objects.filter(card_number=card_number)[0]
            response_data = {}
            #用户不存在
            if not user or not user.student_number:
                response_data['result'] = 0
                response_data['message'] = u"序列号没有对应的学号"
                response_data["student_number"] = None
            else:
                if not user.username: #账号没有在微信注册
                    response_data["result"] = 0
                    response_data["student_number"] = user.student_number
                    response_data["message"] = u"你的账号未注册"
                elif user.usage=="0": #账号被封
                    response_data["result"] = 0
                    response_data["student_number"] = user.student_number
                    response_data["username"] = user.username
                    response_data["message"] = u"你的账号被封啦"
                else: #正常
                    response_data["result"] = 1
                    response_data["student_number"] = user.student_number
                    response_data["username"] = user.username
            return HttpResponse(json.dumps(response_data)
                                , content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

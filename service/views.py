#coding=utf-8
import json
import django
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import time
from models.models import User, Charge, Ammeter, Account, AmmeterGroup

def calculate_money(start_time,end_time,electricity=0.5):
    seconds = (end_time - start_time).seconds
    money = seconds / 3600 * electricity
    return "%.2f" % money

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
            user = User.objects.filter(card_number=card_number)
            response_data = {}
            if user:
                user = user[0]
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
            elif not user or not user[0].student_number:
                #用户不存在
                response_data['result'] = 0
                response_data['message'] = u"序列号没有对应的学号"
                response_data["student_number"] = None
            return HttpResponse(json.dumps(response_data)
                                , content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

'''
URL ：/start
POST数据示例:

{
  "card_number":"5sdf87e4",
  "ammeterGroup_number": '0001',
  "ammeter_number":'0001'
}
返回数据示例 ：

{
    "result":1
}

{"result":-1,message:"Exception"} 异常错误返回-1
'''
def start(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            card_number = r["card_number"]
            ammeter_number = r["ammeter_number"]
            ammeterGroup_number = r["ammeterGroup_number"]
            user = User.objects.filter(card_number=card_number)[0]
            ammeterGroup = AmmeterGroup.objects.filter(ammeterGroup_number=ammeterGroup_number)[0]
            ammeter = Ammeter.objects.filter(ammeter_number=ammeter_number,group=ammeterGroup)[0]
            response_data = {}
            #创建一条新的记录，Ammeter.status设置为on（'0'）
            if ammeter and user:
                ammeter.status = '0'
                ammeter.save()
                #charge = Charge(user=user,ammeter=ammeter) _state 没有定义
                charge =Charge()
                charge.user = user
                charge.ammeter = ammeter
                charge.save()

                return HttpResponse(json.dumps({"result":1}), content_type="application/json")
            return HttpResponse(json.dumps({"result":0}) , content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")


'''
URL ：/end

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "card_number":"5sdf87e4",
      "ammeterGroup_number": '0001',
      "ammeter_number":'0001'
    }
返回数据示例 ：

    {
        "result":1
    }
    '''
def end(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            ammeter_number = r["ammeter_number"]
            ammeterGroup_number = r["ammeterGroup_number"]
            ammeterGroup = AmmeterGroup.objects.filter(ammeterGroup_number=ammeterGroup_number)[0]
            ammeter = Ammeter.objects.filter(ammeter_number=ammeter_number,group=ammeterGroup)[0]
            charge = Charge.objects.filter(ammeter=ammeter).order_by('-id')[0]
            response_data = {}
            #获取对应最新的记录，Ammeter.status设置为off（'1'）,
            if charge:
                ammeter.status = '1'
                ammeter.save()
                charge.status = '1'
                charge.end_time = timezone.now()
                charge.save()
                return HttpResponse(json.dumps({"result":1}), content_type="application/json")
            return HttpResponse(json.dumps({"result":0}) , content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")


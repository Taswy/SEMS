#coding=utf-8
import json
import django
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.views.decorators.csrf import csrf_exempt
import time
from models.models import User, Charge, Ammeter, Account, AmmeterGroup, Node
from wechat.WeChatPush import WeChatPush_payFinish


def calculate_money(start_time,end_time,electricity=0.5):
    seconds = (end_time - start_time).total_seconds()
    money = float(seconds) / 3600 * electricity
    return float("%.2f" % money)

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
            #获取对应最新的记录，Ammeter.status设置为'4', u'闲置',
            if charge:
                ammeter.status = '4'
                ammeter.save()
                charge.status = '1'
                charge.end_time = timezone.now()
                charge.save()
                account = Account()
                account.charge = charge
                account.money = calculate_money(charge.start_time,charge.end_time)
                account.save()
                WeChatPush_payFinish(user=charge.user,account=account)
                return HttpResponse(json.dumps({"result":1}), content_type="application/json")
            return HttpResponse(json.dumps({"result":0}) , content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

'''
URL ：/charge

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

{
  "current_value":1.05,
  "voltage_value":2.01,
  "ammeterGroup_number": '0001',
  "ammeter_number":'0001'
}
返回数据示例 ：

{
    "result":1
}
'''
def charge(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            current_value = r["current_value"]
            voltage_value = r["voltage_value"]
            ammeter_number = r["ammeter_number"]
            ammeterGroup_number = r["ammeterGroup_number"]
            ammeterGroup = AmmeterGroup.objects.filter(ammeterGroup_number=ammeterGroup_number)[0]
            ammeter = Ammeter.objects.filter(ammeter_number=ammeter_number,group=ammeterGroup)[0]
            charge = Charge.objects.filter(ammeter=ammeter).order_by('-id')[0]
            if charge:
                new_node = Node()
                new_node.current_value = current_value
                new_node.voltage_value = voltage_value
                new_node.save()
            return HttpResponse(json.dumps({"result":1}), content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

'''URL ：/AmmeterControl

HTTP请求方式 ：POST

POST数据示例:

{"ammeterGroup_number": "0001"}
返回数据格式 ：JSON

返回数据示例 ：

{
    "21652" : "1",
    "54855" : "0",
    ...
    "14524" : "2"
}
说明: 返回一个数组status 键：电表号，值类型：str 值：1代表电表合闸，0代表电表开闸,2代表释放电表，3代表锁定电表
'''
def AmmeterControl(request):
     if request.method == "POST":
        try:
            r = json.loads(request.body)
            ammeterGroup_number = r["ammeterGroup_number"]
            ammeterGroup = AmmeterGroup.objects.filter(ammeterGroup_number=ammeterGroup_number)[0]
            response_data = {}
            if ammeterGroup:
                ammeter_s = Ammeter.objects.filter(group=ammeterGroup)
                for ammeter in ammeter_s:
                    #STATUS_CHOICE = (('0', u'开启'), ('1', u'关闭'), ('2', u'低压'), ('3', u'异常'),('4', u'闲置'))
                    if ammeter.status == '0' or ammeter.status == '2':
                        response_data[ammeter.ammeter_number] = "1"
                    elif ammeter.status == '1':
                        response_data[ammeter.ammeter_number] = "0"
                    elif ammeter.status == '3':
                        response_data[ammeter.ammeter_number] = "3" #异常即为锁定转台
                    else: #闲置状态
                        response_data[ammeter.ammeter_number] = "2"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

'''
URL ：/money

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

{
  "ammeterGroup_number": "0001",
  "ammeter_number":"0001"
}
说明：

字段：id_client ; 类型：int； 必须：是； 备注：客户端id

字段：Ammeter_id ; 类型：int ; 必须：是 ; 备注：充电处编号

返回数据格式 ：JSON

返回数据示例 ：

{
  "money":1.12
}
说明:

money ； 类型：float；当前金额
'''
def money(request):
    if request.method == "POST":
        try:
            r = json.loads(request.body)
            ammeter_number = r["ammeter_number"]
            ammeterGroup_number = r["ammeterGroup_number"]
            ammeterGroup = AmmeterGroup.objects.filter(ammeterGroup_number=ammeterGroup_number)[0]
            ammeter = Ammeter.objects.filter(ammeter_number=ammeter_number,group=ammeterGroup)[0]
            charge = Charge.objects.filter(ammeter=ammeter).order_by('-id')[0]
            response_data = {}
            if charge:
                end_time =  timezone.now()
                if charge.end_time:
                    end_time =  charge.end_time
                response_data["money"] = calculate_money(charge.start_time, end_time)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception,e:
            return HttpResponse(json.dumps({"result":-1,"message":e.message}), content_type="application/json")

##
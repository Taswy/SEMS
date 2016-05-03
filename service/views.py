# author: HuYong
# -*- coding: utf-8 -*-
import json
import django
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import time
from models.models import User, Charge, Ammeter, Account, AmmeterGroup
from wechat.wechatTest import WeChatFinishPush, WeChatAccountPush

'''
检查学生信息是否存在(API)
URL ：http://wechat123.ngrok.cc/service/checkStudent
HTTP请求方式 ：POST
请求数据格式 ：JSON
POST数据示例:{"student_number":1030614418}
说明：字段：student_number ; 类型：int ; 必须：是 ; 备注：学生学号
返回数据格式 ：JSON
返回数据示例 ：
1) {"result":1} 学生存在
2）{"result":0} 学生不存在
说明: 字段：result ; 类型：int
'''


@csrf_exempt
def checkStudent(request):
    if request.method == "POST":
        r = json.loads(request.body)
        student_number = r["student_number"]
        count = User.objects.filter(student_number=student_number).count()
        response_data = {}
        if count > 0:
            response_data['result'] = 1
        else:
            response_data['result'] = 0
        return HttpResponse(json.dumps(response_data), content_type="application/json")


'''
URL ：http://wechat123.ngrok.cc/service/charge
HTTP请求方式 ：POST
请求数据格式 ：JSON
POST数据示例:{"student_number":1030614418,"Ammeter_id":1,"message"：1}
说明：
字段：student_number ; 类型：int ; 必须：是 ; 备注：学生学号
字段：Ammeter_id ; 类型：int ; 必须：是 ; 备注：充电处编号
字段：message ; 类型：int ; 必须：是；备注 : 1：开始充电 2：结束充电 3：取车
返回数据格式 ：JSON
返回数据示例 ：
1）开始充电的情况：
{"result":1} 数据库更新成功
{"result":0} 数据库更新失败
说明: 字段：result ; 类型：int
2）结束充电情况：
{"result":1} 数据库更新成功
{"result":0} 数据库更新失败
说明:
字段：result ; 类型：int 备注：数据库更新结果
3）取车： {"result":1，"money":10.4} 数据库更新成功,充电金额：10.4元
{"result":0} 数据库更新失败
字段：result ; 类型：int 备注：数据库更新结果
字段：money ; 类型：double 备注：消费金额.
'''


@csrf_exempt
def charge(request):
    if request.method == "POST":
        r = json.loads(request.body)
        message = r["message"]
        student_number = r["student_number"]
        Ammeter_id = r["Ammeter_id"]
        user = User.objects.get(student_number=student_number)
        ammeter = Ammeter.objects.get(id=Ammeter_id)
        if message == 1:
            try:
                newChage = Charge(user=user, ammeter=ammeter)
                newChage.status = '0'
                ammeter.status = '0'
                ammeter.save()
                newChage.save()
                response_data = {'result': 1}
            except:
                response_data = {'result': 0}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif message == 2:
            charge = Charge.objects.get(user=user, ammeter=ammeter, status='0')
            charge.end_time = django.utils.timezone.now()
            charge.save()
            ammeter.status = '1'
            ammeter.save()
            WeChatFinishPush(user, charge)
            response_data = {'result': 1}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif message == 3:
            charge = Charge.objects.get(user=user, ammeter=ammeter, status='0')
            charge.overtime = int(time.mktime(django.utils.timezone.now().timetuple())) - int(
                time.mktime(charge.end_time.timetuple()))
            charge.status = '1'
            charge.save()
            newAccout = Account(charge=charge)
            newAccout.money = 2 + charge.overtime / 3600 * 0.1
            newAccout.save()
            WeChatAccountPush(user, newAccout)
            response_data = {'result': 1, "money": newAccout.money}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


'''
2.3 反向控制
URL ：http://wechat123.ngrok.cc/service/AmmeterControl
HTTP请求方式 ：POST
POST数据示例:
{"Ammeter_id":1}
返回数据格式 ：JSON
返回数据示例 ：
1) {"control":1} 充电站打开
2) {"control":0} 充电站关闭
说明:
字段：Ammeter_id ; 类型：int ; 备注：充电站编号
字段：control ; 类型：int ; 备注：指令
'''


@csrf_exempt
def AmmeterControl(request):
    if request.method == "POST":
        r = json.loads(request.body)
        Ammeter_id = r['Ammeter_id']
        ammeter = Ammeter.objects.get(id=Ammeter_id)
        result = 0
        try:
            charge = Charge.objects.filter(ammeter=ammeter).order_by('-id')[0]
            result = str(charge.status)
        except:
            pass
        response_data = {'result': result}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

@csrf_exempt
def test(request):
    group = AmmeterGroup.objects.get(id=1)
    print "group:"+str(group)
    ammeterlist = group.ammeter_set.all()
    for ammeter in ammeterlist:
        print "电表--->id: "+str(ammeter.id) + "  status："+str(ammeter.status)
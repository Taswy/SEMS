# author: HuYong
# coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from models.models import User, Charge, Node, Account, AmmeterGroup
import requests
import json

from wechat.WeChatUtil import GetAddress, calcDistance

AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'



'''**************************工具方法**************************************************'''

# 由request请求中的code换取openid
def getOpenid(request):
    code = request.REQUEST.get("code")
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code"
    url = url.replace("APPID", AppID).replace("SECRET", AppSecret).replace("CODE", code)
    rjson = requests.get(url)
    r = json.loads(rjson.text)
    openid = r["openid"]
    return openid


# 由openid换取user对象
def getUser(request=None,openid=None):
    if not openid:
        openid = getOpenid(request)
    try:
        user = User.objects.get(openid=openid)
    except:
        user = None
    return user




'''**************************************************************************************************'''


'''*********************************我的**************************************************************'''


# 用户绑定情况判断
def bind(request):
    try:
        openid = getOpenid(request)
    except:
        openid = request.GET.get("openid")
    context = {"openid": openid}
    count = User.objects.filter(openid=openid).count()
    if count > 0:
        user = User.objects.get(openid=openid)
        return render(request, "wechat/success.html")
    else:
        return render(request, "wechat/register.html", context)



#用户绑定
def doregist(request):
    if request.method == 'POST':  # 当提交表单时
        username = request.POST.get("username", "")
        student_number = request.POST.get("student_number", "")
        password = request.POST.get("password", "")
        count = User.objects.filter(student_number=student_number).count()
        print count
        if count > 0:
            openid = request.GET.get("openid")
            user = User.objects.get(student_number=student_number)
            user.username = username
            user.password = password
            user.openid = openid
            user.save()
            return render(request, "wechat/success.html")
        else:
            return  render(request,"wechat/error.html",{"content":"您未在校登记电动车！"})
    else:
        html = '''
            <head>
            <meta http-equiv="refresh" content="1;url=/wechat/regist">
            </head>
            格式错误！'''
        return HttpResponse(html)



# 查询消费记录
def history(request):
    user = getUser(request)
    charges = Charge.objects.filter(user=user).order_by("-start_time")
    result= []
    for charge in charges:
        try:
            account = Account.objects.get(charge=charge)
            account.charge.start_time
            result.append(account)
        except:
            pass
    return render(request, "wechat/consumption.html", {"accounts":result,"user":user})



'''**************************************************************************************************'''




'''****************************************充电**************************************************************'''


# 返回充电站的信息列表
def nearby(request):
    openid = getOpenid(request)
    user = getUser(openid=openid)
    if user == None:
        return HttpResponseRedirect("bind?openid=" + openid)
    groups = AmmeterGroup.objects.all()
    address = GetAddress(user.longitude, user.latitude).encode("utf-8")
    distanceList = []
    for group in groups:
        distance = calcDistance(user.latitude, user.longitude, group.latitude, group.longitude)
        distanceList.append(distance)
    distanceListSort = distanceList[:]
    distanceListSort.sort()
    resultGroupName = []
    resultValidNum = []
    resultDistance = []
    for distance in distanceListSort:
        group = groups[distanceList.index(distance)]
        resultGroupName.append(group.ammeterGroup_name.encode("utf-8"))
        resultValidNum.append(group.valid_number)
        resultDistance.append(distance)
    return render(request, "wechat/nearby.html", {"resultGroupName":resultGroupName,"Num":resultValidNum,"dis":resultDistance,"address":address})


# 返回实时状态
def state(request):
    if request.method == "GET":
        try:
            user = getUser(request)
        except:
            openid = request.GET.get("openid")
            user = User.objects.get(openid=openid)
        try:
            charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
            account = Account.objects.get(charge=charge)
        except:
            return render(request, "wechat/error.html",{"content":"尚未进行充电！"})
        if  charge.InitEnergy < 1:
            return render(request, "wechat/battery.html",{"openid":user.openid})
        else:
            node = Node.objects.filter(charge=charge).order_by("-id")[0]
            prosess = (float(node.energy_value) / 5 * 100+ float(charge.InitEnergy))
            if prosess >= 75:
                result = "/static/img/battery_4.png"
            elif prosess >= 50:
                result = "/static/img/battery_3.png"
            elif prosess >= 25:
                result = "/static/img/battery_2.png"
            else:
                result = "/static/img/battery_1.png"
            return render(request, "wechat/battery_RealTime.html", {"src": result})
    else:
        openid = request.GET.get("openid")
        InitEnergy = request.POST.get("battery")
        user = User.objects.get(openid=openid)
        charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
        charge.InitEnergy = InitEnergy
        charge.save()
        return  HttpResponseRedirect("state?openid="+openid)


# 反向控制
def control(request):
    try:
        user = getUser(request)
    except:
        openid = request.GET.get("openid")
        user = User.objects.get(openid=openid)
    try:
        charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
        account = Account.objects.get(charge=charge)
    except:
        return render(request, "wechat/error.html",{"content":"尚未进行充电！"})
    ammeter = charge.ammeter
    action = request.GET.get("action","")
    if action == "":
        status = ammeter.status
        if status == '0':
            return render(request, "wechat/r_control_1.html", {"openid": user.openid})
        else:
            return render(request, "wechat/r_control_2.html", {"openid": user.openid})
    else:
        if action == "start":
            ammeter.status = '0'
        else:
            ammeter.status = '1'
        ammeter.save()
        return HttpResponseRedirect("control?openid=" + user.openid)


'''**************************************************************************************************'''
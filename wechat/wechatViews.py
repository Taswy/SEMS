# author: HuYong
# coding=utf-8
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
def getUser(request):
    openid = getOpenid(request)
    user = User.objects.get(openid=openid)
    return user


'''**************************************************************************************************'''


'''*********************************我的**************************************************************'''


# 用户绑定情况判断
def bind(request):
    openid = getOpenid(request)
    context = {"openid": openid}
    count = User.objects.filter(openid=openid).count()
    if count > 0:
        user = User.objects.get(openid=openid)
        return render(request, "wechat/welcome.html", {"flag": "2", "user": user})
    else:
        return render(request, "wechat/regist.html", context)



#用户绑定
def doregist(request):
    if request.method == 'POST':  # 当提交表单时
        username = request.POST.get("username", "")
        student_number = request.POST.get("student_number", "")
        password = request.POST.get("password", "")
        count = User.objects.filter(student_number=student_number).count()
        if count > 0:
            openid = request.POST.get("openid")
            new = User(username=username, password=password, student_number=student_number, openid=openid)
            new.save()
            return render(request, "wechat/welcome.html", {"openid": openid, "user": new})
        else:
            html = '''
                <head>
                <meta http-equiv="refresh" content="1;url=/wechat/regist">
                </head>
                <h1>请到管理员处登记！</h1>'''
            return HttpResponse(html)
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
    content = ""
    for charge in charges:
        try:
            account = Account.objects.get(charge=charge)
            content = content + "充电时间：\n" + str(account.charge.start_time) + "---" + str(
                account.charge.end_time) + "\n充电费用：" + str(account.money) + "\n******************\n"
        except:
            pass
    return HttpResponse(content)



'''**************************************************************************************************'''




'''****************************************充电**************************************************************'''


# 返回充电站的信息列表
def nearby(request):
    user = getUser(request)
    groups = AmmeterGroup.objects.all()
    address = GetAddress(user.longitude, user.latitude).encode("utf-8")
    content = ""
    content = content + "你现在位于：" + address + "\n\n"
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
    return HttpResponse(content)


# 返回实时状态
def state(request):
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
    node = Node.objects.filter(time__gt=charge.start_time).order_by("-time")[0]
    prosess = (node.energy_value / 5 + charge.InitEnergy)*100
    if prosess > 75:
        result = 4
    elif prosess > 50:
        result = 3
    elif prosess > 25:
        result = 2
    else:
        result = 1
    return HttpResponse(node[0].voltage_value)


# 反向控制
def control(request):
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
    ammeter = charge.ammeter
    if request.method == 'GET':
        status = ammeter.status
        if status == '0':
            pass
        else:
            pass
    else:
        action = request.REQUEST.get("action")
        if action == "start":
            ammeter.status = '0'
        else:
            ammeter.status = '1'


'''**************************************************************************************************'''
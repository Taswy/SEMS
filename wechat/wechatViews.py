# author: HuYong
# coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
from models.models import User, Charge, Node, Account, AmmeterGroup
import requests
import json

from wechat.WeChatUtil import GetAddress, calcDistance

AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'


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


# 用户绑定
def bind(request):
    openid = getOpenid(request)
    context = {"openid": openid}
    count = User.objects.filter(openid=openid).count()
    if count > 0:
        user = User.objects.get(openid=openid)
        return render(request, "wechat/welcome.html", {"flag": "2", "user": user})
    else:
        return render(request, "wechat/regist.html", context)


# 返回实时状态
def state(request):
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
    nodes = Node.objects.filter(time__gt=charge.start_time).order_by("-time")
    return HttpResponse(nodes[0].voltage_value)


# 反向控制
def control(request):
    action = request.REQUEST.get("action")
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]


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
    for distance in distanceListSort:
        group = groups[distanceList.index(distance)]
        content = content + group.ammeterGroup_name.encode("utf-8") + "\t还有" + str(
            group.valid_number) + "个空位" + "\t距离您" + str(distance) + "m\n"
    print content
    return HttpResponse(content)


def regist(request):
    openid = request.GET.get("openid")
    print openid
    return render(request, "wechat/regist.html", {"openid": openid})


def doregist(request):
    if request.method == 'POST':  # 当提交表单时
        username = request.POST.get("username", "")
        student_number = request.POST.get("student_number", "")
        password = request.POST.get("password", "")
        count = User.objects.filter(student_number=student_number).count()
        if count > 0:
            openid = request.POST.get("openid")
            if openid == "":
                new = User(username=username, password=password, student_number=student_number)
                new.save()
                # 邮件发送！
                # from_student_number = settings.DEFAULT_FROM_student_number
                # context = "恭喜你注册成功！"+"您的账号是："+username+"；您的密码是："+password
                # send_mail('Welcome', context, from_student_number, [student_number], fail_silently=False)
                return redirect("/wechat")
            else:
                print openid
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

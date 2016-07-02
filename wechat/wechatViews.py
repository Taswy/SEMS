# author: HuYong
#-*- coding: utf-8 -*-
from math import *

from django.shortcuts import render, redirect, HttpResponse
from models.models import User, Charge, Node, Account, AmmeterGroup
import requests
import json
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'

#由request请求中的code换取openid
def getOpenid(request):
    code = request.REQUEST.get("code")
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code"
    url = url.replace("APPID",AppID).replace("SECRET",AppSecret).replace("CODE",code)
    rjson = requests.get(url)
    r = json.loads(rjson.text)
    openid = r["openid"]
    return openid


#由openid换取user对象
def getUser(request):
    openid = getOpenid(request)
    user = User.objects.get(openid=openid)
    return user


def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
     ra = 6378.140  # 赤道半径 (km)
     rb = 6356.755  # 极半径 (km)
     flatten = (ra - rb) / ra  # 地球扁率
     rad_lat_A = radians(Lat_A)
     rad_lng_A = radians(Lng_A)
     rad_lat_B = radians(Lat_B)
     rad_lng_B = radians(Lng_B)
     pA = atan(rb / ra * tan(rad_lat_A))
     pB = atan(rb / ra * tan(rad_lat_B))
     xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
     c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
     c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
     dr = flatten / 8 * (c1 - c2)
     distance = ra * (xx + dr)
     return distance

#用户绑定
def bind(request):
    openid = getOpenid(request)
    context = {"openid":openid}
    count  = User.objects.filter(openid=openid).count()
    if count>0:
        user = User.objects.get(openid=openid)
        return render(request,"wechat/welcome.html",{"flag":"2","user":user} )
    else:
        return  render(request,"wechat/index.html",context)



#返回实时状态
def state(request):
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]
    nodes = Node.objects.filter(time__gt=charge.start_time).order_by("-time")
    return HttpResponse(nodes[0].voltage_value)



#反向控制
def control(request):
    user = getUser(request)
    charge = Charge.objects.filter(user=user).order_by("-start_time")[0]



#查询消费记录
def history(request):
    user = getUser(request)
    charges = Charge.objects.filter(user=user).order_by("-start_time")
    print charges
    for charge in charges:
        account = Account.objects.get(charge=charge)
        content = content+"充电时间：\n" + str(account.charge.start_time) + "---" + str(account.charge.end_time) + "\n充电费用：" + str(account.money) + "\n******************\n"
    return HttpResponse(content)


#返回充电站的信息列表
def AmmeterGroupUrl(request):
    user = getUser(request)
    group  = AmmeterGroup.objects.all()




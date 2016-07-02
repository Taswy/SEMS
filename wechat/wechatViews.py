# author: HuYong
#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from models.models import User
import requests
import json
AppID = 'wxce660ee67e094937'
AppSecret = '10108b4f9ec7bb9b76f4699087f620e6'
def bangding(request):
    code = request.REQUEST.get("code")
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code"
    url = url.replace("APPID",AppID).replace("SECRET",AppSecret).replace("CODE",code)
    rjson = requests.get(url)
    r = json.loads(rjson.text)
    openid = r["openid"]
    print openid
    context = {"openid":openid}
    count  = User.objects.filter(openid=openid).count()
    if count>0:
        user = User.objects.get(openid=openid)
        return render(request,"wechat/welcome.html",{"flag":"2","user":user} )
    else:
        return  render(request,"wechat/index.html",context)
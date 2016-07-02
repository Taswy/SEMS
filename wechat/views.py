# coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
from models.models import User
import os


def regist(request):
    openid = request.GET.get("openid")
    print openid
    return render(request, "wechat/regist.html",{"openid":openid})


def doregist(request):
    if request.method == 'POST':  # 当提交表单时
        username = request.POST.get("username","")
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


def dologin(request):
    student_number = request.POST.get("student_number", "")
    password = request.POST.get("password", "")
    openid = request.POST.get("openid", "")
    print openid
    if openid == "":
        print student_number
        user = User.objects.filter(student_number=student_number)[0]
        if user.password == password:
            context = {"user": user,"flag":"1"}
            request.session['userid']=user.id
            return render(request, "wechat/welcome.html", context)
        else:
            return redirect("/wechat")
    else:
        print student_number
        user = User.objects.filter(student_number=student_number)[0]
        print user
        if user.password == password:
            user.openid = openid
            user.save()
            context = {"user": user,"flag":"0"}
            request.session['userid']=user.id
            return render(request, "wechat/welcome.html", context)
        else:
            return HttpResponse("绑定失败！")

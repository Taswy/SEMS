# coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
from models.models import User
from wechat.form import UserForm
import os

def getimage(request):
    path = os.getcwd().replace("\\",'/')
    image = open(path+"/wechat/test.jpg","rb").read()
    return HttpResponse(image,content_type="application/image")



def regist(request):
    form = UserForm()
    openid = request.GET.get("openid")
    print openid
    return render(request, "wechat/regist.html",{'form':form,"openid":openid})


def doregist(request):
    if request.method == 'POST':  # 当提交表单时
        form = UserForm(request.POST) # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            student_number = form.cleaned_data['student_number']
            count = User.objects.filter(student_number=student_number).count()
            if count > 0:
                html = '''
                <head>
                <meta http-equiv="refresh" content="1;url=/wechat/regist">
                </head>
                此账号已被注册'''
                return HttpResponse(html)
            else:
                openid = request.POST.get("openid")
                if openid == "":
                    new = User(username=username, password=password,student_number=student_number)
                    new.save()
                # 邮件发送！
                # from_student_number = settings.DEFAULT_FROM_student_number
                # context = "恭喜你注册成功！"+"您的账号是："+username+"；您的密码是："+password
                # send_mail('Welcome', context, from_student_number, [student_number], fail_silently=False)
                    return redirect("/wechat")
                else:
                    new = User(username=username, password=password,student_number=student_number,openid=openid)
                    new.save()
                    return render(request,"wechat/welcome.html",{"openid":openid,"user":new})
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
    openid = request.POST.get("openid", "openid")
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

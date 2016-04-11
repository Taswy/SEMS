# coding=utf-8
from django.shortcuts import render, redirect, HttpResponse
from models.models import User
from wechat.form import UserForm


def index(request):
    return render(request, "wechat/index.html")


def regist(request):
    form = UserForm()
    openid = request.GET.get("openid")
    print openid
    return render(request, "wechat/regist.html",{'form':form,"openid":openid})


def doregist(request):
    if request.method == 'POST':# 当提交表单时
        form = UserForm(request.POST) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            student_number = form.cleaned_data['student_number']
            count = User.objects.filter(student_number=student_number).count()
            if count>0:
                html = '''
                <head>
                <meta http-equiv="refresh" content="1;url=/wechat/regist">
                </head>
                此账号已被注册'''
                return HttpResponse(html)
            else:
                openid = request.POST.get("openid")
                if openid=="":
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
                格式错误！!'''
            return HttpResponse(html)


def dologin(request):
    student_number = request.POST.get("student_number", "")
    password = request.POST.get("password", "")
    openid = request.POST.get("openid", "openid")
    if openid == "":
        user = User.objects.get(student_number=student_number)
        if user.password == password:
            comtext = {"user": user,"flag":"1"}
            request.session['userid']=user.id
            return render(request, "wechat/welcome.html", comtext)
        else:
            return redirect("/wechat")
    else:
        user = User.objects.get(student_number=student_number)
        if user.password == password:
            user.openid = openid
            user.save()
            comtext = {"user": user,"flag":"0"}
            request.session['userid']=user.id
            return render(request, "wechat/welcome.html", comtext)
        else:
            return HttpResponse("绑定失败！")




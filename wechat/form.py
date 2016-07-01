# author: HuYong
#-*- coding: utf-8 -*-
from django import forms
class UserForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=5,required=True,label="用户名")
    password = forms.CharField(min_length=3,widget=forms.PasswordInput,label="密码")
    student_number = forms.CharField(max_length=20,min_length=5,required=True,label="学号")

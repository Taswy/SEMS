# author: HuYong
#coding=utf-8
from django.conf.urls import url
from wechat import views,wechat_index,wechatViews


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^regist$',views.regist),
    url(r'^doregist$',views.doregist),
    url(r'^dologin$',views.dologin),
    url(r'^wechat_index$',wechat_index.index),
    url(r'^bangding$',wechatViews.bangding),

]
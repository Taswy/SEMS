# author: HuYong
#coding=utf-8
from django.conf.urls import url
from service import views


urlpatterns = [
    url(r'^checkStudent',views.checkStudent),
    url(r'^start',views.start),
    url(r'^end',views.end),
    url(r'^charge',views.charge),
]
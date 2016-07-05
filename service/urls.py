# author: HuYong
#coding=utf-8
from django.conf.urls import url
from service import views
from service import actions

urlpatterns = [
    url(r'^checkStudent',views.checkStudent),
    url(r'^start',views.start),
    url(r'^end',views.end),
    url(r'^charge',views.charge),
    url(r'^AmmeterControl',views.AmmeterControl),
    url(r'^money',views.money),
    #url(r'^display',actions.display),
]
# author: HuYong
# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from wechat import wechat_index, wechatViews

urlpatterns = [
    url(r'^wechat_index$', wechat_index.index),
    url(r'^index$', TemplateView.as_view(template_name="wechat/index.html")),
    url(r'^doregist$', wechatViews.doregist),
    url(r'^bind$', wechatViews.bind),
    url(r'^state$', wechatViews.state),
    url(r'^control$', wechatViews.control),
    url(r'^history$', wechatViews.history),
    url(r'^nearby$', wechatViews.nearby),
]

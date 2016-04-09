#coding=utf-8
from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    username = models.CharField(null=False,max_length=45)
    openid = models.CharField(null=False,max_length=45)
    password = models.CharField(null=False,max_length=16)
    student_number = models.IntegerField(unique=True,null=False)
    phonenumber = models.CharField(null=False,max_length=45)
    mark = models.IntegerField(default=0)
    def __unicode__(self):
        return u'用户名：%s,学号：%d'%(self.username,self.student_number)

class Manager(models.Model):
    name = models.CharField(null=False,max_length=45)
    password = models.CharField(null=False,max_length=16)
    POWER_CHOICE = (('0','GENERAL'), ('1','ASSOCIATE'))
    power = models.CharField(max_length=1, choices=POWER_CHOICE)
    def __unicode__(self):
        return u'管理员：%s,权限：%s'%(self.name,self.power)

class Ammeter(models.Model):
    name = models.CharField(null=False,max_length=45)
    longitude = models.FloatField() # 经度
    latitude = models.FloatField() # 纬度
    STATUS_CHOICE = (('0','ON'),('1','OFF'),('2','ABNORMAL'))
    status = models.CharField(max_length=1,choices=STATUS_CHOICE)
    def __unicode__(self):
        return u'id : %s 电表名：%s,经度：%f,纬度：%f,状态：%s'%(self.id,self.name,self.longitude,self.latitude,self.status)

class Charge(models.Model):
    user = models.ForeignKey(User)
    ammeter = models.ForeignKey(Ammeter)
    STATUS_CHOICE = (('0','CHARGING'),('1', 'DONE'),('2' ,'ABNORMAL'))
    status = models.CharField(max_length=1,choices=STATUS_CHOICE)
    start_time = models.DateTimeField(null=False,default=timezone.now)
    end_time = models.DateTimeField(blank=True,null=True)
    overtime = models.IntegerField(default=0)
    message = models.CharField(max_length=200,blank=True)
    #last_change_time = models.DateTimeField(default=timezone.now(),auto_now=)
    def __unicode__(self):
        return u'用户名：%s,电表id：%s,状态：%s,开始时间：%s,结束时间：%s'%(self.user.username,self.ammeter.id,self.status,self.start_time,self.end_time)

class Account(models.Model):
    charge = models.ForeignKey(Charge)
    money = models.DecimalField(max_digits=4,decimal_places=2,null=False,default=0.00)
    message = models.CharField(max_length=200,blank=True)
    def __unicode__(self):
        return u'充电记录id：%d,金额：%f'%(self.charge_id,self.money)
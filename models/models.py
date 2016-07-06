# coding=utf-8
from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    card_number = models.CharField(null=False,max_length=45,verbose_name=u"序列号")#必须
    student_number = models.CharField(null=False, max_length=45,verbose_name=u"学号")#必须
    username = models.CharField(null=True,blank=True, max_length=45,verbose_name=u"用户名")
    openid = models.CharField(null=True,blank=True, max_length=45)
    password = models.CharField(null=True,blank=True, max_length=16,verbose_name=u"密码")
    phone_number = models.CharField(null=True, max_length=45, blank=True,verbose_name=u"电话号码")
    longitude = models.FloatField(null=True,blank=True,verbose_name=u'经度')  # 经度
    latitude = models.FloatField(null=True,blank=True,verbose_name=u'维度')  # 纬度
    USAGE_CHOICE = (("0",u"不可用"),("1",u"可用"))
    usage = models.CharField(null=True,choices=USAGE_CHOICE,max_length=1,default='1', blank=True,verbose_name=u"可用度")   #用以标记用户的可用度
    default_money = models.FloatField(null=True,blank=True,default=0.00,verbose_name=u"拖欠金额") #用户上次拖欠金额

    def __unicode__(self):
        return u'用户名：%s,学号：%s' % (self.username, self.student_number)

    class Meta:
        verbose_name_plural = u"用户"


class Manager(models.Model):
    name = models.CharField(null=False, max_length=45)
    password = models.CharField(null=False, max_length=16)
    POWER_CHOICE = (('0', 'GENERAL'), ('1', 'ASSOCIATE'))
    power = models.CharField(max_length=1, choices=POWER_CHOICE)

    def __unicode__(self):
        return u'管理员：%s,权限：%s' % (self.name, self.power)

    class Meta:
        verbose_name_plural = u"管理员"


class AmmeterGroup(models.Model):
    ammeterGroup_number = models.CharField(null=False,max_length=45,verbose_name=u'编号')
    ammeterGroup_name = models.CharField(null=False,max_length=45,blank=True,verbose_name=u'名称')
    longitude = models.FloatField(null=True,blank=True,verbose_name=u'经度')  # 经度
    latitude = models.FloatField(null=True,blank=True,verbose_name=u'维度')  # 纬度
    valid_number = models.IntegerField(null=False,default=0,verbose_name=u"闲置电表数量")
    sum_number = models.IntegerField(null=False,default=0,verbose_name=u"站组电表总量")

    def __unicode__(self):
        return u'id:%d 序列号:%s 名称:%s' % (self.id,self.ammeterGroup_number,self.ammeterGroup_name)

    class Meta:
        verbose_name_plural = u"充电站组"


class Ammeter(models.Model):
    ammeter_number = models.CharField(null=False,max_length=45)
    name = models.CharField(null=False, max_length=45)
    STATUS_CHOICE = (('0', u'开启'), ('1', u'关闭'), ('2', u'低压'), ('3', u'异常'),('4', u'闲置'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICE,default='1',verbose_name=u'电表状态')
    group = models.ForeignKey(AmmeterGroup,verbose_name=u"所属站组")

    def __unicode__(self):
        return u'id : %s 电表名：%s,状态：%s' % (self.id, self.name, self.status)

    class Meta:
        verbose_name_plural = u"充电站"


class Charge(models.Model):
    user = models.ForeignKey(User,verbose_name=u'用户')
    ammeter = models.ForeignKey(Ammeter,verbose_name=u'电表')
    STATUS_CHOICE = (('0', u'正在充电'), ('1', u'充电完成'), ('2', u'充电异常'))
    status = models.CharField(null=False,max_length=1, choices=STATUS_CHOICE,default='0',verbose_name=u'充电状态')
    start_time = models.DateTimeField(null=False, default=timezone.now,verbose_name=u'开始时间')
    end_time = models.DateTimeField(blank=True, null=True,verbose_name=u'结束时间')
    overtime = models.IntegerField(blank=True, null=True,default=0,verbose_name=u'超时')
    message = models.CharField(blank=True, null=True,max_length=200,verbose_name=u'备注')
    '''
    def __init__(self,user=None,ammeter=None):
        self.ammeter = ammeter
        self.user = user
        self.adding = True
        '''
    class Meta:
        verbose_name_plural = u"充电记录"


    def __unicode__(self):
        return u'用户名：%s,电表id：%s,状态：%s,开始时间：%s' % (
            self.user.username, self.ammeter.ammeter_number, self.status, self.start_time)

class Node(models.Model):
    charge = models.ForeignKey(Charge)
    current_value = models.FloatField(null=False,verbose_name=u"电流")
    energy_value = models.FloatField(null=False,verbose_name=u"电能")
    time = models.DateTimeField(null=False, default=timezone.now,verbose_name=u'时刻')
    class Meta:
        verbose_name_plural = u"时值节点"
    def __unicode__(self):
        return u'充电记录：%d 于%s' % (self.charge.id,str(self.time))

class Account(models.Model):
    charge = models.ForeignKey(Charge)
    money = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0.00)
    message = models.CharField(max_length=200, blank=True,null=True)

    def __unicode__(self):
        return u'充电记录id：%d,金额：%s' % (self.charge_id, self.money)

    class Meta:
        verbose_name_plural = "消费记录"


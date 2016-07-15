# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_auto_20160707_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='InitEnergy',
            field=models.IntegerField(default=0, null=True, verbose_name='\u8d77\u59cb\u7535\u538b', blank=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='lowtime',
            field=models.DateTimeField(null=True, verbose_name='\u4f4e\u538b\u65f6\u957f', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='message',
            field=models.CharField(max_length=200, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='money',
            field=models.DecimalField(default=0.0, verbose_name='\u91d1\u989d', max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='ammeter',
            name='ammeter_number',
            field=models.CharField(max_length=45, verbose_name='\u5e8f\u5217\u53f7'),
        ),
        migrations.AlterField(
            model_name='ammeter',
            name='name',
            field=models.CharField(max_length=45, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='message',
            field=models.CharField(default=b'0,0,0,1,1,0', max_length=200, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='overtime',
            field=models.DateTimeField(null=True, verbose_name='\u8d85\u65f6', blank=True),
        ),
    ]

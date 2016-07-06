# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_auto_20160703_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='ammetergroup',
            name='ammeterGroup_name',
            field=models.CharField(max_length=45, verbose_name='\u540d\u79f0', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='\u7ef4\u5ea6', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='\u7ecf\u5ea6', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='message',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ammetergroup',
            name='ammeterGroup_number',
            field=models.CharField(max_length=45, verbose_name='\u7f16\u53f7'),
        ),
    ]

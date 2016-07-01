# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_auto_20160701_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ammetergroup',
            name='name',
        ),
        migrations.AddField(
            model_name='ammeter',
            name='ammeter_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ammetergroup',
            name='ammeterGroup_number',
            field=models.CharField(default=datetime.datetime(2016, 7, 2, 0, 6, 37, 971000), max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ammeter',
            name='group',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u7ad9\u7ec4', to='models.AmmeterGroup'),
        ),
        migrations.AlterField(
            model_name='ammeter',
            name='status',
            field=models.CharField(default=b'1', max_length=1, verbose_name='\u7535\u8868\u72b6\u6001', choices=[(b'0', '\u5f00\u542f'), (b'1', '\u5173\u95ed'), (b'2', '\u4f4e\u538b'), (b'3', '\u5f02\u5e38')]),
        ),
        migrations.AlterField(
            model_name='ammetergroup',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='\u7ef4\u5ea6', blank=True),
        ),
        migrations.AlterField(
            model_name='ammetergroup',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='\u7ecf\u5ea6', blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='ammeter',
            field=models.ForeignKey(verbose_name='\u7535\u8868', to='models.Ammeter'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='message',
            field=models.CharField(max_length=200, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='overtime',
            field=models.IntegerField(default=0, null=True, verbose_name='\u8d85\u65f6', blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='status',
            field=models.CharField(default=b'0', max_length=1, verbose_name='\u5145\u7535\u72b6\u6001', choices=[(b'0', '\u6b63\u5728\u5145\u7535'), (b'1', '\u5145\u7535\u5b8c\u6210'), (b'2', '\u5145\u7535\u5f02\u5e38')]),
        ),
        migrations.AlterField(
            model_name='charge',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to='models.User'),
        ),
    ]

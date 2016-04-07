# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='weixin',
            new_name='openid',
        ),
        migrations.AlterField(
            model_name='account',
            name='message',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='ammeter',
            name='status',
            field=models.CharField(max_length=1, choices=[(b'0', b'ON'), (b'1', b'OFF'), (b'2', b'ABNORMAL')]),
        ),
        migrations.AlterField(
            model_name='charge',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='message',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='status',
            field=models.CharField(max_length=1, choices=[(b'0', b'CHARGING'), (b'1', b'DONE'), (b'2', b'ABNORMAL')]),
        ),
        migrations.AlterField(
            model_name='manager',
            name='power',
            field=models.CharField(max_length=1, choices=[(b'0', b'GENERAL'), (b'1', b'ASSOCIATE')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20160701_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=16)),
                ('power', models.CharField(max_length=1, choices=[(b'0', b'GENERAL'), (b'1', b'ASSOCIATE')])),
            ],
            options={
                'verbose_name_plural': '\u7ba1\u7406\u5458',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='card_number',
            field=models.CharField(max_length=45, verbose_name='\u5e8f\u5217\u53f7'),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_money',
            field=models.FloatField(default=0.0, null=True, verbose_name='\u62d6\u6b20\u91d1\u989d', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='openid',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=16, null=True, verbose_name='\u5bc6\u7801', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=45, null=True, verbose_name='\u7535\u8bdd\u53f7\u7801', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.CharField(max_length=45, verbose_name='\u5b66\u53f7'),
        ),
        migrations.AlterField(
            model_name='user',
            name='usage',
            field=models.CharField(default=b'1', choices=[(b'0', '\u4e0d\u53ef\u7528'), (b'1', '\u53ef\u7528')], max_length=1, blank=True, null=True, verbose_name='\u53ef\u7528\u5ea6'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=45, null=True, verbose_name='\u7528\u6237\u540d', blank=True),
        ),
    ]

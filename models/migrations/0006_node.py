# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_auto_20160702_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_value', models.FloatField(verbose_name='\u7535\u6d41')),
                ('voltage_value', models.FloatField(verbose_name='\u7535\u538b')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u65f6\u523b')),
                ('charge', models.ForeignKey(to='models.Charge')),
            ],
            options={
                'verbose_name_plural': '\u65f6\u503c\u8282\u70b9',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_auto_20160706_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='power_value',
            field=models.FloatField(default=0, verbose_name='\u529f\u7387'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='voltage_value',
            field=models.FloatField(default=0, verbose_name='\u7535\u538b'),
            preserve_default=False,
        ),
    ]

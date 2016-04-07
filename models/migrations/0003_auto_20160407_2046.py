# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20160405_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

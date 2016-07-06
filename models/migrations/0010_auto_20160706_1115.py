# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_auto_20160703_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='energy_value',
            field=models.FloatField(verbose_name='\u7535\u80fd'),
        ),
    ]

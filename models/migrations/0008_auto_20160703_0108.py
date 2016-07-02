# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_auto_20160703_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='ammetergroup',
            name='sum_number',
            field=models.IntegerField(default=0, verbose_name='\u7ad9\u7ec4\u7535\u8868\u603b\u91cf'),
        ),
        migrations.AddField(
            model_name='ammetergroup',
            name='valid_number',
            field=models.IntegerField(default=0, verbose_name='\u95f2\u7f6e\u7535\u8868\u6570\u91cf'),
        ),
    ]

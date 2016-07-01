# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20160701_1458'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Manager',
        ),
        migrations.AlterField(
            model_name='user',
            name='card_number',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='student_number',
            field=models.CharField(max_length=45),
        ),
    ]

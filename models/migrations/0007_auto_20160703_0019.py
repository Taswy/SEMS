# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ammeter',
            name='status',
            field=models.CharField(default=b'1', max_length=1, verbose_name='\u7535\u8868\u72b6\u6001', choices=[(b'0', '\u5f00\u542f'), (b'1', '\u5173\u95ed'), (b'2', '\u4f4e\u538b'), (b'3', '\u5f02\u5e38'), (b'4', '\u95f2\u7f6e')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.DecimalField(default=0.0, max_digits=4, decimal_places=2)),
                ('message', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'verbose_name_plural': '\u6d88\u8d39\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Ammeter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('status', models.CharField(max_length=1, choices=[(b'0', b'ON'), (b'1', b'OFF'), (b'2', b'Low'), (b'3', b'ABNORMAL')])),
            ],
            options={
                'verbose_name_plural': '\u5145\u7535\u7ad9',
            },
        ),
        migrations.CreateModel(
            name='AmmeterGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
                'verbose_name_plural': '\u5145\u7535\u7ad9\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_number', models.CharField(unique=True, max_length=45)),
                ('student_number', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': '\u5b66\u751f\u5361',
            },
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(b'0', b'CHARGING'), (b'1', b'DONE'), (b'2', b'ABNORMAL')])),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('overtime', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=200, blank=True)),
                ('ammeter', models.ForeignKey(to='models.Ammeter')),
            ],
            options={
                'verbose_name_plural': '\u5145\u7535\u8bb0\u5f55',
            },
        ),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=45)),
                ('openid', models.CharField(max_length=45, blank=True)),
                ('password', models.CharField(max_length=16)),
                ('phone_number', models.CharField(max_length=45, blank=True)),
                ('usage', models.IntegerField(default=1)),
                ('default_money', models.FloatField(default=0.0)),
                ('card', models.ForeignKey(to='models.Card')),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='charge',
            name='user',
            field=models.ForeignKey(to='models.User'),
        ),
        migrations.AddField(
            model_name='ammeter',
            name='group',
            field=models.ForeignKey(to='models.AmmeterGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='charge',
            field=models.ForeignKey(to='models.Charge'),
        ),
    ]

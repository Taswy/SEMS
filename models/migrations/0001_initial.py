# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.DecimalField(default=0.0, max_digits=4, decimal_places=2)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ammeter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('status', models.CharField(max_length=1, choices=[(0, b'ON'), (1, b'OFF'), (2, b'ABNORMAL')])),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(0, b'CHARGING'), (1, b'DONE'), (2, b'ABNORMAL')])),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('overtime', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=200)),
                ('ammeter', models.ForeignKey(to='models.Ammeter')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=16)),
                ('power', models.CharField(max_length=1, choices=[(0, b'GENERAL'), (1, b'ASSOCIATE')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=45)),
                ('weixin', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=16)),
                ('student_number', models.IntegerField(unique=True)),
                ('phonenumber', models.CharField(max_length=45)),
                ('mark', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='charge',
            name='user',
            field=models.ForeignKey(to='models.User'),
        ),
        migrations.AddField(
            model_name='account',
            name='charge',
            field=models.ForeignKey(to='models.Charge'),
        ),
    ]

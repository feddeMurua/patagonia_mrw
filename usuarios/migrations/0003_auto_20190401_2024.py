# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-01 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_customuser_is_directive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_directive',
            field=models.BooleanField(default=False, verbose_name='Es directivo'),
        ),
    ]

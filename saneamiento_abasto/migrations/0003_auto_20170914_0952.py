# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0002_auto_20170914_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reinspeccion',
            name='fecha',
        ),
        migrations.AlterField(
            model_name='reinspeccion',
            name='turno',
            field=models.DateTimeField(),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-04 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animales', '0006_auto_20190401_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esterilizacion',
            name='turno',
            field=models.DateTimeField(),
        ),
    ]

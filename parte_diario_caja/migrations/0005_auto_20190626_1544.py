# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-26 18:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parte_diario_caja', '0004_movimientodiario_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='arqueodiario',
            name='realizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movimientodiario',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2019, 6, 26, 15, 44, 11, 609987)),
        ),
    ]

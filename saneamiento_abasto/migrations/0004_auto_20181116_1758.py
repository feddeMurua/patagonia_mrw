# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-16 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0003_reinspeccion_origen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reinspeccion',
            name='certificado',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
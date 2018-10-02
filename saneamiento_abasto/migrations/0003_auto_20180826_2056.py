# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-26 23:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0002_auto_20180817_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='reinspeccion',
            name='importe',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='reinspeccion',
            name='total_kg',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]

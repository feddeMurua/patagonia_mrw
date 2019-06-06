# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-06 11:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0019_auto_20190606_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='nro',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterUniqueTogether(
            name='vehiculo',
            unique_together=set([]),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libreta_curso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='fecha_inscripcion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

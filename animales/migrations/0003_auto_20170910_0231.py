# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 05:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animales', '0002_auto_20170910_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retiroentregaanimal',
            name='mascota',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='animales.Mascota'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-17 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0009_auto_20190415_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallecc',
            name='pagado',
        ),
        migrations.AddField(
            model_name='periodocc',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]
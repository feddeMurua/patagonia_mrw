# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-15 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saneamiento_abasto', '0008_periodocc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallecc',
            name='cc',
        ),
        migrations.AddField(
            model_name='detallecc',
            name='periodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='saneamiento_abasto.PeriodoCC'),
        ),
        migrations.AddField(
            model_name='periodocc',
            name='cc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='saneamiento_abasto.CuentaCorriente'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-26 21:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parte_diario_caja', '0005_auto_20190626_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='arqueodiario',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='arqueodiario',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='arqueodiario',
            name='turno',
            field=models.CharField(choices=[(b'Manana', 'Ma\xf1ana'), (b'Tarde', 'Tarde')], default='Ma\xf1ana', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='movimientodiario',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2019, 6, 26, 18, 7, 28, 944388)),
        ),
        migrations.AlterUniqueTogether(
            name='arqueodiario',
            unique_together=set([('fecha', 'turno')]),
        ),
    ]

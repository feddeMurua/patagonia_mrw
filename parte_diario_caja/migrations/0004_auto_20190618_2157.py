# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-19 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parte_diario_caja', '0003_arqueodiario_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arqueodiario',
            name='turno',
            field=models.CharField(choices=[(b'Ma\xc3\xb1ana', 'Ma\xf1ana'), (b'Tarde', 'Tarde')], default='Ma\xf1ana', max_length=10, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-14 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animales', '0004_porcino_precinto2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porcino',
            name='categoria_porcino',
            field=models.CharField(choices=[(b'LECHON', 'LECHON'), (b'PORKER', 'PORKER'), (b'ADULTO', 'ADULTO')], default='LECHON', max_length=6),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-01-16 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreta_curso', '0003_auto_20190116_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libretasanitaria',
            name='fecha_examen_clinico',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='libretasanitaria',
            name='fecha_vencimiento',
            field=models.DateField(null=True),
        ),
    ]

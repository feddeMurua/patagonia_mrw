# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonaGenerica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('domicilio', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('rubro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PersonaFisica',
            fields=[
                ('personagenerica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaGenerica')),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('dni', models.CharField(max_length=50, unique=True)),
                ('nacionalidad', models.CharField(max_length=50)),
                ('obra_social', models.CharField(blank=True, max_length=50)),
                ('documentacion_retirada', models.BooleanField(default=False)),
            ],
            bases=('personas.personagenerica',),
        ),
        migrations.CreateModel(
            name='PersonaJuridica',
            fields=[
                ('personagenerica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaGenerica')),
                ('cuil', models.CharField(max_length=20, unique=True)),
            ],
            bases=('personas.personagenerica',),
        ),
        migrations.CreateModel(
            name='PersonalPropio',
            fields=[
                ('personafisica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaFisica')),
                ('rol_actuante', models.CharField(max_length=50)),
            ],
            bases=('personas.personafisica',),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-02 15:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barrio', models.CharField(blank=True, max_length=20, null=True)),
                ('calle', models.CharField(max_length=50)),
                ('calle_entre1', models.CharField(blank=True, max_length=50, null=True)),
                ('calle_entre2', models.CharField(blank=True, max_length=50, null=True)),
                ('nro', models.IntegerField()),
                ('dpto', models.CharField(blank=True, max_length=50, null=True)),
                ('piso', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomicilioRural',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chacra', models.CharField(max_length=4)),
                ('parcela', models.CharField(blank=True, max_length=4, null=True)),
                ('sector', models.CharField(blank=True, max_length=3, null=True)),
                ('circunscripcion', models.CharField(blank=True, max_length=3, null=True)),
                ('ruta', models.CharField(blank=True, max_length=25, null=True)),
                ('km', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('cp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonaGenerica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('nacionalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Nacionalidad')),
            ],
        ),
        migrations.CreateModel(
            name='RolActuante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PersonaFisica',
            fields=[
                ('personagenerica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaGenerica')),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('dni', models.CharField(max_length=50, unique=True)),
                ('obra_social', models.CharField(blank=True, max_length=50)),
                ('documentacion_retirada', models.BooleanField(default=False)),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('personas.personagenerica',),
        ),
        migrations.CreateModel(
            name='PersonaJuridica',
            fields=[
                ('personagenerica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaGenerica')),
                ('cuit', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('personas.personagenerica',),
        ),
        migrations.AddField(
            model_name='personagenerica',
            name='domicilio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Domicilio'),
        ),
        migrations.AddField(
            model_name='personagenerica',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_personas.personagenerica_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Provincia'),
        ),
        migrations.AddField(
            model_name='domicilio',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Localidad'),
        ),
        migrations.CreateModel(
            name='PersonalPropio',
            fields=[
                ('personafisica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.PersonaFisica')),
                ('rol_actuante', models.ManyToManyField(to='personas.RolActuante')),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('personas.personafisica',),
        ),
        migrations.AddField(
            model_name='personafisica',
            name='nacionalidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Nacionalidad'),
        ),
    ]

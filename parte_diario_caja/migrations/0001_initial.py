# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-02 15:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArqueoDiario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('nro_planilla', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('mil', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('quinientos', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('doscientos', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cien', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('b_cincuenta', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('veinte', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('diez', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cinco', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('m_dos', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('uno', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('m_cincuenta', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('veinticinco', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarjeta_cant', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarjeta_sub', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cheques_cant', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cheques_sub', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_manual', models.FloatField(null=True)),
                ('mov_efectivo_sis', models.IntegerField(null=True)),
                ('sub_efectivo_sis', models.FloatField(null=True)),
                ('mov_tarjeta_sis', models.IntegerField(null=True)),
                ('sub_tarjeta_sis', models.FloatField(null=True)),
                ('mov_cheque_sis', models.IntegerField(null=True)),
                ('sub_cheque_sis', models.FloatField(null=True)),
                ('mov_total_sistema', models.IntegerField(null=True)),
                ('imp_total_sistema', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleMovimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('importe', models.FloatField()),
                ('servicio', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoDiario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('nro_ingreso', models.BigIntegerField(unique=True)),
                ('forma_pago', models.CharField(choices=[(b'Efectivo', 'Efectivo'), (b'Tarjeta', 'Tarjeta de Debito/Credito'), (b'Cheque', 'Cheque'), (b'Eximido', 'Eximido')], default='Efectivo', max_length=50)),
                ('nro_cheque', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('importe', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parte_diario_caja.TipoServicio'),
        ),
    ]


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from personas import models as m


class Abastecedor(models.Model):
    persona = models.OneToOneField(m.PersonaFisica, on_delete=models.CASCADE)
    empresa_y_o_transporte = models.CharField(max_length=150)
    rubro = models.CharField(max_length=150)

    def __str__(self):
        return "%s - %s" % (self.persona, self.rubro)


class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    dominio = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.marca, self.dominio)

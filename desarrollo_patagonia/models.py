# -*- coding: utf-8 -*-

from django.db import models


class PersonaGenerica(models.Model):
    domicilio = models.CharField(max_length=50)
    telefono = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=50, blank=True)
    rubro = models.CharField(max_length=50)

    class Meta:
        abstract = True

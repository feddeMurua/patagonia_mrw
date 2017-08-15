# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    Patente,
    Mascota,    
)

admin.site.register(Patente)
admin.site.register(Mascota)

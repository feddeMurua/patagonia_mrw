# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import (    
    LibretaSanitaria,
    Curso,
    Inscripcion,
)

admin.site.register(LibretaSanitaria)
admin.site.register(Curso)
admin.site.register(Inscripcion)

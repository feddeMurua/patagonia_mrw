# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    PersonaFisica,
    LibretaSanitaria,
    Curso,
    Inscripcion,
    ExamenClinico   )

admin.site.register(PersonaFisica)
admin.site.register(LibretaSanitaria)
admin.site.register(Curso)
admin.site.register(Inscripcion)
admin.site.register(ExamenClinico)

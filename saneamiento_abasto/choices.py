# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
import sys

reload(sys)
sys.setdefaultencoding('utf8') # Para que no de error por los acentos

Quincenas = (
    ('Primer quincena', _("Primer quincena")),
    ('Segunda quincena', _("Segunda quincena")),
)

Categoria = (
    ('Categoria A',
     _("Transporte isotérmico con equipo de frio para transportar productos congelados")),

     ('Categoria B',
      _("Transporte isotérmico con equipo de frio para transportar productos refrigerados")),

      ('Categoria C',
       _("Transporte isotérmico de productos envasados que no requieran refrigeración")),

       ('Categoria D',
        _("Transporte con caja abierta y protección mediante lona o toldo")),

        ('Categoria E',
         _("Otros")),
)

Plagas = (
    ('Palomas', _("Palomas")),
    ('Ratas', _("Ratas")),
    ('Cucarachas', _("Cucarachas")),
    ('Murciélagos', _("Murciélagos")),
    ('Hormigas', _("Hormigas")),
    ('Chinches', _("Chinches")),
    ('Garrapatas', _("Garrapatas")),
    ('Pulgas', _("Pulgas")),
    ('Otros', _("Otros")),
)

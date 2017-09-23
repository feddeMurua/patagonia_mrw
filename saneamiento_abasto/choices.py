# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
import sys

reload(sys)
sys.setdefaultencoding('utf8')  # Para que no de error por los acentos

Quincenas = (
    ('Primer quincena', _("Primer quincena")),
    ('Segunda quincena', _("Segunda quincena")),
)

Categoria = (
    ('Categoria_A',
     _("Transporte isotérmico con equipo de frio para transportar productos congelados")),

    ('Categoria_B',
     _("Transporte isotérmico con equipo de frio para transportar productos refrigerados")),

    ('Categoria_C',
     _("Transporte isotérmico de productos envasados que no requieran refrigeración")),

    ('Categoria_D',
     _("Transporte con caja abierta y protección mediante lona o toldo")),

    ('Categoria_E',
     _("Otros")),
)

Categoria_A = {
    'Productos carneos': "Productos carneos",
    'Aves': "Aves",
    'Pescados': "Pescados",
    'Mariscos': "Mariscos",
    'Hielo': "Hielo",
    'Helados': "Helados"
}

Categoria_B = {
    'Productos carneos': "Productos carneos",
    'Aves': "Aves",
    'Fiambres': "Fiambres",
    'Lacteos': "Lacteos",
    'Pastas': "Pastas",
    'Productos de mar': "Productos de mar",
    'Sandwiches': "Sandwiches",
    'Productos de rotiseria': "Productos de rotiseria"
}

Categoria_C = {
    'Bebidas': "Bebidas",
    'Aguas': "Aguas",
    'Panificados y afines': "Panificados y afines"
}

Categoria_D = {
    'Frutas': "Frutas",
    'Verduras': "Verduras",
    'Huevos': "Huevos",
    'Bebidas': "Bebidas"
}

Categoria_E = {
    'Otros': "Otros"
}

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

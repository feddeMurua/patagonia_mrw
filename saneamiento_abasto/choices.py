# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
import sys

reload(sys)
sys.setdefaultencoding('utf8')  # Para que no de error por los acentos

Tipo_Vehiculo = (
    ('TSA', _("Transporte de Sustancias Alimenticias")),
    ('TPP', _("Transporte Público de Pasajeros"))
)

Marca_vehiculo = (
    ('Alfa Romeo', _("Alfa Romeo")),
    ('Audi', _("Audi")),
    ('BMW', _("BMW")),
    ('Chery', _("Chery")),
    ('Chevrolet', _("Chevrolet")),
    ('Chrysler', _("Chrysler")),
    ('Citroen', _("Citroën")),
    ('Dodge', _("Dodge")),
    ('DS', _("DS")),
    ('Fiat', _("Fiat")),
    ('Ford', _("Ford")),
    ('Honda', _("Honda")),
    ('Hyundai', _("Hyundai")),
    ('Iveco', _("Iveco")),
    ('KIA', _("KIA")),
    ('Land Rover', _("Land Rover")),
    ('Mercedes Benz', _("Mercedes Benz")),
    ('Mini', _("Mini")),
    ('Peugeot', _("Peugeot")),
    ('RAM', _("RAM")),
    ('Renault', _("Renault")),
    ('Suzuki', _("Suzuki")),
    ('Toyota', _("Toyota")),
    ('Volkswagen', _("Volkswagen")),
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

Estado_Desinfeccion = (
    ('Realizada', _("Realizada")),
    ('No realizada', _("No realizada")),
    ('Vencida', _("Vencida"))
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

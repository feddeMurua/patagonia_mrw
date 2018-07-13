from django import template

register = template.Library()


@register.filter
def string_split(format_string):
    mes, anio = format_string.split("-")
    return mes, anio

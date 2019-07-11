# -*- coding: utf-8 -*-
import sys
from django.utils.translation import ugettext as _

reload(sys)
sys.setdefaultencoding('utf8')

TipoPago = (
    ('Efectivo', _("Efectivo")),
    ('Tarjeta', _("Tarjeta de Debito/Credito")),
    ('Cheque', _("Cheque")),
    ('Eximido', _("Eximido")),
)

Turno = (
    ('Manana', _("Mañana")),
    ('Tarde', _("Tarde")),
    ('Completo', _("Completo"))
)

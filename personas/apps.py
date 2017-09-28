# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.contrib.auth.models import User


class PersonasConfig(AppConfig):
    name = 'personas'


'''
class MyAppConfig(AppConfig):
    name = 'personas'

    def ready(self):
        from actstream import registry
        registry.register(User, self.get_model('PersonaFisica'))
'''


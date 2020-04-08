#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define la clase "Perro".

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

__docformat__ = "epytext"

class Perro():
    """La clase Perro trata de implementar un perro real como objeto instanciable."""

    def __init__(self, nombreperro, colorperro, alturaperro, constitucionperro, humorperro, edadperro):
        """Inicializador de la clase Perro"""
        self.nombre = nombreperro
        self.color = colorperro
        self.altura = alturaperro
        self.constitucion = constitucionperro
        self.humor = humorperro
        self.edad = edadperro
        self.hambre = False
        self.cansado = False

    def Comer(self):
        """Ordena al perro comer.\n
        Éste sólo comerá si tiene hambre."""
        if self.hambre:
            print 'Ñam Ñam...'
            self.hambre = False
        else:
            print 'Sniff Sniff... no tengo hambre'

    def Dormir(self):
        """Ordena al perro dormir"""
        print 'zZz...zZz...zZz...zZz...zZz...'

    def Ladrar(self):
        """Ordena al perro ladrar.\n
        El ladrido variará en función de su estado de ánimo."""
        if self.humor == 'enfadado':
            print 'GRRRRR... guau guau'
        elif self.humor == 'tranquilo':
            print 'Waaaahhh...vale...guau'
        elif self.humor == 'loco':
            print 'guau guau guau guau guau guau guau guau guau guau'
        else:
            print 'guau guau'

chucho = Perro('Canelo','marrón','bajito','fondón','enfadado',12)
"""Instancia de la clase Perro"""
print 'Me llamo %s' % chucho.nombre
print 'Soy de color %s' % chucho.color
print 'Estoy %s' % chucho.humor
if chucho.hambre:
    print 'Tengo hambre'
else:
    print 'No tengo hambre'
chucho.Comer()
chucho.hambre = True
chucho.Comer()
chucho.Ladrar()

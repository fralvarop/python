#!/usr/bin/env python
# -*- coding: utf-8 -*-
while True:
    respuesta = raw_input('Escribe algo ("adiós" para salir): ')
    if respuesta == 'adiós':
        print 'Adiós, gilipollas'
        break
    else:
        print '¡Eco! %s' % respuesta

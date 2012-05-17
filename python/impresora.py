#!/usr/bin/env python
# -*- coding: utf-8 -*-

# impresora.py
# Ejemplo de utilización de la impresora

import os

impresora = os.popen('lpr','w')
impresora.write('Prueba de impresión con Python\n')

impresora.close()

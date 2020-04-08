#!/usr/bin/env python
# -*- coding: utf-8 -*-

# imprimir_fichero.py
# Ejemplo de utilización de la impresora

import os
import sys

os.system('lpr %s' % sys.argv[1])

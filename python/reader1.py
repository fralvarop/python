#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
arbol = etree.parse('ejemplo1.xml')

print 'XML original:'
etree.dump(arbol)
persona = arbol.findall('.//persona')
print ''
print 'Árbol de elementos:'
for p in persona:
    for dato in p:
        print '%s: %s' % (dato.tag, dato.text)


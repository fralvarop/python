#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pprint1.py
# Ejemplo de funciones semi-útiles

def Separador(caracter, ancho):
    # El ancho es el ancho total de la linea
    return '%s%s%s' % ('+', (caracter * (ancho-2)), '+')

def Formato(valor1, izda, valor2, dcha):
    # Pinta dos valores ajustados a izquierda y derecha de la linea
    # valor1 es lo que se pinta a la izquierda, valor2 es lo que se pinta a la derecha
    # izda es el tamaño de la parte izquierda, dcha es el tamaño de la parte derecha
    parte2 = '%.2f' % valor2
    return '%s%s%s%s' % ('| ', valor1.ljust(izda - 2, ' '), parte2.rjust(dcha - 2, ' '), ' |')

# Definimos el precio de cada articulo
item1 = 3.00
item2 = 15.00
# Mostramos todo, pero bonito
print Separador('=', 40)
print Formato('Item 1', 30, item1, 10)
print Formato('Item 2', 30, item2, 10)
print Separador('-', 40)
print Formato('Total', 30, item1 + item2, 10)
print Separador('=', 40)

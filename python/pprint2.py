#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pprint2.py
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
articulos = [['Cafe',0.5],['Chucherias',2.45],['Pan',1.35],['Leche',0.9]]

# Mostramos todo, pero bonito
print Separador('=', 40)
total = 0
for articulo in articulos:
    print Formato(articulo[0], 30, articulo[1], 10)
    total += articulo[1]
print Separador('-', 40)
print Formato('Total (sin IVA)', 30, total*0.82, 10)
print Formato('IVA (18 %)', 30, total*0.18, 10)
print Formato('TOTAL', 30, total, 10)
print Separador('=', 40)

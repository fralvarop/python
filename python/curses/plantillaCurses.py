#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

#---------------------------------------
# Plantilla de programación con Curses
#---------------------------------------

def InicializarPantalla(borde):
    if borde:
        pantalla.border(0)

#====================
# Bucle principal
#====================

pantalla = curses.initscr()
InicializarPantalla(True)
try:
    pantalla.refresh()
    # Pon el código aquí
    pantalla.addstr(1,1, "Pulsa cualquier tecla para continuar")
    pantalla.getch()
finally:
    curses.endwin()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

#=======================================
# Ejemplo de programación con Curses 2
#=======================================

try:
    pantalla = curses.initscr()
    pantalla.clear()
    pantalla.addstr(0,0,"0        1         2         3         4         5         6         7")
    pantalla.addstr(1,0,"12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    pantalla.addstr(5,0,"5")
    pantalla.addstr(10,0,"10")
    pantalla.addstr(15,0,"15")
    pantalla.addstr(20,0,"20")
    pantalla.addstr(23,0, "23 - Pulsa cualquier tecla para continuar")
    pantalla.refresh()
    pantalla.getch()
finally:
    curses.endwin()

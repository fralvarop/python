#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

#---------------------------------------
# Ejemplo de programación con Curses 1
#---------------------------------------

pantalla = curses.initscr()
pantalla.border(0)
pantalla.addstr(12, 25, "¡Corre, Curses, corre libre!")
pantalla.refresh()
pantalla.getch()
curses.endwin()

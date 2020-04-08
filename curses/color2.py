#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

def main(pantalla):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    pantalla.clear()
    pantalla.addstr(3,1,"Esto es una prueba",curses.color_pair(1))
    pantalla.addstr(4,1,"Esto es una prueba",curses.color_pair(2))
    pantalla.addstr(5,1,"Esto es una prueba",curses.color_pair(3))
    pantalla.refresh()
    pantalla.getch()

curses.wrapper(main)


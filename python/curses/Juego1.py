#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import random

class Juego1():
    def __init__(self):
        # Lineas
        self.pistolaFila = 22           # Fila donde se mueve la pistola
        self.pistolaColumna = 39        # Columna donde empieza la pistola
        self.letraFila = 2              # Fila en la que la letra se mueve en horizontal
        self.puntuacionFila = 1         # Fila donde mostraremos la puntuacion
        self.puntuacionColumna = 45     # Columna donde mostraremos la puntuacion
        self.vidasColumna = 65          # Columna donde mostraremos las vidas restantes
        # Letras
        self.letraActual = "A"          # Letra a mostrar en cada momento
        self.letraColumnaActual = 78    # Columna donde aparece por primera vez cada letra
        self.columnaCaida = 10          # Columna por la que caera cada letra
        self.letraCayendo = False       # Flag que indica la letra ha iniciado la caida
        self.letraFilaActual = 3        # Fila donde se encuentra la letra en cada momento
        self.letraEspera = 15           # Regulamos la velocidad de la letra respecto a la pistola (numeros grandes = letra lenta)
        # Bala
        self.disparando = False         # Flag que indica si estamos disparando
        self.balaFila = self.pistolaFila - 1
        self.balaColumna = self.pistolaColumna
        # Resto
        self.contadorCiclos = 0         # Cuantos ciclos hemos recorrido en MoverLetra
        self.puntuacion = 0             # Puntuacion actual
        self.vidas = 3                  # Numero de vidas por defecto
        self.colorActual = 1            # Color de la letra
        self.perderAlFallar = False     # Marcar como True si queremos que cuente como fallo el que una letra llegue al suelo

    def MoverLetra(self,pantalla):
        # Si la letra todavia planea...
        if self.contadorCiclos == self.letraEspera:
            self.contadorCiclos = 0
            if not self.letraCayendo:
                pantalla.addch(self.letraFila,self.letraColumnaActual," ")
                curses.napms(50)
                if self.letraColumnaActual > 2:
                    self.letraColumnaActual -= 1
                pantalla.addch(self.letraFila,self.letraColumnaActual,self.letraActual,curses.color_pair(self.colorActual))
                if self.letraColumnaActual == self.columnaCaida:
                    self.letraCayendo = True
                self.letraFilaActual = self.letraFila
                self.ComprobarImpacto(pantalla)
            else:
                # Si la letra esta en caida...
                pantalla.addch(self.letraFilaActual,self.letraColumnaActual," ")
                curses.napms(50)
                if self.letraFilaActual < self.pistolaFila:
                    self.letraFilaActual += 1
                    pantalla.addch(self.letraFilaActual,self.letraColumnaActual,self.letraActual,curses.color_pair(self.colorActual))
                    self.ComprobarImpacto(pantalla)
                else:
                    if self.perderAlFallar:
                        self.Explotar(pantalla)
                        self.puntuacion -= 1
                        self.vidas -= 1
                        self.MostrarPuntuacion(pantalla)
                        self.PrepararNuevaLetra()
                    else:
                        if self.letraColumnaActual == self.pistolaColumna:
                            self.Explotar(pantalla)
                            self.puntuacion -= 1
                            self.vidas -= 1
                            self.MostrarPuntuacion(pantalla)
                            self.PrepararNuevaLetra()
                        else:
                            self.Explotar(pantalla)
                            self.PrepararNuevaLetra()
        else:
            self.contadorCiclos += 1
        if self.disparando:
            self.MoverBala(pantalla)
            self.ComprobarImpacto(pantalla)
        pantalla.refresh

    def MoverBala(self,pantalla):
        pantalla.addch(self.balaFila,self.balaColumna," ")
        if self.balaFila > self.letraFila:
            self.ComprobarImpacto(pantalla)
            self.balaFila -= 1
            pantalla.addch(self.balaFila,self.balaColumna,"|")
        else:
            self.ComprobarImpacto(pantalla)
            pantalla.addch(self.balaFila,self.balaColumna," ")
            self.balaFila = self.pistolaFila - 1
            self.disparando = False

    def Explotar(self,pantalla):
        pantalla.addch(self.letraFilaActual,self.letraColumnaActual,"X",curses.color_pair(5))
        curses.napms(100)
        pantalla.refresh()
        pantalla.addch(self.letraFilaActual,self.letraColumnaActual,"|",curses.color_pair(5))
        curses.napms(100)
        pantalla.refresh()
        pantalla.addch(self.letraFilaActual,self.letraColumnaActual,"-",curses.color_pair(5))
        curses.napms(100)
        pantalla.refresh()
        pantalla.addch(self.letraFilaActual,self.letraColumnaActual,".",curses.color_pair(5))
        curses.napms(100)
        pantalla.refresh()
        pantalla.addch(self.letraFilaActual,self.letraColumnaActual," ")
        pantalla.addch(self.pistolaFila,self.pistolaColumna,self.CaracterPistola,curses.color_pair(2) | curses.A_BOLD)
        pantalla.refresh()

    def PrepararNuevaLetra(self):
        self.letraFilaActual = self.letraFila
        self.letraColumnaActual = 78
        self.letraCayendo = False
        self.ElegirLetra()
        self.ElegirColor()
        self.ElegirPuntoCaida()

    def ElegirLetra(self):
        random.seed()
        self.letraActual = chr(random.randint(65,90))

    def ElegirColor(self):
        random.seed()
        self.colorActual = random.randint(1,4)

    def LeerTeclas(self,pantalla,tecla):
        if tecla == 260: # Flecha izquierda (NO keypad)
            self.MoverPistola(pantalla,0)
            curses.flushinp()  # Limpiamos el buffer de entrada por seguridad
        elif tecla == 261: # Flecha derecha (NO keypad)
            self.MoverPistola(pantalla,1)
            curses.flushinp()  # Limpiamos el buffer de entrada por seguridad
        elif tecla == 52:  # Flecha izquierda (keypad)
            self.MoverPistola(pantalla,0)
            curses.flushinp()  # Limpiamos el buffer de entrada por seguridad
        elif tecla == 54:  # Flecha derecha (keypad)
            self.MoverPistola(pantalla,1)
            curses.flushinp()  # Limpiamos el buffer de entrada por seguridad
        elif tecla == 32:  # Barra espaciadora
            if not self.disparando:
                self.disparando = True
                self.balaColumna = self.pistolaColumna
                pantalla.addch(self.balaFila,self.balaColumna,"|")
                curses.flushinp()  # Limpiamos el buffer de entrada por seguridad

    def MoverPistola(self,pantalla,direccion):
        pantalla.addch(self.pistolaFila,self.pistolaColumna," ")
        if direccion == 0:    # Izquierda
            if self.pistolaColumna > 0:
                self.pistolaColumna -= 1
        elif direccion == 1:  # Drecha
            if self.pistolaColumna < 79:
                self.pistolaColumna += 1
        pantalla.addch(self.pistolaFila,self.pistolaColumna,self.CaracterPistola,curses.color_pair(2) | curses.A_BOLD)

    def ElegirPuntoCaida(self):
        random.seed()
        self.columnaCaida = random.randint(3,78)

    def BucleJuego(self,pantalla):
        while True:
            curses.napms(20)
            self.MoverLetra(pantalla)
            tecla = pantalla.getch(self.puntuacionFila,self.puntuacionColumna)
            if tecla == ord('Q') or tecla == ord('q') or tecla == 27:  # 'Q' o <Esc>
                break
            else:
                self.LeerTeclas(pantalla,tecla)
            self.MostrarPuntuacion(pantalla)
            if self.vidas == 0:
                break
        curses.flushinp()
        pantalla.clear()

    def JuegoNuevo(self,pantalla):
        self.CaracterPistola = curses.ACS_SSBS
        pantalla.addch(self.pistolaFila,self.pistolaColumna,self.CaracterPistola,curses.color_pair(2) | curses.A_BOLD)
        pantalla.nodelay(1)    # No esperamos una pulsacion, cacheamos y punto
        self.PrepararNuevaLetra()
        self.puntuacion = 0
        self.vidas = 3
        self.MostrarPuntuacion(pantalla)
        pantalla.move(self.puntuacionFila,self.puntuacionColumna)

    def MostrarPuntuacion(self,pantalla):
        pantalla.addstr(self.puntuacionFila,self.puntuacionColumna,"Puntuacion: %d" % self.puntuacion)
        pantalla.addstr(self.puntuacionFila,self.vidasColumna,"Vidas: %d" % self.vidas)

    def ComprobarImpacto(self,pantalla):
        if self.disparando:
            if self.balaFila == self.letraFilaActual:
                if self.balaColumna == self.letraColumnaActual:
                    pantalla.addch(self.balaFila,self.balaColumna," ")
                    self.ExplotarBala(pantalla)
                    self.puntuacion +=1
                    self.PrepararNuevaLetra()

    def ExplotarBala(self,pantalla):
        pantalla.addch(self.balaFila,self.balaColumna,"X",curses.color_pair(5))
        pantalla.refresh()
        curses.napms(200)
        pantalla.addch(self.balaFila,self.balaColumna,"|",curses.color_pair(5))
        pantalla.refresh()
        curses.napms(200)
        pantalla.addch(self.balaFila,self.balaColumna,"-",curses.color_pair(5))
        pantalla.refresh()
        curses.napms(200)
        pantalla.addch(self.balaFila,self.balaColumna,".",curses.color_pair(5))
        pantalla.refresh()
        curses.napms(200)
        pantalla.addch(self.balaFila,self.balaColumna," ",curses.color_pair(5))
        pantalla.refresh()
        curses.napms(200)

    def main(self,pantalla):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
        pantalla.addstr(11,18,"Bienvenido a EL ATAQUE DE LAS LETRAS")
        pantalla.addstr(13,18,"Pulsa cualquier tecla para empezar...")
        pantalla.getch()
        pantalla.clear()
        while True:
            self.JuegoNuevo(pantalla)
            self.BucleJuego(pantalla)
            pantalla.nodelay(0)
            curses.flushinp()
            pantalla.addstr(11,35,"FIN")
            pantalla.addstr(13,23,"Quieres volver a jugar? (S/N)")
            tecla = pantalla.getch(14,56)
            if tecla == ord("N") or tecla == ord("n"):
                break
            else:
                pantalla.clear()

    def Arrancar(self):
        curses.wrapper(self.main)

juego = Juego1()
juego.Arrancar()


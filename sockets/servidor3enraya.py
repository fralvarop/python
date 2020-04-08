#!/usr/bin/env python
# -*- coding: utf-8 -*-

# servidor3enraya.py

from socket import *
import sys
import os

TAM_BUFFER = 4096
HOST = ''
PUERTO = 29876
DIRECCION = (HOST,PUERTO)

class Servidor3enRaya:
    def __init__(self):
       self.socket_servidor = socket(AF_INET, SOCK_STREAM)
       self.socket_servidor.bind((DIRECCION))
       self.linea_comandos = None
       self.bucle_proceso = False
       self.jugador = 1
       self.tablero = [['-','-','-'],['-','-','-'],['-','-','-']]
       self.escuchar()

    def escuchar(self):
        while True:
            # Escuchamos por el socket creado
            self.socket_servidor.listen(5)
            print 'Escuchando a los clientes que lleguen'
            # Cada conexión nos da una línea de comandos y una dirección origen
            linea_comandos, direccion = self.socket_servidor.accept()
            self.linea_comandos = linea_comandos
            print 'Conexión establecida desde', direccion
            self.bucle_proceso = True
            while self.bucle_proceso:
               self.procesarComando()
            self.linea_comandos.close()
        self.socket_servidor.close()

    def procesarComando(self):
        # Recibimos comandos
        comando = self.linea_comandos.recv(TAM_BUFFER)
        if comando:
            # Procesamos el comando
            print 'Procesando comando: %s' % comando
            comando = comando.strip()
            # Los clientes se desconectan enviando el comando 'BYE'
            if comando == 'BYE':
                self.bucle_proceso = False
            if self.bucle_proceso:
                # El comando 'Empezar' comienza una nueva partida
                if comando == 'Empezar':
                    self.InicializarTablero()
                    self.MostrarTablero(True)
                # Aceptamos movimientos con el comando 'Mover'
                if comando[:5] == 'Mover':
                    print 'MOVIMIENTO'
                    posicion = comando[6:]
                    print 'Posición = ' + posicion
                    if posicion[0] == 'A':
                        fila = 0
                    elif posicion[0] == 'B':
                        fila = 1
                    elif posicion[0] == 'C':
                        fila = 2
                    else:
                        self.linea_comandos.send('Posición no válida')
                        return
                    columna = int(posicion[1])-1
                    print 'Columna = %s, Fila = %s' % (columna, fila)
                    if fila < 0 or fila > 2:
                        self.linea_comandos.send('Posición no válida')
                        return
                    # Pintamos movimientos con una 'X' o una 'O'
                    if self.tablero[fila][columna] == '-':
                        if self.jugador == 1:
                            self.tablero[fila][columna] = "X"
                        else:
                            self.tablero[fila][columna] = "O"
                    self.MostrarTablero(False)

    def InicializarTablero(self):
        self.tablero = [['-','-','-'],['-','-','-'],['-','-','-']]

    def MostrarTablero(self,estado_inicial):
        salida = ('   1   2   3') + chr(13) + chr(10)
        salida += (" A {0} | {1} | {2}".format(self.tablero[0][0],self.tablero[0][1],self.tablero[0][2]))+ chr(13)+chr(10)
        salida += ('  ------------')+ chr(13)+chr(10)
        salida += (" B {0} | {1} | {2}".format(self.tablero[1][0],self.tablero[1][1],self.tablero[1][2]))+ chr(13)+chr(10)
        salida += ('  ------------')+ chr(13)+chr(10)
        salida += (" C {0} | {1} | {2}".format(self.tablero[2][0],self.tablero[2][1],self.tablero[2][2]))+ chr(13)+chr(10)
        salida += ('  ------------')+ chr(13)+chr(10)
        if not estado_inicial:
            if self.jugador == 1:
                victoria = self.comprobarVictoria("X")
            else:
                victoria = self.comprobarVictoria("O")
            if victoria:
                if self.jugador == 1:
                    salida += "¡Gana el jugador 1!"
                else:
                    salida += "¡Gana el jugador 2!"
            else:
                if self.jugador == 1:
                    self.jugador = 2
                else:
                    self.jugador = 1
                salida += ('Introduce movimiento para el jugador %s' % self.jugador)
        self.linea_comandos.send(salida)

    def comprobarVictoria(self,jugador):
        # Recorremos todas las filas y columnas
        for c in range(0,3):
        # Líneas horizontales
            if self.tablero[c][0] == jugador and self.tablero[c][1] == jugador and self.tablero[c][2] == jugador:
              print '*********\n\n%s gana\n\n*********' % jugador
              return True
            # Líneas verticales
            elif self.tablero[0][c] == jugador and self.tablero[1][c] == jugador and self.tablero[2][c] == jugador:
              print '*********\n\n%s gana\n\n*********' % jugador
              return True
            # Diagonal (de izquierda a derecha)
            elif self.tablero[0][0] == jugador and self.tablero[1][1] == jugador and self.tablero[2][2] == jugador:
              print '*********\n\n%s gana\n\n*********' % jugador
              return True
            # Diagonal (de derecha a izquierda)
            elif self.tablero[0][2] == jugador and self.tablero[1][1] == jugador and self.tablero[2][0] == jugador:
              print '*********\n\n%s gana\n\n*********' % jugador
              return True
        else:
            return False

if __name__ == '__main__':
   servidor = Servidor3enRaya()


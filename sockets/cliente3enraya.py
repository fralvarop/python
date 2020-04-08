#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cliente2.py

from socket import *
from time import time
from time import sleep
import sys
import string

TAM_BUFFER = 4096

class LineaComandos:
    def __init__(self,host):
        self.HOST = host
        self.PUERTO = 29876
        self.DIRECCION = (self.HOST,self.PUERTO)
        self.socket_cliente = None

    def abrirConexion(self):
        self.socket_cliente = socket(AF_INET,SOCK_STREAM)
        self.socket_cliente.connect(self.DIRECCION)

    def enviarComando(self, comando):
        self.socket_cliente.send(comando)

    def recibirResultado(self):
        resultado = self.socket_cliente.recv(TAM_BUFFER)
        print resultado
        return resultado

if __name__ == '__main__':
    conexion = LineaComandos('localhost')
    conexion.abrirConexion()
    conexion.enviarComando('Empezar')
    resultado = conexion.recibirResultado()
    while string.find(resultado, "Gana") == -1:
        movimiento = raw_input("Introduce una casilla: ")
        conexion.enviarComando('Mover ' + movimiento)
        resultado = conexion.recibirResultado()
    conexion.enviarComando('BYE')

# Cadena de movimientos "ganadores" (para pruebas):
#     Mover A3
#     Mover B2
#     Mover C1
#     Mover A1
#     Mover C3
#     Mover B3
#     Mover C2


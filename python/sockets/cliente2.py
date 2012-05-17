#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cliente2.py

from socket import *
from time import time
from time import sleep
import sys

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
        print self.socket_cliente.recv(TAM_BUFFER)

if __name__ == '__main__':
    conexion = LineaComandos('localhost')
    conexion.abrirConexion()
    conexion.enviarComando('ls -al')
    conexion.recibirResultado()
    conexion.enviarComando('BYE')


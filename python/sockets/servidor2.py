#!/usr/bin/env python
# -*- coding: utf-8 -*-

# servidor2.py

from socket import *
import sys
import os

TAM_BUFFER = 4096
HOST = ''
PUERTO = 29876
DIRECCION = (HOST,PUERTO)

class ServidorComandos:
    def __init__(self):
        # Creamos el socket
        self.socket_servidor = socket(AF_INET,SOCK_STREAM)
        # Lo enlazamos al puerto elegido
        self.socket_servidor.bind((DIRECCION))
        self.linea_comandos = None
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
            while True:
                # Recibimos comandos
                comando = self.linea_comandos.recv(TAM_BUFFER)
                if comando:
                    # Procesamos el comando
                    print 'Procesando comando: %s' % comando
                    comando = comando.strip()
                    # Los clientes se desconectan enviando el comando 'BYE'
                    if comando == 'BYE':
                        break
                    else:
                        # Ejecutamos el comando (abriendo un nuevo proceso)
                        proceso = os.popen(comando)
                        salida = proceso.read()
                        if salida:
                            self.linea_comandos.send(salida)
                        else:
                            self.linea_comandos.send('OK')
            self.linea_comandos.close()
        self.socket_servidor.close()

if __name__ == '__main__':
    servidor = ServidorComandos()


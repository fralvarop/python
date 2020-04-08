#!/usr/bin/env python
# -*- coding: utf-8 -*-

# servidor1.py
import socket
soc = socket.socket()
hostname = socket.gethostname()
print 'Soy el host %s' % hostname
puerto = 21000
soc.bind((hostname,puerto))
soc.listen(5)
while True:
    conexion,direccion = soc.accept()
    print 'Estoy conectado a', direccion
    conexion.send('Hola y adiós')
    conexion.close()


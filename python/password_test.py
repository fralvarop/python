#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------
# password_test.py
#    ejemplo con if/else, listas, asignaciones, raw_input,
#    comentarios y evaluaciones
#------------------------------------------------------------
# Asignamos nombres de usuario y passwords
usuarios = ['Pepe','Juan','Paco','Manolo','Luis']
passwords = ['acceso','perro','12345','admin','qwerty']
#------------------------------------------------------------
# Pedimos nombre de usuario y password
usuario = raw_input('Introduzca su nombre de usuario: ')
pwd = raw_input('Introduzca su contraseña: ')
#------------------------------------------------------------
# Comprobamos que el usuario esté en la lista
if usuario in usuarios:
    posicion = usuarios.index(usuario) # Cogemos la posicion del usuario en la lista
    if pwd == passwords[posicion]:    # Encontramos la password de esa posicion
        print 'Hola, %s. Acceso permitido' % usuario
    else:
        print 'Acceso denegado'

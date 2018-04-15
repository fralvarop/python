#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Localiza todos los ficheros *.mp3 de un directorio dado
(y sus subdirectorios) y rellena las etiquetas USLT con
la letra de la canción del fichero homónimo *.txt.
@author: Raúl López
@organization: N/A
@license: GPL
@version: 1.0
@status: beta
@todo: Soporte UTF-8
B{Usage:} python addLyrics.py I{ruta}
B{Options:}
    - -h, --help       Muestra esta ayuda
"""

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT

import os

from os.path import join
from os.path import exists

import sys

import string

__docformat__ = "epytext"

def RecorrerLaRuta(rutamusica):
    """Recorre la ruta dada por el usuario en busca de canciones
    @param rutamusica: Ruta donde se encuentra la música
    @type rutamusica: str"""
    cont_errores = 0
    cont_directorios = 0
    cont_ficheros = 0
    # Abrimos el log de error
    log_error = open('errores.log',"w")
    for ruta, directorios, ficheros in os.walk(rutamusica):
        # Recorremos un directorio más
        cont_directorios += 1
        for fichero in [f for f in ficheros if f.endswith(".mp3")]:
            # Recorremos un MP3 más
            cont_ficheros += 1
            # Limpiamos la variable temporal
            _letra=''
            # Creamos una variable que contenga el fichero con la ruta completa
            fichero_con_ruta = join(ruta,fichero)
            try:
                etiqueta = ID3(fichero_con_ruta)
                # Leemos la letra del fichero correspondiente
                _letra = unicode(open(fichero_con_ruta.replace("mp3","txt"),"r").read(), "utf-8")
                # Creamos la etiqueta "USLT::spa"
                etiqueta.add(USLT(encoding=0, lang='spa', text=_letra))
                etiqueta.save(fichero_con_ruta)
            except Exception:
                cont_errores += 1
                log_error.writelines('ERROR - Fichero: %s\n' % fichero_con_ruta)
            print 'Procesando: %s' % fichero_con_ruta
        # Cerramos el log de errores
        log_error.close
    # Terminamos
    print '\n'
    print '%d directorios procesados' % cont_directorios
    print '%d ficheros procesados' % cont_ficheros
    print '%d errores encontrados' % cont_errores

def error(mensaje):
    """Muestra un mensaje de error por stderr
    @param mensaje: Mensaje a mostrar
    @type mensaje: str"""
    print >> sys.stderr, str(mensaje)

def main():
    """Función main de esta aplicación"""
    global conexion
    global cursor
    #----------------------------------------------
    if len(sys.argv) != 2:
        uso()
    else:
        # Manual de uso
        if sys.argv[1] in ("-h", "--help"):
            uso()
        # Manipular etiquetas
        else:
            DirectorioRaiz = sys.argv[1]
            # Función de os.path
            if not exists(DirectorioRaiz):
                print 'Parece que el directorio %s no existe... Saliendo.' % DirectorioRaiz
                sys.exit(1)
            else:
                print 'Vamos allá con %s:' % DirectorioRaiz
            # Hacemos el trabajo en sí...
            RecorrerLaRuta(DirectorioRaiz)
            # Avisamos al terminar...
            print '¡HECHO!'

def uso():
    """Muestra el modo de uso de esta aplicación"""
    mensaje = (
        '==============================================\n'
        'addLyrics - Localiza todos los ficheros *.mp3 de un directorio dado\n'
        '            (y sus subdirectorios) y rellena las etiquetas USLT con\n'
        '            la letra de la canción del fichero homónimo *.txt.\n\n'
        'Uso:\n'
        '       {0} <directorio>\n'
        '       donde <directorio> es la ruta hacia los ficheros MP3.\n\n'
        'Opciones:\n'
        '    -h, --help       Muestra esta ayuda\n\n'
        '==============================================\n'
        ).format(sys.argv[0])
    error(mensaje)
    sys.exit(1)

if __name__ == '__main__':
    main()

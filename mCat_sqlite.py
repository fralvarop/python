#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea una base de datos en SQLite a partir de la colección de música
ubicada en la ruta que el usuario especifique como argumento.

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
@todo: Soporte UTF-8

B{Usage:} python mCat_sqlite.py I{ruta}
"""

from mutagen.mp3 import MP3

import os

from os.path import join
from os.path import getsize
from os.path import exists

import sys

import apsw

__docformat__ = "epytext"

def CrearBaseDeDatos():
    """Crea la base de datos de canciones. Si la tabla ya existe, no hace nada"""
    sql = 'CREATE TABLE IF NOT EXISTS mp3 (pkID INTEGER PRIMARY KEY, titulo TEXT, artista TEXT, album TEXT, bitrate TEXT, '
    sql = sql + 'genero TEXT, duracion TEXT, pista INTEGER, ano TEXT, tamano TEXT, ruta TEXT, fichero TEXT);'
    cursor.execute(sql)

def SegundosAHorasMinutosSegundos(t):
    """Convierte tiempo en segundos a una cadena hh:mm:ss
    @param t: Tiempo en segundos
    @type t: float"""
    if t > 3600:
        h = int(t/3600)
        r = t-(h*3600)
        m = int(r / 60)
        s = int(r-(m*60))
        return '{0}:{1:02n}:{2:02n}'.format(h,m,s)
    else:
        m = int(t / 60)
        s = int(t-(m*60))
        return '{0}:{1:02n}'.format(m,s)

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
            # Limpiamos las variables temporales
            _titulo=''
            _artista=''
            _album=''
            _genero=''
            _ano=''
            _bitrate=''
            _duracion=''
            _tamano=''
            _pista=0
            # Combine path and filename to create a single variable.
            fichero_con_ruta = join(ruta,fichero)
            try:
                audio = MP3(fichero_con_ruta)
                claves = list(audio.keys())
                for clave in claves:
                    # Año
                    if clave == 'TDRC':
                        _ano = audio.get(clave)
                    # Álbum
                    elif clave == 'TALB':
                        _album = audio.get(clave)
                    # Pista
                    elif clave == 'TRCK':
                        _pst = audio.get(clave)
                        _pista = _pst[0]
                    # Artista
                    elif clave == "TPE1":
                        _artista = audio.get(clave)
                    # Título
                    elif clave == "TIT2":
                        _titulo = audio.get(clave)
                    # Género
                    elif clave == "TCON":
                        _genero = audio.get(clave)
                # Bitrate
                _bitrate = audio.info.bitrate
                # Duración
                _duracion = SegundosAHorasMinutosSegundos(audio.info.length)
                # Tamaño del fichero
                _tamano = getsize(fichero_con_ruta)
                # Escribimos en la base de datos
                sql = 'INSERT INTO mp3 (titulo, artista, album, genero, ano, pista, bitrate, duracion, tamano, ruta, fichero) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
                cursor.execute(sql, (str(_titulo), str(_artista), str(_album), str(_genero), str(_ano), int(_pista), str(_bitrate), str(_duracion), str(_tamano), ruta, fichero))
            except ValueError:
                cont_errores += 1
                log_error.writelines('===========================================\n')
                log_error.writelines('VALOR INCORRECTO - Fichero: %s\n' % fichero_con_ruta)
                log_error.writelines('Título: %s - Artista: %s - Álbum: %s\n' % (_titulo, _artista, _album))
                log_error.writelines('Género: %s - Año: %s - Pista: %s\n' % (_genero, _ano, str(_pista)))
                log_error.writelines('Bitrate: {0} - Duración: {1} \n'.format(_bitrate, _duracion))              
                log_error.writelines('===========================================\n')
            except TypeError:
                cont_errores += 1
                log_error.writelines('===========================================\n')
                log_error.writelines('TIPO INCORRECTO - Fichero: {0}\n'.format(fichero_con_ruta))
                log_error.writelines('Título: {0} - Artista: {1} - Álbum: {2}\n'.format(_titulo, _artista, _album))
                log_error.writelines('Género: {0} - Año: {1} - Pista: {2}\n'.format(_genero, _ano, _pista))
                log_error.writelines('Bitrate: {0} - Duración: {1} \n'.format(_bitrate, _duracion))
                log_error.writelines('===========================================\n')
            except:
                cont_errores += 1
                log_error.writelines('ERROR - Fichero: {0}\n'.format(fichero_con_ruta))
            print 'Procesando: %s - %s' % (str(_artista), str(_titulo))
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
        DirectorioRaiz = sys.argv[1]
        # Función de os.path
        if not exists(DirectorioRaiz):
            print 'Parece que el directorio %s no existe... Saliendo.' % DirectorioRaiz
            sys.exit(1)
        else:
            print 'Vamos allá con %s:' % DirectorioRaiz
        # Creamos la conexión con la base de datos y el cursor
        conexion=apsw.Connection("mCat.db3")
        cursor=conexion.cursor()
        # Creamos la base de datos si no existe...
        CrearBaseDeDatos()
        # Hacemos el trabajo en sí...
        RecorrerLaRuta(DirectorioRaiz)
        # Cerramos el cursor y la conexión...
        cursor.close()
        conexion.close()
        # Avisamos al terminar...
        print '¡HECHO!'

def uso():
    """Muestra el modo de uso de esta aplicación"""
    mensaje = (
        '==============================================\n'
        'mCat - Localiza todos los ficheros *.mp3 de un directorio\n'
        '       dado (y sus subdirectorios), lee las etiquetas ID3 y\n'
        '       escribe toda esa información en una base de datos SQLite.\n\n'
        'Uso:\n'
        '       {0} <directorio>\n'
        '       donde <directorio> es la ruta hacia los ficheros MP3.\n\n'
        'Autor: Greg Walters\n'
        'Para Full Circle Magazine\n'
        '==============================================\n'
        ).format(sys.argv[0])
    error(mensaje)
    sys.exit(1)

if __name__ == '__main__':
    main()

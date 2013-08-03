#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea una base de datos en PostgreSQL a partir de la colección de música
ubicada en la ruta que el usuario especifique como argumento.

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
@todo: Soporte UTF-8

B{Usage:} python mCat_pgsql.py I{ruta}

B{Options:}
    - -h, --help       Muestra esta ayuda
    - -b, --borrar     Borra la base de datos de música
Si se ejecuta sin opciones, se crea la base de
datos de música a partir del directorio indicado.
"""

from mutagen.mp3 import MP3

import os

from os.path import join
from os.path import getsize
from os.path import exists

import sys

import string

from pyPgSQL import PgSQL
from pyPgSQL import libpq

__docformat__ = "epytext"

database = "musica"

def crearBasedeDatos(db):
    """Crea en PostgreSQL la base de datos indicada por "db".
    @param db: Nombre de la base de datos
    @type db: str"""
    conexion = PgSQL.connect(database='template1')
    conexion.autocommit = 1
    cursor = conexion.cursor()
    try:
        cursor.execute("CREATE DATABASE %s ENCODING 'UTF8' TEMPLATE template1" % db)
    except libpq.OperationalError:
        print '¡Ya existe la base de datos "%s"!' % db
        sys.exit(1)
    print 'Creada base de datos "%s"' % db
    cursor.close()
    del cursor
    del conexion

def borrarBasedeDatos(db):
    """Borra de PostgreSQL la base de datos indicada por "db".
    @param db: Nombre de la base de datos
    @type db: str"""
    conexion = PgSQL.connect(database='template1')
    conexion.autocommit = 1
    cursor = conexion.cursor()
    try:
        cursor.execute("DROP DATABASE %s" % db)
    except libpq.OperationalError:
        print '¡No existe la base de datos "%s"!' % db
        sys.exit(1)
    print 'Borrada base de datos "%s"' % db
    cursor.close()
    del cursor
    del conexion

def crearTablas(db):
    """Crea en PostgreSQL las tablas de la base de datos indicada por "db".
    @param db: Nombre de la base de datos
    @type db: str"""
    conexion = PgSQL.connect(database=db)
    conexion.autocommit = 1
    cursor = conexion.cursor()

    sql = 'CREATE TABLE mp3 (titulo VARCHAR(255), artista VARCHAR(255), album VARCHAR(255), bitrate INT, frecuencia INT, genero VARCHAR(20),'
    sql = sql + ' duracion VARCHAR(8), pista SMALLINT, ano SMALLINT, tamano INT, ruta VARCHAR(255), fichero VARCHAR(255));'
    cursor.execute(sql)
    print 'Creada tabla "mp3"'

    cursor.close()
    del cursor
    del conexion

def SegundosAHorasMinutosSegundos(t):
    """Convierte tiempo en segundos a una cadena hh:mm:ss
    @param t: Tiempo en segundos
    @type t: float
    @return: Tiempo en formato hh:mm:ss"""
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
            _ano=0
            _bitrate=0
            _frecuencia=0
            _duracion=''
            _tamano=0
            _pista=0
            # Creamos una variable que contenga el fichero con la ruta completa
            fichero_con_ruta = join(ruta,fichero)
            try:
                audio = MP3(fichero_con_ruta)
                claves = list(audio.keys())
                for clave in claves:
                    # Año
                    if clave == 'TDRC':
                        _ano = int(str(audio.get(clave)).split("-")[0])
                    # Álbum
                    elif clave == 'TALB':
                        _album_1 = str(audio.get(clave))
                        _album = _album_1.replace("'","\\\'") # Escapamos los apóstrofos
                    # Pista
                    elif clave == 'TRCK':
                        _pst = audio.get(clave)
                        _pista = int(_pst[0].split()[0].split("/")[0]) # Prescindimos de lo que haya tras espacios o signos "/"
                    # Artista
                    elif clave == "TPE1":
                        _artista_1 = str(audio.get(clave))
                        _artista = _artista_1.replace("'","\\\'") # Escapamos los apóstrofos
                    # Título
                    elif clave == "TIT2":
                        _titulo_1 = str(audio.get(clave))
                        _titulo = _titulo_1.replace("'","\\\'") # Escapamos los apóstrofos
                    # Género
                    elif clave == "TCON":
                        _genero = audio.get(clave)
                # Bitrate
                _bitrate = audio.info.bitrate
                # Frecuencia de muestreo
                _frecuencia = audio.info.sample_rate
                # Duración
                _duracion = SegundosAHorasMinutosSegundos(audio.info.length)
                # Tamaño del fichero
                _tamano = getsize(fichero_con_ruta)
                # Ruta del fichero
                _ruta = ruta.replace("'","\\\'") # Escapamos los apóstrofos
                # Nombre del fichero
                _fichero = fichero.replace("'","\\\'") # Escapamos los apóstrofos
                # Escribimos en la base de datos
                sql = 'INSERT INTO mp3 (titulo, artista, album, genero, ano, pista, bitrate, frecuencia, duracion, tamano, ruta, fichero) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%d\',\'%d\',\'%d\',\'%d\',\'%s\',\'%d\',\'%s\',\'%s\')' % (_titulo, _artista, _album, _genero, _ano, _pista, _bitrate, _frecuencia, _duracion, _tamano, _ruta, _fichero)
                cursor.execute(sql)
            except ValueError:
                cont_errores += 1
                log_error.writelines('===========================================\n')
                log_error.writelines('VALOR INCORRECTO - Fichero: %s\n' % fichero_con_ruta)
                log_error.writelines('Título: %s - Artista: %s - Álbum: %s\n' % (_titulo_1, _artista_1, _album_1))
                log_error.writelines('Género: %s - Año: %d - Pista: %d\n' % (_genero, _ano, _pista))
                log_error.writelines('Bitrate: %d - Frecuencia: %d - Duración: %s\n' % (_bitrate, _frecuencia, _duracion))
                log_error.writelines('===========================================\n')
            except TypeError:
                cont_errores += 1
                log_error.writelines('===========================================\n')
                log_error.writelines('TIPO INCORRECTO - Fichero: %s\n' % fichero_con_ruta)
                log_error.writelines('Título: %s - Artista: %s - Álbum: %s\n' % (_titulo_1, _artista_1, _album_1))
                log_error.writelines('Género: %s - Año: %d - Pista: %d\n' % (_genero, _ano, _pista))
                log_error.writelines('Bitrate: %d - Frecuencia: %d - Duración: %s\n' % (_bitrate, _frecuencia, _duracion))
                log_error.writelines('===========================================\n')
            except:
                cont_errores += 1
                log_error.writelines('ERROR - Fichero: %s\n' % fichero_con_ruta)
            print 'Procesando: %s - %s' % (str(_artista_1), str(_titulo_1))
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
        # Borrar la base de datos
        elif sys.argv[1] in ("-b", "--borrar"):
            resp = raw_input('¿SEGURO que quieres borrar la base de datos de música por completo? (S/n) ')
            if string.upper(resp) == 'S':
                borrarBasedeDatos(database)
            else:
                print 'Operación cancelada'
        # Crear la base de datos
        else:
            DirectorioRaiz = sys.argv[1]
            # Función de os.path
            if not exists(DirectorioRaiz):
                print 'Parece que el directorio %s no existe... Saliendo.' % DirectorioRaiz
                sys.exit(1)
            else:
                print 'Vamos allá con %s:' % DirectorioRaiz
            # Creamos la base de datos si no existe...
            crearBasedeDatos(database)
            crearTablas(database)
            # Creamos la conexión con la base de datos y el cursor
            conexion = PgSQL.connect(database=database)
            conexion.autocommit = 1
            cursor = conexion.cursor()
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
        '       escribe toda esa información en una base de datos PostgreSQL.\n\n'
        'Uso:\n'
        '       {0} <directorio>\n'
        '       donde <directorio> es la ruta hacia los ficheros MP3.\n\n'
        'Opciones:\n'
        '    -h, --help       Muestra esta ayuda\n'
        '    -b, --borrar     Borra la base de datos de música\n'
        '    Si se ejecuta sin opciones, se crea la base de\n'
        '    datos de música a partir del directorio indicado.\n\n'
        '==============================================\n'
        ).format(sys.argv[0])
    error(mensaje)
    sys.exit(1)

if __name__ == '__main__':
    main()

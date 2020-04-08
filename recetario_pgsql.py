#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de gestión de una base de datos de recetas en PostgreSQL.
@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

import os
import sys
from pyPgSQL import PgSQL
from pyPgSQL import libpq
import string
import webbrowser

__docformat__ = "epytext"

database = "recetario"

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

    sql = "CREATE TABLE recetas (nombre VARCHAR(40) NOT NULL, raciones INT, autor VARCHAR(20), CONSTRAINT PK_nombre PRIMARY KEY (nombre))"
    cursor.execute(sql)
    print 'Creada tabla "recetas"'

    sql = "CREATE TABLE instrucciones (paso VARCHAR(60) NOT NULL, nombre_receta VARCHAR(40), CONSTRAINT PK_paso PRIMARY KEY (paso), CONSTRAINT FK_nombre_receta FOREIGN KEY (nombre_receta) REFERENCES recetas (nombre) ON DELETE CASCADE ON UPDATE CASCADE)"
    cursor.execute(sql)
    print 'Creada tabla "instrucciones"'

    sql = "CREATE TABLE ingredientes (ingrediente VARCHAR(30) NOT NULL, nombre_receta VARCHAR(40), CONSTRAINT PK_ingrediente PRIMARY KEY (ingrediente), CONSTRAINT FK_nombre_receta FOREIGN KEY (nombre_receta) REFERENCES recetas (nombre) ON DELETE CASCADE ON UPDATE CASCADE)"
    cursor.execute(sql)
    print 'Creada tabla "ingredientes"'

    cursor.close()
    del cursor
    del conexion

def rellenarTablas(db):
    """Rellena en PostgreSQL las tablas de la base de datos indicada por "db".
    @param db: Nombre de la base de datos
    @type db: str"""
    conexion = PgSQL.connect(database=db)
    conexion.autocommit = 1
    cursor = conexion.cursor()
    sql = "INSERT INTO recetas (nombre, raciones, autor) VALUES ('Paella',4,'Greg Walters')"
    cursor.execute(sql)

    instrucciones = ['1. Sofreír la carne picada', '2. Mezclar el resto de ingredientes', '3. Dejar que rompa a hervir', '4. Dejar cocer durante 20 minutos o hasta que pierda el agua']

    for paso in instrucciones:
        sql = "INSERT INTO instrucciones (nombre_receta, paso) VALUES ('Paella','%s')" % paso
        cursor.execute(sql)

    ingredientes = ['1 taza de arroz', 'carne picada', '2 vasos de agua', '1 lata de salsa de tomate', '1 cebolla picada', '1 ajo', '1 cucharadita de comino', '1 cucharadita de orégano', 'sal y pimienta al gusto', 'salsa al gusto']

    for ingrediente in ingredientes:
        sql = "INSERT INTO ingredientes (nombre_receta, ingrediente) VALUES ('Paella','%s')" % ingrediente
        cursor.execute(sql)

    print '"Paella" insertada en el recetario'

    cursor.close()

    del cursor
    del conexion

class Recetario:
    """Clase que implementa el comportamiendo de una base de datos de recetas."""

    def __init__(self, db):
        """Inicializador de la clase Recetario
        @param db: Nombre de la base de datos a utilizar
        @type db: str"""
        global conexion
        global cursor
        self.cantidadtotal = 0
        try:
            conexion = PgSQL.connect(database=db)
        except libpq.DatabaseError:
            print '¡No existe la base de datos "%s"!' % database
            print 'Has de crearla primero\n'
            uso()
        conexion.autocommit = 1
        cursor = conexion.cursor()

    def MostrarTodas(self):
        """Lista todas las recetas del recetario"""
        # Listamos todas las recetas del recetario con el siguiente formato:
        #
        # Número Nombre                         Raciones             Autor                         
        # --------------------------------------------------------------------------------
        #      1 Paella                         4                    Greg Walters                  
        # --------------------------------------------------------------------------------
        # Total de recetas: 1
        # --------------------------------------------------------------------------------
        if os.name == 'posix':
            os.system('clear')
        print '%s %s %s' % ('Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(25))
        print '-' * 75
        sql = 'SELECT * FROM recetas'
        contador = 0
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            contador += 1
            print '%s %s %s' % (tupla[0].ljust(30), str(tupla[1]).ljust(20), tupla[2].ljust(25))
        print '-' * 75
        self.cantidadtotal = contador

    def BuscarReceta(self):
        """Permite buscar una receta en el recetario por:
        - nombre de la receta
        - autor
        - ingredientes"""
        # Mostramos el menú de búsqueda
        if os.name == 'posix':
            os.system('clear')
        print '-------------------------------'
        print ' Búsqueda por'
        print '-------------------------------'
        print ' 1 - Nombre de la receta'
        print ' 2 - Autor'
        print ' 3 - Ingredientes'
        print ' 4 - Salir'
        buscarpor = raw_input('Buscar por: ')
        if buscarpor != '4':
            if buscarpor == '1':
                busqueda = 'receta'
            elif buscarpor == '2':
                busqueda = 'autor'
            elif buscarpor == '3':
                busqueda = 'ingrediente'
            else:
                print 'Comando no reconocido. Volviendo al menú.'
                tecla = raw_input('Pulsa intro para continuar')
                return

            respuesta = raw_input('¿Qué %s quieres buscar? (en blanco para salir) ' % busqueda)

            # Búsqueda por nombre de la receta
            if buscarpor == '1':
                sql = "SELECT nombre, raciones, autor FROM recetas WHERE UPPER(nombre) LIKE UPPER('%%%s%%')" % respuesta

            # Búsqueda por autor
            elif buscarpor == '2':
                sql = "SELECT nombre, raciones, autor FROM recetas WHERE UPPER(autor) LIKE UPPER('%%%s%%')" % respuesta

            # Búsqueda por ingrediente
            elif buscarpor == '3':
                sql = "SELECT r.nombre, r.raciones, r.autor, i.ingrediente FROM recetas r NATURAL INNER JOIN ingredientes i WHERE UPPER(r.nombre) = UPPER(i.nombre_receta) AND UPPER(i.ingrediente) LIKE UPPER('%%%s%%') GROUP BY r.nombre, r.raciones, r.autor, i.ingrediente" % respuesta

            try:
                if buscarpor == '3':
                    # Si hemos buscado por ingrediente, incluimos el ingrediente de referencia:
                    #
                    # Numero Nombre                         Raciones             Autor                          Ingrediente                   
                    # ------------------------------------------------------------------------------------------------------------------------
                    #      1 Paella                         4                    Greg Walters                   1 taza de arroz               
                    # ------------------------------------------------------------------------------------------------------------------------
                    print '%s %s %s %s' % ('Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(30), 'Ingrediente'.ljust(30))
                    print '-' * 120
                    cursor.execute(sql)
                    for tupla in cursor.fetchall():
                        print '%s %s %s %s' % (tupla[0].ljust(30), str(tupla[1]).ljust(20), tupla[2].ljust(30), tupla[3].ljust(30))
                    print '-' * 120
                else:
                    # Si no hemos buscado por ingrediente, basta con mostrar los siguientes campos:
                    #
                    # Numero Nombre                         Raciones             Autor                         
                    # --------------------------------------------------------------------------------
                    #      1 Paella                         4                    Greg Walters                  
                    # --------------------------------------------------------------------------------
                    print '%s %s %s' % ('Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(30))
                    print '-' * 80
                    cursor.execute(sql)
                    for tupla in cursor.fetchall():
                        print '%s %s %s' % (tupla[0].ljust(30), str(tupla[1]).ljust(20), tupla[2].ljust(30))
                    print '-' * 80
            except:
                print 'Ha ocurrido un problema'
            tecla = raw_input('Pulsa intro para continuar')

    def MostrarReceta(self, cual):
        """Muestra una receta completa, incluyendo autor, ingredientes y pasos a seguir
        @param cual: Nombre de la receta
        @type cual: str"""
        # Mostramos la receta completa con el siguiente formato:
        #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Nombre: Paella
        # Raciones: 4
        # Autor: Greg Walters
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Ingredientes:
        # 1 taza de arroz
        # carne picada
        # 2 vasos de agua
        # 1 lata de salsa de tomate
        # 1 cebolla picada
        # 1 ajo
        # 1 cucharadita de comino
        # 1 cucharadita de oregano
        # sal y pimienta al gusto
        # salsa al gusto
        #
        # Pasos:
        # 1. Sofreir la carne picada
        # 2. Mezclar el resto de ingredientes
        # 3. Dejar que rompa a hervir
        # 4. Dejar cocer durante 20 minutos o hasta que pierda el agua
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if os.name == 'posix':
            os.system('clear')
        sql = 'SELECT * FROM recetas WHERE UPPER(nombre) LIKE UPPER(\'%%%s%%\')' % cual
        print '~' * 40
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            print 'Nombre: %s' % tupla[0]
            print 'Raciones: %s' % tupla[1]
            print 'Autor: %s' % tupla[2]
        print '~' * 40
        sql = 'SELECT * FROM ingredientes WHERE UPPER(nombre_receta) LIKE UPPER(\'%%%s%%\')' % cual
        print 'Ingredientes:'
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            print tupla[0]
        print ''
        print 'Pasos:'
        sql = 'SELECT * FROM instrucciones WHERE UPPER(nombre_receta) LIKE UPPER(\'%%%s%%\')' % cual
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            print tupla[0]
        print '~' * 40
        tecla = raw_input('Pulsa intro para continuar')

    def BorrarReceta(self, cual):
        """Borra una receta concreta
        @param cual: Nombre de la receta
        @type cual: str"""
        resp = raw_input('¿SEGURO que quieres borrar esta receta? (S/n) ')
        if string.upper(resp) == 'S':
            sql = "DELETE FROM recetas WHERE UPPER(nombre) LIKE UPPER('%%%s%%')" % cual
            cursor.execute(sql)
            print 'Receta BORRADA'
        else:
            print 'Operación cancelada'
        tecla = raw_input('Pulsa intro para continuar')

    def NuevaReceta(self):
        """Permite introducir una nueva receta en la base de datos"""
        ingredientes = []
        nombre = ''
        autor = ''
        raciones = ''
        instrucciones = []
        id_receta = 0
        if os.name == 'posix':
            os.system('clear')

        # Introducimos el nombre de la receta
        respuesta = raw_input('Introduce el nombre la receta (en blanco para salir): ')
        if respuesta != '' :  # Continuamos
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                nombre = respuesta.replace("'","\'")
            else:
                nombre = respuesta

            # Introducimos el autor de la receta
            respuesta = raw_input('Introduce el autor de la receta: ')
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                autor = respuesta.replace("'","\'")
            else:
                autor = respuesta

            # Introducimos el número de raciones
            respuesta = raw_input('Introduce el número de raciones: ')
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                raciones = respuesta.replace("'","\'")
            else:
                raciones = respuesta

            # Introducimos la lista de ingredientes
            print 'Ahora vamos a introducir la lista de ingredientes.'
            while True:
                ingrediente = raw_input('Introduce ingrediente (en blanco para terminar): ')
                if ingrediente != '':
                    ingredientes.append(ingrediente)
                else:
                    break

            # Introducimos los pasos a seguir
            print 'Ahora vamos a introducir por orden los pasos a seguir para elaborar la receta.'
            contador_pasos = 0
            while True:
                paso = raw_input('Introduce el siguiente paso (en blanco para terminar): ')
                if paso != '':
                    contador_pasos += 1
                    instrucciones.append('%s. %s' % (str(contador_pasos), paso))
                else:
                    break

            # Pedimos confirmación mostrando los datos que tenemos
            print '~' * 40
            print 'Esto es lo que tenemos'
            print 'Nombre: %s' % nombre
            print 'Autor: %s' % autor
            print 'Raciones: %s' % raciones
            print 'Ingredientes:'
            for ingrediente in ingredientes:
                print ingrediente
            print 'Pasos:'
            for paso in instrucciones:
                print paso
            print '~' * 40
            respuesta = raw_input("¿Guardar así? (S/n) ")
            if string.upper(respuesta) != 'N':
                # Insertamos la receta en la tabla "recetas"
                sql = 'INSERT INTO recetas (nombre, raciones, autor) VALUES (\'%s\',\'%s\',\'%s\')' %(nombre, raciones, autor)
                cursor.execute(sql)
                # Insertamos todos los ingredientes de la receta en la tabla "ingredientes"
                for ingrediente in ingredientes:
                    sql = 'INSERT INTO ingredientes (nombre_receta, ingrediente) VALUES (\'%s\',\'%s\')' % (nombre, ingrediente)
                    cursor.execute(sql)
                # Insertamos la receta en la tabla "instrucciones"
                for paso in instrucciones:
                    sql = 'INSERT INTO instrucciones (nombre_receta, paso) VALUES(\'%s\',\'%s\')' %(nombre, paso)
                    cursor.execute(sql)
                # Informamos al usuario de que hemos terminado
                print 'Hecho'
            else:
                print 'Operación cancelada'
            tecla = raw_input('Pulsa intro para continuar')

    def ImprimirReceta(self, cual):
        """Vuelca la receta a un fichero HTML con formato
        para poder imprimirla desde el navegador
        @param cual: Nombre de la receta
        @type cual: str"""
        fi = open('impresion.html','w')
        fi.write("<html>")
        fi.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">")
        sql = "SELECT * FROM recetas WHERE UPPER(nombre) LIKE UPPER('%%%s%%')" % cual
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            nombre = tupla[0]
            raciones = tupla[1]
            autor = tupla[2]
        fi.write("<head><title>%s</title></head><body>" % nombre)
        fi.write("<H1>%s</H1>" % nombre)
        fi.write("<H2>Raciones: %s</H2>" % raciones)
        fi.write("<H2>Autor: %s</H2>" % autor)
        fi.write("<H3>Ingredientes:</H3>")
        sql = 'SELECT * FROM ingredientes WHERE UPPER(nombre_receta) LIKE UPPER(\'%%%s%%\')' % cual
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            fi.write("<li>%s</li>" % tupla[0])
        fi.write("<H3>Pasos:</H3>")
        sql = 'SELECT * FROM instrucciones WHERE UPPER(nombre_receta) LIKE UPPER(\'%%%s%%\')' % cual
        cursor.execute(sql)
        for tupla in cursor.fetchall():
            fi.write("%s<br>" % tupla[0])
        fi.write("</body></html>")
        fi.close()
        webbrowser.open('impresion.html')
        print 'Hecho'

def main():
    """Función main de esta aplicación"""
    rct = Recetario(database) # Inicializamos la clase "recetario"
    while True:
        if os.name == 'posix':
            os.system('clear')
        print '==================================================='
        print '             BASE DE DATOS DE RECETAS'
        print '==================================================='
        print ' 1 - Ver todas las recetas'
        print ' 2 - Buscar una receta'
        print ' 3 - Ver una receta'
        print ' 4 - Borrar una receta'
        print ' 5 - Añadir una receta'
        print ' 6 - Imprimir una receta'
        print ' 0 - Salir'
        print '==================================================='
        respuesta = raw_input('Elige una opción: ')

        # Ver todas las recetas
        if respuesta == '1':
            rct.MostrarTodas()
            print 'Total de recetas: %s' % rct.cantidadtotal
            print '-' * 75
            res = raw_input('Pulsa intro para continuar')

        # Buscar una receta
        elif respuesta == '2':
            rct.BuscarReceta()

        # Ver una receta
        elif respuesta == '3':
            rct.MostrarTodas()
            res = raw_input('¿Cuál quieres ver? ')
            rct.MostrarReceta(res)

        # Borrar una receta
        elif respuesta == '4':
            rct.MostrarTodas()
            res = raw_input('Elige una receta para borrar (0 para cancelar): ')
            if res != '0':
                rct.BorrarReceta(res)
            elif res == '0':
                print 'Volviendo al menú...'
            else:
                print 'Comando no reconocido. Volviendo al menú.'

        # Añadir una receta
        elif respuesta == '5':
            rct.NuevaReceta()

        # Imprimir una receta
        elif respuesta == '6':
            rct.MostrarTodas()
            res = raw_input('Elige una receta para imprimir (0 para salir): ')
            if res != '0':
                rct.ImprimirReceta(res)
            elif res == '0':
                print 'Volviendo al menú...'
            else:
                print 'Comando no reconocido. Volviendo al menú.'

        # Salir del programa
        elif respuesta == '0':
            print 'Adiós'
            break

        else:
            print 'Opción no válida'

def uso():
    """Muestra el modo de uso de esta aplicación"""
    mensaje = (
        '==========================================================\n\n'
        'recetario - Permite gestionar una base de datos de recetas\n\n'
        'Opciones:\n'
        '    -h, --help       Muestra esta ayuda\n'
        '    -c, --crear      Crea la base de datos\n'
        '    -b, --borrar     Borra la base de datos\n'
        '    -g, --gestionar  Permite gestionar el recetario\n\n'
        '    Si se ejecuta sin argumentos, se lanza\n'
        '    la gestión (opción -g) por defecto.\n\n'
        '=========================================================='
        ).format(sys.argv[0])
    print >> sys.stderr, str(mensaje)
    sys.exit(1)

if __name__ == '__main__':

    # Sin argumentos, lanzamos la gestión del recetario
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:

        # Manual de uso
        if sys.argv[1] in ("-h", "--help"):
            uso()

        # Crear la base de datos
        elif sys.argv[1] in ("-c", "--crear"):
            crearBasedeDatos(database)
            crearTablas(database)
            rellenarTablas(database)

        # Borrar la base de datos
        elif sys.argv[1] in ("-b", "--borrar"):
            resp = raw_input('¿SEGURO que quieres borrar el recetario por completo? (S/n) ')
            if string.upper(resp) == 'S':
                borrarBasedeDatos(database)
            else:
                print 'Operación cancelada'

        # Lanzar la gestión del recetario
        elif sys.argv[1] in ("-g", "--gestionar"):
            main()

        else:
            print 'Opción no válida'
            uso()

    else:
        print 'Parámetros incorrectos'
        uso()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de gestión de una base de datos de recetas en SQLite.
@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

import os
import apsw
import string
import webbrowser

__docformat__ = "epytext"

class Recetario:
    """Clase que implementa el comportamiendo de una base de datos de recetas."""

    def __init__(self):
        """Inicializador de la clase Recetario"""
        global conexion
        global cursor
        self.cantidadtotal = 0
        conexion = apsw.Connection("recetario.db3")
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
        print '%s %s %s %s' % ('Número'.ljust(6), 'Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(25))
        print '-' * 75
        sql = 'SELECT * FROM recetas'
        contador = 0
        for tupla in cursor.execute(sql):
            contador += 1
            print '%s %s %s %s' % (str(tupla[0]).rjust(6), tupla[1].ljust(30), tupla[2].ljust(20), tupla[3].ljust(25))
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
                sql = "SELECT pkID, nombre, raciones, autor FROM recetas WHERE nombre like '%%%s%%'" % respuesta

            # Búsqueda por autor
            elif buscarpor == '2':
                sql = "SELECT pkID, nombre, raciones, autor FROM recetas WHERE autor like '%%%s%%'" % respuesta

            # Búsqueda por ingrediente
            elif buscarpor == '3':
                sql = "SELECT r.pkID, r.nombre, r.raciones, r.autor, i.ingrediente FROM recetas r Left Join ingredientes i on (r.pkID = i.id_receta) WHERE i.ingrediente like '%%%s%%' GROUP BY r.pkID" % respuesta

            try:
                if buscarpor == '3':
                    # Si hemos buscado por ingrediente, incluimos el ingrediente de referencia:
                    #
                    # Numero Nombre                         Raciones             Autor                          Ingrediente                   
                    # ------------------------------------------------------------------------------------------------------------------------
                    #      1 Paella                         4                    Greg Walters                   1 taza de arroz               
                    # ------------------------------------------------------------------------------------------------------------------------
                    print '%s %s %s %s %s' % ('Número'.ljust(6), 'Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(30), 'Ingrediente'.ljust(30))
                    print '-' * 120
                    for tupla in cursor.execute(sql):
                        print '%s %s %s %s %s' % (str(tupla[0]).rjust(6), tupla[1].ljust(30), tupla[2].ljust(20), tupla[3].ljust(30), tupla[4].ljust(30))
                    print '-' * 120
                else:
                    # Si no hemos buscado por ingrediente, basta con mostrar los siguientes campos:
                    #
                    # Numero Nombre                         Raciones             Autor                         
                    # --------------------------------------------------------------------------------
                    #      1 Paella                         4                    Greg Walters                  
                    # --------------------------------------------------------------------------------
                    print '%s %s %s %s' % ('Número'.ljust(6), 'Nombre'.ljust(30), 'Raciones'.ljust(20), 'Autor'.ljust(30))
                    print '-' * 80
                    for tupla in cursor.execute(sql):
                        print '%s %s %s %s' % (str(tupla[0]).rjust(6), tupla[1].ljust(30), tupla[2].ljust(20), tupla[3].ljust(30))
                    print '-' * 80
            except:
                print 'Ha ocurrido un problema'
            tecla = raw_input('Pulsa intro para continuar')

    def MostrarReceta(self, cual):
        """Muestra una receta completa, incluyendo autor, ingredientes y pasos a seguir
        @param cual: Identificador de la receta
        @type cual: int"""
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
        sql = 'SELECT * FROM recetas WHERE pkID = %s' % str(cual)
        print '~' * 40
        for tupla in cursor.execute(sql):
            id_receta = tupla[0]
            print 'Nombre: %s' % tupla[1]
            print 'Raciones: %s' % tupla[2]
            print 'Autor: %s' % tupla[3]
        print '~' * 40
        sql = 'SELECT * FROM ingredientes WHERE id_receta = %s' % id_receta
        print 'Ingredientes:'
        for tupla in cursor.execute(sql):
            print tupla[1]
        print ''
        print 'Pasos:'
        sql = 'SELECT * FROM instrucciones WHERE id_receta = %s' % id_receta
        for tupla in cursor.execute(sql):
            print tupla[1]
        print '~' * 40
        tecla = raw_input('Pulsa intro para continuar')

    def BorrarReceta(self, cual):
        """Borra una receta concreta
        @param cual: Identificador de la receta
        @type cual: int"""
        resp = raw_input('¿SEGURO que quieres borrar esta receta? (S/n) ')
        if string.upper(resp) == 'S':
            sql = "DELETE FROM recetas WHERE pkID = %s" % str(cual)
            cursor.execute(sql)
            sql = "DELETE FROM instrucciones WHERE id_receta = %s" % str(cual)
            cursor.execute(sql)
            sql = "DELETE FROM ingredientes WHERE id_receta = %s" % str(cual)
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
                sql = 'INSERT INTO recetas (nombre, raciones, autor) VALUES ("%s","%s","%s")' %(nombre, raciones, autor)
                cursor.execute(sql)
                # Guardamos el pkID de la nueva receta
                sql = "SELECT last_insert_rowid()"
                cursor.execute(sql)
                for x in cursor.execute(sql):
                    id_receta = x[0]
                # Insertamos todos los ingredientes de la receta en la tabla "ingredientes"
                for ingrediente in ingredientes:
                    sql = 'INSERT INTO ingredientes (id_receta, ingrediente) VALUES (%s,"%s")' % (id_receta, ingrediente)
                    cursor.execute(sql)
                # Insertamos la receta en la tabla "instrucciones"
                for paso in instrucciones:
                    sql = 'INSERT INTO instrucciones (id_receta, paso) VALUES( %s,"%s")' %(id_receta, paso)
                    cursor.execute(sql)
                # Informamos al usuario de que hemos terminado
                print 'Hecho'
            else:
                print 'Operación cancelada'
            tecla = raw_input('Pulsa intro para continuar')

    def ImprimirReceta(self, cual):
        """Vuelca la receta a un fichero HTML con formato
        para poder imprimirla desde el navegador
        @param cual: Identificador de la receta
        @type cual: int"""
        fi = open('impresion.html','w')
        sql = "SELECT * FROM recetas WHERE pkID = %s" % cual
        for tupla in cursor.execute(sql):
            nombre = tupla[1]
            raciones = tupla[2]
            autor = tupla[3]
        fi.write("<H1>%s</H1>" % nombre)
        fi.write("<H2>Raciones: %s</H2>" % raciones)
        fi.write("<H2>Autor: %s</H2>" % autor)
        fi.write("<H3>Ingredientes:</H3>")
        sql = 'SELECT * FROM ingredientes WHERE id_receta = %s' % cual
        for tupla in cursor.execute(sql):
            fi.write("<li>%s</li>" % tupla[1])
        fi.write("<H3>Pasos:</H3>")
        sql = 'SELECT * FROM instrucciones WHERE id_receta = %s' % cual
        for tupla in cursor.execute(sql):
            fi.write("%s<br>" % tupla[1])
        fi.close()
        webbrowser.open('impresion.html')
        print 'Hecho'

def main():
    """Función main de esta aplicación"""
    rct = Recetario() # Inicializamos la clase "recetario"
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
            try:
                res = int(raw_input('¿Cuál quieres ver? '))
                if res <= rct.cantidadtotal:
                    rct.MostrarReceta(res)
                elif res == rct.cantidadtotal + 1:
                    print 'Volviendo al menú...'
                else:
                    print 'Comando no reconocido. Volviendo al menú.'
            except ValueError:
                print 'No has introducido un número... volviendo al menú.'

        # Borrar una receta
        elif respuesta == '4':
            rct.MostrarTodas()
            try:
                res = int(raw_input('Elige una receta para borrar (0 para salir): '))
                if res != 0:
                    rct.BorrarReceta(res)
                elif res == '0':
                    print 'Volviendo al menú...'
                else:
                    print 'Comando no reconocido. Volviendo al menú.'
            except ValueError:
                print 'No has introducido un número... volviendo al menú.'

        # Añadir una receta
        elif respuesta == '5':
            rct.NuevaReceta()

        # Imprimir una receta
        elif respuesta == '6':
            rct.MostrarTodas()
            try:
                res = int(raw_input('Elige una receta para imprimir (0 para salir): '))
                if res != 0:
                    rct.ImprimirReceta(res)
                elif res == '0':
                    print 'Volviendo al menú...'
                else:
                    print 'Comando no reconocido. Volviendo al menú.'
            except ValueError:
                print 'No has introducido un número... volviendo al menú.'

        # Salir del programa
        elif respuesta == '0':
            print 'Adiós'
            break

        else:
            print 'Opción no válida'

if __name__ == '__main__':
    main()


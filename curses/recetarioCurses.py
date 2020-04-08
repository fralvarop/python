#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de gestión de una base de datos de recetas en SQLite.\n
Versión libcurses
@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta
"""

import curses
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
        pantalla.erase()
        pantalla.border(0)
        pantalla.addstr(1,1, "==================================================")
        pantalla.addstr(2,1, "             Mostrar todas las recetas")
        pantalla.addstr(3,1, "==================================================")
        pantalla.addstr(4,1, "Numero Nombre                         Raciones             Autor")
        pantalla.addstr(5,1, "-"*78)
        sql = 'SELECT * FROM recetas'
        contador = 0
        for tupla in cursor.execute(sql):
            contador += 1
            pantalla.addstr(5+contador,1, str(tupla[0]).rjust(6))
            pantalla.addstr(5+contador,8, tupla[1])
            pantalla.addstr(5+contador,39, tupla[2])
            pantalla.addstr(5+contador,60, tupla[3])
        pantalla.addstr(6+contador,1, "-"*78)
        self.cantidadtotal = contador
        pantalla.addstr(7+contador,1, "Total de recetas: " + str(self.cantidadtotal))
        pantalla.addstr(8+contador,1, "-"*78)
        pantalla.addstr(9+contador,1, "Pulsa una tecla para continuar")
        pantalla.refresh()
        pantalla.getch()

    def BuscarReceta(self):
        """Permite buscar una receta en el recetario por:
        - nombre de la receta
        - autor
        - ingredientes"""
        pantalla.erase()    
        pantalla.border(0)
        pantalla.addstr(1,1, "==================================================")
        pantalla.addstr(2,1, "                Busqueda de recetas")
        pantalla.addstr(3,1, "==================================================")
        pantalla.addstr(4,1, "-------------------------------")
        pantalla.addstr(5,1, " Busqueda por")
        pantalla.addstr(6,1, "-------------------------------")
        pantalla.addstr(7,1, " 1 - Nombre de la receta")
        pantalla.addstr(8,1, " 2 - Autor")
        pantalla.addstr(9,1, " 3 - Ingredientes")
        pantalla.addstr(10,1," 0 - Salir")
        pantalla.addstr(11,1,"Buscar por: ")
        pantalla.refresh()

        while True:
            tecla = pantalla.getch(11,13)
            pantalla.addch(11,13,tecla)
            if tecla == ord('1'):
                cadena_busqueda = CapturarCadena(13,1,"¿Qué receta quieres buscar? ")
                sql = "SELECT pkID, nombre, raciones, autor FROM recetas WHERE nombre like '%%%s%%'" % cadena_busqueda
                break
            elif tecla == ord('2'):
                cadena_busqueda = CapturarCadena(13,1,"¿Qué autor quieres buscar? ")
                sql = "SELECT pkID, nombre, raciones, autor FROM recetas WHERE autor like '%%%s%%'" % cadena_busqueda
                break
            elif tecla == ord('3'):
                cadena_busqueda = CapturarCadena(13,1,"¿Qué ingrediente quieres buscar? ")
                sql = "SELECT r.pkID, r.nombre, r.raciones, r.autor, i.ingrediente FROM recetas r Left Join ingredientes i on (r.pkID = i.id_receta) WHERE i.ingrediente like '%%%s%%' GROUP BY r.pkID" % cadena_busqueda
                break
            else:
                cadena_busqueda = ""
                break

        try:
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(1,1, "==================================================")
            pantalla.addstr(2,1, "                Busqueda de recetas")
            pantalla.addstr(3,1, "==================================================")
            if tecla == ord('3'):
                # Si hemos buscado por ingrediente, incluimos el ingrediente de referencia:
                #
                # Numero Nombre                         Raciones             Autor                          Ingrediente                   
                # ------------------------------------------------------------------------------------------------------------------------
                #      1 Paella                         4                    Greg Walters                   1 taza de arroz               
                # ------------------------------------------------------------------------------------------------------------------------
                pantalla.addstr(4,1,"Numero Nombre                    Raciones   Autor          Ingrediente")
                pantalla.addstr(5,1, "-"*78)
                contador = 0
                for tupla in cursor.execute(sql):
                    contador += 1
                    pantalla.addstr(5+contador,1, str(tupla[0]).rjust(6))
                    pantalla.addstr(5+contador,8, tupla[1])
                    pantalla.addstr(5+contador,34, tupla[2])
                    pantalla.addstr(5+contador,45, tupla[3])
                    pantalla.addstr(5+contador,60, tupla[4])
            else:
                # Si no hemos buscado por ingrediente, basta con mostrar los siguientes campos:
                #
                # Numero Nombre                         Raciones             Autor                         
                # --------------------------------------------------------------------------------
                #      1 Paella                         4                    Greg Walters                  
                # --------------------------------------------------------------------------------
                pantalla.addstr(4,1, "Numero Nombre                         Raciones             Autor")
                pantalla.addstr(5,1, "-"*78)
                contador = 0
                for tupla in cursor.execute(sql):
                    contador += 1
                    pantalla.addstr(5+contador,1, str(tupla[0]).rjust(6))
                    pantalla.addstr(5+contador,8, tupla[1])
                    pantalla.addstr(5+contador,39, tupla[2])
                    pantalla.addstr(5+contador,60, tupla[3])
            pantalla.addstr(6+contador,1, "-"*78)
            pantalla.addstr(7+contador,1, "Pulsa una tecla para continuar")
            pantalla.refresh()
            pantalla.getch()
        except:
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(1,1, "==================================================")
            pantalla.addstr(2,1, "                Busqueda de recetas")
            pantalla.addstr(3,1, "==================================================")
            pantalla.addstr(5,1, "Ha habido un problema con la base de datos")
            pantalla.addstr(7,1, "Pulsa una tecla para continuar")
            pantalla.refresh()
            pantalla.getch()

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
        try:
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(1,1, "~"*40)
            sql = 'SELECT * FROM recetas WHERE pkID = %s' % str(cual)
            for tupla in cursor.execute(sql):
                id_receta = tupla[0]
                pantalla.addstr(2,1, "Nombre: " + tupla[1])
                pantalla.addstr(3,1, "Raciones: " + tupla[2])
                pantalla.addstr(4,1, "Autor: " + tupla[3])
            pantalla.addstr(5,1, "~"*40)

            sql = 'SELECT * FROM ingredientes WHERE id_receta = %s' % id_receta
            pantalla.addstr(6,1, "Ingredientes:")
            contador = 0
            for tupla in cursor.execute(sql):
                contador += 1
                pantalla.addstr(6+contador,1, "\t" + tupla[1])

            sql = 'SELECT * FROM instrucciones WHERE id_receta = %s' % id_receta
            pantalla.addstr(8+contador,1, "Pasos:")
            for tupla in cursor.execute(sql):
                contador += 1
                pantalla.addstr(8+contador,1, "\t" + tupla[1])
            pantalla.addstr(9+contador,1, "~"*40)
            pantalla.addstr(10+contador,1, "Pulsa una tecla para continuar")
            pantalla.refresh()
            pantalla.getch()
        except:
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(5,5,"Imposible mostrar la receta, es necesaria una terminal mas grande")
            pantalla.refresh()
            pantalla.getch()

    def BorrarReceta(self, cual):
        """Borra una receta concreta
        @param cual: Identificador de la receta
        @type cual: int"""
        pantalla.erase()
        pantalla.border(0)
        pantalla.addstr(1,1, "==================================================")
        pantalla.addstr(2,1, "                  Borrar receta")
        pantalla.addstr(3,1, "==================================================")
        pantalla.refresh()
        confirmacion = CapturarCadena(5, 1, "Confirma que quieres borrar esta receta (S/n) ")
        if string.upper(confirmacion) == 'S':
            sql = "DELETE FROM recetas WHERE pkID = %s" % str(cual)
            cursor.execute(sql)
            sql = "DELETE FROM instrucciones WHERE id_receta = %s" % str(cual)
            cursor.execute(sql)
            sql = "DELETE FROM ingredientes WHERE id_receta = %s" % str(cual)
            cursor.execute(sql)
            pantalla.addstr(7,10, "Receta borrada")
        else:
            pantalla.addstr(7,10, "Operacion cancelada")
        pantalla.addstr(9,1, "Pulsa una tecla para continuar")
        pantalla.refresh()
        pantalla.getch()

    def NuevaReceta(self):
        """Permite introducir una nueva receta en la base de datos"""
        ingredientes = []
        nombre = ''
        autor = ''
        raciones = ''
        instrucciones = []
        id_receta = 0

        pantalla.erase()
        pantalla.border(0)
        pantalla.addstr(1,1, "==================================================")
        pantalla.addstr(2,1, "                   Nueva receta")
        pantalla.addstr(3,1, "==================================================")
        pantalla.refresh()

        # Introducimos el nombre de la receta
        respuesta = CapturarCadena(5, 1, "Introduce el nombre de la receta: ")
        if respuesta != '' :  # Continuamos
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                nombre = respuesta.replace("'","\'")
            else:
                nombre = respuesta

            # Introducimos el autor de la receta
            respuesta = CapturarCadena(6, 1, "Introduce el autor de la receta: ")
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                autor = respuesta.replace("'","\'")
            else:
                autor = respuesta

            # Introducimos el número de raciones
            respuesta = CapturarCadena(7, 1, "Introduce el numero de raciones: ")
            if string.find(respuesta,"'"): # Escapamos los apóstrofos
                raciones = respuesta.replace("'","\'")
            else:
                raciones = respuesta

            # Introducimos la lista de ingredientes
            pantalla.addstr(8,1, "Ahora vamos a introducir la lista de ingredientes.")
            contador = 0
            while True:
                contador += 1
                ingrediente = CapturarCadena(8+contador,1, "Introduce ingrediente (en blanco para terminar): ")
                if ingrediente != '':
                    ingredientes.append(ingrediente)
                else:
                    break

            # Introducimos los pasos a seguir
            pantalla.addstr(9+contador,1, "Ahora vamos a introducir por orden los pasos a seguir para elaborar la receta.")
            contador_pasos = 0
            while True:
                paso = CapturarCadena(10+contador,1, "Introduce el siguiente paso (en blanco para terminar): ")
                if paso != '':
                    contador += 1
                    contador_pasos += 1
                    instrucciones.append('%s. %s' % (str(contador_pasos), paso))
                else:
                    break

            # Pedimos confirmación mostrando los datos que tenemos
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(1,1, "Esto es lo que tenemos:")
            pantalla.addstr(2,1, "~"*40)
            pantalla.addstr(3,1, "Nombre: " + nombre)
            pantalla.addstr(4,1, "Autor: " + autor)
            pantalla.addstr(5,1, "Raciones: " + raciones)
            pantalla.addstr(6,1, "Ingredientes:")
            contador = 0
            for ingrediente in ingredientes:
                contador += 1
                pantalla.addstr(6+contador,1, ingrediente)
            pantalla.addstr(7+contador,1, "Pasos:")
            for paso in instrucciones:
                contador += 1
                pantalla.addstr(7+contador,1, paso)
            pantalla.addstr(8+contador,1, "~"*40)

            confirmacion = CapturarCadena(9+contador, 1, "Confirma que quieres guardar esta receta (S/n) ")
            if string.upper(confirmacion) != 'N':
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
                pantalla.addstr(10+contador,10, "Receta guardada")
            else:
                pantalla.addstr(10+contador,10, "Operacion cancelada")
            pantalla.addstr(11+contador,1, "Pulsa una tecla para continuar")
            pantalla.refresh()
            pantalla.getch()

    def ImprimirReceta(self, cual):
        """Vuelca la receta a un fichero HTML con formato
        para poder imprimirla desde el navegador
        @param cual: Identificador de la receta
        @type cual: int"""
        # Escribimos la receta en un fichero HTML y lo abrimos con el navegador
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

def CapturarCadena(fila, columna, cadena):
    """Permite capturar una cadena de texto mediante libcurses
    @param fila: Fila donde se encuentra el cursor
    @type fila: int
    @param columna: Columna donde se encuentra el cursor
    @type columna: int
    @param cadena: Cadena capturada
    @type cadena: str"""
    pantalla.addstr(fila, columna, cadena)
    pantalla.refresh()
    cadena_completa = pantalla.getstr(fila,len(cadena)+1)
    pantalla.addstr(fila,len(cadena)+1,cadena_completa)
    pantalla.refresh()
    return cadena_completa

#===========================================================
# Función main
#===========================================================
if __name__ == "__main__":

    #  Bucle principal
    try:
        pantalla = curses.initscr()
        rct = Recetario() # Inicializamos la clase "recetario"
        tecla = 'X'
        while tecla != ord('0'):
            pantalla.erase()
            pantalla.border(0)
            pantalla.addstr(1,1,  "===================================================")
            pantalla.addstr(2,1,  "             BASE DE DATOS DE RECETAS")
            pantalla.addstr(3,1,  "===================================================")
            pantalla.addstr(4,1,  "  1 - Ver todas las recetas")
            pantalla.addstr(5,1,  "  2 - Buscar una receta")
            pantalla.addstr(6,1,  "  3 - Ver una receta")
            pantalla.addstr(7,1,  "  4 - Borrar una receta")
            pantalla.addstr(8,1,  "  5 - Introducir una nueva receta")
            pantalla.addstr(9,1,  "  6 - Imprimir una receta")
            pantalla.addstr(10,1, "  0 - Salir")
            pantalla.addstr(11,1, "===================================================")
            pantalla.addstr(12,1, "  Elige una opción: ")
            pantalla.refresh()
            tecla = pantalla.getch(12,21)
            pantalla.addch(12,21,tecla)

            # Ver todas las recetas
            if tecla == ord('1'):
                rct.MostrarTodas()

            # Buscar una receta
            elif tecla == ord('2'):
                rct.BuscarReceta()

            # Ver una receta
            elif tecla == ord('3'):
                rct.MostrarTodas()
                pantalla.erase()
                pantalla.border(0)
                pantalla.addstr(1,1, "==================================================")
                pantalla.addstr(2,1, "                  Mostrar receta")
                pantalla.addstr(3,1, "==================================================")
                pantalla.refresh()
                id_receta = CapturarCadena(5, 1, "Introduce el numero de la receta que quieres mostrar: ")
                rct.MostrarReceta(id_receta)

            # Borrar una receta
            elif tecla == ord('4'):
                rct.MostrarTodas()
                pantalla.erase()
                pantalla.border(0)
                pantalla.addstr(1,1, "==================================================")
                pantalla.addstr(2,1, "                  Borrar receta")
                pantalla.addstr(3,1, "==================================================")
                pantalla.refresh()
                id_receta = CapturarCadena(5, 1, "Introduce el numero de la receta que quieres borrar: ")
                rct.BorrarReceta(id_receta)

            # Añadir una receta
            elif tecla == ord('5'):
                rct.NuevaReceta()

            # Imprimir una receta
            elif tecla == ord('6'):
                rct.MostrarTodas()
                pantalla.erase()
                pantalla.border(0)
                pantalla.addstr(1,1, "==================================================")
                pantalla.addstr(2,1, "                 Imprimir receta")
                pantalla.addstr(3,1, "==================================================")
                pantalla.refresh()
                id_receta = CapturarCadena(5, 1, "Introduce el numero de la receta que quieres imprimir: ")
                rct.ImprimirReceta(id_receta)
    finally:
        curses.endwin()


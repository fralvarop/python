#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos APSW (Another Python SQLite Wrapper)
import apsw

# Abrimos/creamos la base de datos

conexion = apsw.Connection("recetario.db3")
cursor = conexion.cursor()

sql = 'CREATE TABLE recetas (pkID INTEGER PRIMARY KEY, nombre TEXT, raciones TEXT, autor TEXT)'
cursor.execute(sql)

sql = 'CREATE TABLE instrucciones (pkID INTEGER PRIMARY KEY, paso TEXT, id_receta NUMERIC)'
cursor.execute(sql)

sql = 'CREATE TABLE ingredientes (pkID INTEGER PRIMARY KEY, ingrediente TEXT, id_receta NUMERIC)'
cursor.execute(sql)

sql = 'INSERT INTO recetas (nombre, raciones, autor) VALUES ("Paella",4,"Greg Walters")'
cursor.execute(sql)

sql = 'SELECT last_insert_rowid()'

for x in cursor.execute(sql):
    ultimoid = x[0]

instrucciones = ["1. Sofreir la carne picada",
                 "2. Mezclar el resto de ingredientes",
                 "3. Dejar que rompa a hervir",
                 "4. Dejar cocer durante 20 minutos o hasta que pierda el agua"]

for paso in instrucciones:
    sql = 'INSERT INTO instrucciones (id_receta, paso) VALUES (%s,"%s")' % (ultimoid, paso)
    cursor.execute(sql)

ingredientes = ["1 taza de arroz",
                "carne picada",
                "2 vasos de agua",
                "1 lata de salsa de tomate",
                "1 cebolla picada",
                "1 ajo",
                "1 cucharadita de comino",
                "1 cucharadita de oregano",
                "sal y pimienta al gusto",
                "salsa al gusto"]

for ingrediente in ingredientes:
    sql = 'INSERT INTO ingredientes (id_receta, ingrediente) VALUES (%s,"%s")' % (ultimoid, ingrediente)
    cursor.execute(sql)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Devuelve el tiempo actual, previsión y alertas para un código
postal dado con datos de WeatherUnderground.com.

@author: Greg Walters
@organization: Full Circle Magazine
@license: GPL
@version: 1.0
@status: beta

B{Usage:} python el_tiempo.py [opciones]

B{Options:}
    - -h, --help Mostrar esta ayuda
    - -l, --location Ciudad, Provincia
    - -z, --zip Código postal

B{Examples:}
    - el_tiempo.py -h (muestra esta ayuda)
    - el_tiempo.py -z 80013 (usa el código postal 80013 como localizador)
    - el_tiempo.py -l Alcobendas (usa el municipio de Alcobendas como localizador)
"""

from xml.etree import ElementTree as etree
import urllib
import sys
import getopt

__docformat__ = "epytext"

eng2spa = {"Monday": "Lunes",
           "Monday Night": "Lunes por la noche",
           "Tuesday": "Martes",
           "Tuesday Night": "Martes por la noche",
           "Wednesday": "Miércoles",
           "Wednesday Night": "Miércoles por la noche",
           "Thursday": "Jueves",
           "Thursday Night": "Jueves por la noche",
           "Friday": "Viernes",
           "Friday Night": "Viernes por la noche",
           "Saturday": "Sábado",
           "Saturday Night": "Sábado por la noche",
           "Sunday": "Domingo",
           "Sunday Night": "Domingo por la noche",
           "Today": "Hoy",
           "Tonight": "Esta noche",
           "North": "Norte",
           "South": "Sur",
           "East": "Este",
           "West": "Oeste",
           "Clear": "Despejado",
           "Scattered Clouds": "Nubes dispersas",
           "Partly Cloudy": "Parcialmente nublado",
           "Mostly Cloudy": "Muy nublado",
           "Fog": "Niebla",
           "Chance of Rain": "Probabilidad de lluvia",
           "Chance Rain": "Probabilidad de lluvia"}
"""Diccionario traductor inglés/español"""

class InfoActual:
    """Esta clase lee el tiempo en XML desde WeatherUnderground.com a partir
    del código postal. Para definir la localización:
        - por código postal: la entrada sería del estilo de 80013 (sin comillas)
        - por ciudad/provincia: la entrada sería del estilo de "London,%20England" (con comillas dobles)"""

    def getTiempoActual(self,ubicacion):
        """Recoge el estado actual del tiempo desde WeatherUnderground.com
        @param ubicacion: Ubicación de referencia
        @type ubicacion: str"""
        try:
            CondicionesActuales = 'http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=%s' % ubicacion
            urllib.socket.setdefaulttimeout(8)
            socket = urllib.urlopen(CondicionesActuales)
            arbol = etree.parse(socket)
            socket.close()
        except:
            print 'ERROR - No se han podido recoger las condiciones actuales del servidor...'
            sys.exit(2)
        # Ubicación
        for ubi in arbol.findall(".//city"):
            self.ubicacion = ubi.text
        # Fecha observación
        for obs in arbol.findall(".//observation_time"):
            self.observado = obs.text
        # Condiciones atmosféricas
        for condiciones in arbol.findall(".//weather"):
            try:
                self.condiciones = eng2spa[condiciones.text]
            except KeyError:
                self.condiciones = condiciones.text
        # Temperatura
        for temperatura in arbol.findall(".//temp_c"):
            self.temperatura = temperatura.text
        # Humedad relativa
        for humedad in arbol.findall(".//relative_humidity"):
            self.humedad = humedad.text
        # Dirección del viento
        for direccion_viento in arbol.findall(".//wind_dir"):
            if direccion_viento.text == "Variable":
                self.direccion_viento = "variable"
            else:
                try:
                    self.direccion_viento = str.replace(eng2spa[direccion_viento.text],"W","O")
                except KeyError:
                    self.direccion_viento = str.replace(direccion_viento.text,"W","O")
        # Velocidad del viento
        for velocidad_viento in arbol.findall(".//wind_mph"):
            self.velocidad_viento = int(round(int(velocidad_viento.text) * 1.609))
        # Presión atmosférica
        for presion in arbol.findall(".//pressure_mb"):
            self.presion = presion.text

    def mostrar(self):
        """Muestra el estado actual del tiempo"""
        print 'Información del tiempo obtenida desde WUnderground.com'
        print 'El tiempo para %s:' % self.ubicacion
        print '\t%s' % self.observado
        print '\tCondiciones climatológicas: %s' % self.condiciones
        print '\tTemperatura: %sºC' % self.temperatura
        print '\tPresión atmosférica: %s mbar' % self.presion
        print '\tHumedad relativa: %s' % self.humedad
        print '\tViento de componente %s con rachas de %s km/h' % (self.direccion_viento, self.velocidad_viento)

class Pronostico:
    """Esta clase lee el pronóstico del tiempo en XML desde WeatherUnderground.com a partir
    del código postal. Para definir la localización:
       - por código postal: la entrada sería del estilo de 80013 (sin comillas)
       - por ciudad/provincia: la entrada sería del estilo de "London,%20England" (con comillas dobles)"""

    def __init__(self):
        """Inicializador de la clase Pronostico"""
        self.pronostico = []           # Pronóstico para hoy/esta noche
        self.titulo = []               # Hoy/esta noche
        self.fecha = ''        
        self.icono = []                # Icono a utilizar para las condiciones climatológicas
        self.periodos = 0
        self.periodo = 0
        #===========================================================
        # Pronóstico extendido
        #===========================================================      
        self.ext_icono = []            # Icono a utilizar para el pronóstico extendido
        self.ext_dia = []              # Día de la semana ("Lunex", "Martes", etc)
        self.ext_maxima = []           # Temperatura máxima
        self.ext_minima = []           # Temperatura mínima
        self.ext_condiciones = []      # Condiciones
        self.ext_periodos = []         # Periodos incluidos en el pronóstico
        self.ext_precipitaciones = []  # Probabilidad de precipitaciones

    def getPronostico(self,ubicacion):
        """Recoge el pronóstico del tiempo desde WeatherUnderground.com
        @param ubicacion: Ubicación de referencia
        @type ubicacion: str"""
        try:
            URLpronostico = 'http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=%s' % ubicacion
            urllib.socket.setdefaulttimeout(8)
            socket = urllib.urlopen(URLpronostico)
            arbol = etree.parse(socket)
            socket.close()
        except:
            print 'ERROR - No se ha podido recoger el pronóstico del servidor...'
            sys.exit(2)
        #===========================================================  
        # Leemos el pronóstico de hoy y (si es posible) el de esta noche
        #===========================================================
        pronostico = arbol.find('.//txt_forecast')
        for p in pronostico:
            if p.tag == 'number':
                self.periodos = p.text
            elif p.tag == 'date':
                self.fecha = p.text
            for subelemento in p:
                if subelemento.tag == 'period':
                    self.periodo = int(subelemento.text)
                if subelemento.tag == 'fcttext':
                    self.pronostico.append(str.replace(subelemento.text,"&deg;","º"))
                elif subelemento.tag == 'icon':
                    self.icono.append(subelemento.text)
                elif subelemento.tag == 'title':
                    try:
                        self.titulo.append(eng2spa[subelemento.text])
                    except KeyError:
                        self.titulo.append(subelemento.text)
        #===========================================================
        # Leemos el pronóstico extendido
        #===========================================================
        pronostico = arbol.find('.//simpleforecast')
        for p in pronostico:
            for subelemento in p:
                if subelemento.tag == 'period':
                    self.ext_periodos.append(subelemento.text)
                elif subelemento.tag == 'conditions':
                    try:
                        self.ext_condiciones.append(eng2spa[subelemento.text])
                    except KeyError:
                        self.ext_condiciones.append(subelemento.text)
                elif subelemento.tag == 'icon':
                    self.ext_icono.append(subelemento.text)
                elif subelemento.tag == 'pop':
                    self.ext_precipitaciones.append(subelemento.text)
                elif subelemento.tag == 'date':
                    for hijo in subelemento.getchildren():
                        if hijo.tag == 'weekday':
                            try:
                                self.ext_dia.append(eng2spa[hijo.text])
                            except KeyError:
                                self.ext_dia.append(hijo.text)
                elif subelemento.tag == 'high':
                    for hijo in subelemento.getchildren():
                        if hijo.tag == 'celsius':
                            self.ext_maxima.append(hijo.text)
                elif subelemento.tag == 'low':
                    for hijo in subelemento.getchildren():
                        if hijo.tag == 'celsius':
                            self.ext_minima.append(hijo.text)

    def mostrar(self,incluirHoy):
        """Muestra el pronóstico del tiempo
        @param incluirHoy: Flag que determina si incluimos el día actual en el pronóstico
        @type incluirHoy: bool"""
        for contador in range(int(self.periodo)):
            if contador == 0:
                print'----------------------------------------'
            print 'Pronóstico para %s' % self.titulo[contador].lower()
            print 'Pronóstico = %s' % self.pronostico[contador]
            print 'Icono=%s' % self.icono[contador]
            print '----------------------------------------'
        print 'Pronóstico extendido...'
        inicioRango = 0 if incluirHoy else 1
        for contador in range(inicioRango,6):
            print self.ext_dia[contador]
            print '\tMáxima: %sºC' % self.ext_maxima[contador]
            print '\tMínima: %sºC' % self.ext_minima[contador]
            if int(self.ext_precipitaciones[contador]) == 0:
                print '\tCondiciones climatológicas: %s' % self.ext_condiciones[contador]
            else:
                print '\tCondiciones climatológicas: %s. %d%% de probabilidad de precipitaciones.' % (self.ext_condiciones[contador], int(self.ext_precipitaciones[contador]))

def uso():
    """Muestra el modo de uso de esta aplicación"""
    print __doc__

def main(argv):
    """Función main de esta aplicación
    @param argv: Parámetros recibidos por línea de comandos
    @type argv: list"""
    try:
        opts, args = getopt.getopt(argv, "hz:l:", ["help=", "zip=", "location="])
    except getopt.GetoptError:
        uso()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            uso()
            sys.exit()
        elif opt in ("-l", "--location"):
            ubicacion = arg
        elif opt in ("-z", "--zip"):
            ubicacion = arg
        print 'Ubicación = %s' % ubicacion
        actual = InfoActual()
        pronostico = Pronostico()

        actual.getTiempoActual(ubicacion)
        pronostico.getPronostico(ubicacion)

        actual.mostrar()
        print '=' * 50
        pronostico.mostrar(False)

if __name__ == "__main__":
    main(sys.argv[1:])


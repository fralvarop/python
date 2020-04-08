#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.etree import ElementTree as etree
arbol = etree.parse('Cache.loc')

print 'XML original:'
etree.dump(arbol)

w = arbol.find('.//waypoint')

for w1 in w:
    if w1.tag == "name":
        # Get text of cache name up to the phrase "Open Cache: "
        CacheName = w1.text[:w1.text.find("Open Cache:")-1]
        # Get the text between "Open Cache: " and "Cache Type: "
        OpenCache = w1.text[w1.text.find("Open Cache:")+12:w1.text.find("Cache Type: ")-1]
        # More of the same
        CacheType = w1.text[w1.text.find("Cache Type:")+12:w1.text.find("Cache Size: ")-1]
        CacheSize = w1.text[w1.text.find("Cache Size:")+12:w1.text.find("Difficulty: ")-1]
        Difficulty = w1.text[w1.text.find("Difficulty:")+12:w1.text.find("Terrain   : ")-1]
        Terrain = w1.text[w1.text.find("Terrain   :")+12:]
        if list(w1.keys()):
            for name,value in list(w1.items()):
                if name == 'id':
                    CacheID = value
    elif w1.tag == "coord":
        if list(w1.keys()):
            for name,value in list(w1.items()):
                if name == "lat":
                    Lat = value
                elif name == "lon":
                    Lon = value
    elif w1.tag == "type":
        GType = w1.text
    elif w1.tag == "link":
        if list(w1.keys()):
            for name, value in list(w1.items()):
                Info = value
        Link = w1.text

print ''
print 'Datos parseados:'
print 'Cache Name: ', CacheName
print 'Cache ID: ', CacheID
print 'Open Cache: ', OpenCache
print 'Cache Type: ', CacheType
print 'Cache Size: ', CacheSize
print 'Dificultad: ', Difficulty
print 'Terreno: ', Terrain
print 'Latitud: ', Lat
print 'Longitud: ', Lon
print 'GType: ', GType
print 'Enlace: ', Link
print '=' * 25
print 'Hecho'

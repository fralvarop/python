#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os

colorFondo = 208, 202, 104
colorFuente = 255, 255, 255 # Blanco

# Centramos la ventana en la pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Inicializamos pygame
pygame.init()

# Configuramos la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Establecemos el titulo de la ventana
pygame.display.set_caption('Prueba de Pygame #3')

# Fijamos el color de fondo
pantalla.fill(colorFondo)

# Escribimos un texto en la ventana
fuente = pygame.font.Font("/usr/share/fonts/truetype/msttcorefonts/cour.ttf",27)

fuente.set_bold(True)
fuente.set_italic(True)

texto = fuente.render('Esto es un texto de prueba', True, colorFuente, colorFondo)
rectangulo_texto = texto.get_rect()

# Centramos el texto
rectangulo_texto.centerx = pantalla.get_rect().centerx
rectangulo_texto.centery = pantalla.get_rect().centery

# "Planchamos" el texto en la ventana
pantalla.blit(texto, rectangulo_texto)
pygame.display.update()

# Mostramos la pantalla y esperamos el evento
while True:
    if pygame.event.wait().type in (KEYDOWN, MOUSEBUTTONDOWN):
        break


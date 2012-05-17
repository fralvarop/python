#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os

fondo = 208, 202, 104

# Centramos la ventana en la pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Inicializamos pygame
pygame.init()

# Configuramos la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Establecemos el titulo de la ventana
pygame.display.set_caption('Prueba de Pygame #1')

# Fijamos el color de fondo
pantalla.fill(fondo)
pygame.display.update()

# Mostramos la pantalla y esperamos el evento
while True:
    if pygame.event.wait().type in (KEYDOWN, MOUSEBUTTONDOWN):
        break


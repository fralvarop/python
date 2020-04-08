#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os
import sys

class Sprite(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Guardamos una copia del rectángulo de la pantalla
        self.pantalla = pygame.display.get_surface().get_rect()
        # Creamos una variable que almacene la anterior posición del sprite
        self.anterior_sprite = (0, 0, 0, 0)
        self.imagen = pygame.image.load('stick.png')
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.x = posicion[0]
        self.rectangulo.y = posicion[1]

    def actualizar(self, cantidad):
        # Hacemos una copia del rectángulo actual para borrar
        self.anterior_sprite = self.rectangulo
        # Movemos el rectángulo la distancia especificada
        self.rectangulo = self.rectangulo.move(cantidad)
        # Comprobamos si nos salimos de la pantalla
        if self.rectangulo.x < 0:
            self.rectangulo.x = 0
        elif self.rectangulo.x > (self.pantalla.width - self.rectangulo.width):
            self.rectangulo.x = self.pantalla.width - self.rectangulo.width
        if self.rectangulo.y < 0:
            self.rectangulo.y = 0
        elif self.rectangulo.y > (self.pantalla.height - self.rectangulo.height):
            self.rectangulo.y = self.pantalla.height - self.rectangulo.height

fondo = 0,255,127
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pantalla = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Ejemplo de Pygame #4: Sprite')
pantalla.fill(fondo)

# Creamos el sprite del personaje
personaje = Sprite((pantalla.get_rect().centerx, pantalla.get_rect().centery))
pantalla.blit(personaje.imagen, personaje.rectangulo)

# Creamos una superficie en blanco con las dimensiones del personaje
vacio = pygame.Surface((personaje.rectangulo.width, personaje.rectangulo.height))
vacio.fill(fondo)

pygame.display.update()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        # Comprobamos los movimientos (flechas)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                personaje.actualizar([-10, 0])
            elif evento.key == pygame.K_UP:
                personaje.actualizar([0, -10])
            elif evento.key == pygame.K_RIGHT:
                personaje.actualizar([10, 0])
            elif evento.key == pygame.K_DOWN:
                personaje.actualizar([0, 10])
            elif evento.key == pygame.K_q or evento.key == pygame.K_ESCAPE:
                sys.exit()
    # Borramos la anterior posicion pintando "en blanco" en el mismo sitio
    pantalla.blit(vacio, personaje.anterior_sprite)
    # Dibujamos el sprite en su nueva posición
    pantalla.blit(personaje.imagen, personaje.rectangulo)
    # Actualizamos SÓLO las áreas de la pantalla que han sido modificadas
    pygame.display.update([personaje.anterior_sprite, personaje.rectangulo])


#! /usr/bin/env python
# coding: utf-8


"""
hud.py - Docked at the top or bottom of screen. Displays current info about
         game progress.
"""


from __future__ import division, print_function
import pygame
import pygame.freetype
import pygame.font
import brickbreaker.util as u


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pygame.font.init()
pygame.freetype.init()


class Message(pygame.sprite.Sprite):

    def __init__(self, displayArea, text, x_wrap):
        self.rect = displayArea.get_rect()

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(BLACK)
        
        self.font = pygame.freetype.Font(None, 35)
        
        self.TextSurf = u.get_fitted_text_on_surface(text, x_wrap, self.font)
        self.TextRect = self.TextSurf.get_rect()
        self.TextRect.center = ((self.rect.width/2),(self.rect.height/2))
    
    def draw(self):
        self.image.blit(self.TextSurf, self.TextRect)
        
    def set_text_and_wrap(self, text, x_wrap):
        self.image.fill(BLACK)
        self.TextSurf = u.get_fitted_text_on_surface(text, x_wrap, self.font)
        self.TextRect = self.TextSurf.get_rect()
        self.TextRect.center = ((self.rect.width/2),(self.rect.height/2))
        

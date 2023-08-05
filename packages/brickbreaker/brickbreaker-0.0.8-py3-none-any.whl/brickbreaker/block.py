#! /usr/bin/env python
# coding: utf-8


"""
block.py - Holds the classes for the breakout blocks.
""" 


from __future__ import division, print_function
import pygame


color_chart = {
    'r' : pygame.color.THECOLORS['red'], 
    'b' : pygame.color.THECOLORS['blue'], 
    'g' : pygame.color.THECOLORS['green'], 
    'y' : pygame.color.THECOLORS['yellow'],
}

hp_to_color = {
    4 : 'r',
    3 : 'y',
    2 : 'g',
    1 : 'b'
}

color_to_hp = {
    'r' : 4,
    'y' : 3,
    'g' : 2,
    'b' : 1,
}


class Block(pygame.sprite.Sprite):
    """
    A class to store info for each breakout block.
    """
        
    def __init__(self, colorChar, x, y, blocksize):

        pygame.sprite.Sprite.__init__(self)
        self.hp = color_to_hp[colorChar]
        self.position = [x,y]
        self.width, self.height = blocksize
        self.image = pygame.Surface(
            (self.width, self.height), 
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position


    def get_xypos(self):
        """
        Return the xy position of the block.
        
        return: tuple, the x and y position of the block's rect.
        """
        return self.position


    def is_alive(self):
        """
        Returns a boolean whether the block's hp has been depleted.
        
        return: boolean, hp is greater than 0.
        """
        return self.hp > 0
    
    
    def hit(self):
        """
        Decrements the block's hp by one.
        """
        if self.is_alive():
            self.hp -= 1
            if self.hp <= 0:
                self.image.fill((0,0,0,0))
    
    
    def get_worth(self):
        """
        Returns the points the block is worth.
        
        return: integer, amount of points for hitting the block.
        """
        return self.hp * 10


    def draw(self):
        """
        Draws the block's image or blank dependent on its current hp.
        """
        if self.hp > 0:
            ## create a slightly smaller surface than image
            inner = pygame.Surface((self.width - 2, self.height -2))
            ## color this one by the hp value
            inner.fill(color_chart[hp_to_color[self.hp]])
            self.image.fill(pygame.color.THECOLORS['black'])
            ## fill image with black then draw the inner in the center to leave
            ## a 1 pixel black border around the colored portion
            self.image.blit(inner, (1, 1))


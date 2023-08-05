#! /usr/bin/env python
# coding: utf-8


"""
paddle.py - Holds the class for the breakout paddle.
""" 


from __future__ import division, print_function
import pygame


class PlayerPaddle(pygame.sprite.Sprite):
    """
    A class for the player's paddle in breakout.
    """
    
    DEFAULT_SIZE = (96, 8)
    MOVE_VECTORS = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
    }
    
    
    def __init__(self, img, height, xbounds, ybounds):
        """
        Constructor for the PlayerPaddle class.
        
        param: img, a path to an image file to use for the paddle. 
            Pygame supports a few formats but I'm expecting one 
            of jpg, png, or a non-animated gif.
            
        param: xbounds, a tuple of the left and right boundry pixels
            to cap x axis movement.
            
        param: ybounds, a tuple of the top and bottom boundry pixels
            to cap y axis movement.
        """
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = self.DEFAULT_SIZE
        self.texture = pygame.image.load(img)
        self.image = pygame.Surface(
            (self.width, self.height), 
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect()
        self.speed = 30
        self.position = [0, height]
        self.vector = [0, 0]
        self.move = False
        self.xbounds = xbounds
        self.ybounds = ybounds
        self.center()


    def get_xypos(self):
        """
        Return the xy position of the paddle.
        
        return: tuple, the x and y position of the paddle's rect.
        """
        return self.position


    def get_xpos(self):
        """
        Return the x position of the paddle.
        
        return: integer, the x position of the paddle.
        """
        return self.position[0]
    
    
    def get_ypos(self):
        """
        Return the y position of the paddle.
        
        return: integer, the y position of the paddle rect.
        """
        return self.position[1]
    
    
    def get_vector(self):
        """
        Return the paddle's current movement vector.
        
        return: list, the xy direction vector.
        """
        return self.vector


    def set_xypos(self, xy):
        """
        Set the paddle position.
        
        param: xy, the paddle's x and y position in a list.
        """
        self.position = xy
        self.rect.x, self.rect.y = xy
        
    
    def set_xpos(self, x):
        """
        Set the paddle's x position.
        
        param: x, the paddle's new x position.
        """
        self.position[0] = x
    
    
    def set_ypos(self, y):
        """
        Set the paddle's y position.
        
        param: y, the paddle's new y position. 
        """
        self.position[1] = y
    
    
    def can_move(self, tf):
        """
        Sets whether the paddle will move or not.
        
        param: tf, a boolean True or False for paddle movement.
        """
        self.move = tf


    def set_vector(self, vec):
        """
        Set the movement vector for the paddle. It can only move left 
        and right by default.
        
        param: vec, a list of 2 values for x and y. -1 is the negative 
            direction, 0 is not move, 1 is the positive direction.
        """
        self.vector = vec


    def center(self):
        """
        Centers the paddle position on the board.
        """
        self.set_xypos([self.xbounds[1] // 2 - self.width // 2, self.get_ypos()])
    
    
    def read_keys(self, keys):
        """
        Can read the keys that are pressed and act on them.
        
        param: keys, a dict of which pygame keys are currently pressed.
        """
        ## set movement direction for paddle and update position
        move_vector = (0, 0)
        for m in (self.MOVE_VECTORS[key] for key in self.MOVE_VECTORS if keys[key]):
            move_vector = list(map(sum, zip(move_vector, m)))
        # normalize movement vector
        if sum(map(abs, move_vector)) == 2:
            move_vector = [p/1.4142 for p in move_vector]
        # apply speed to movement vector
        self.set_vector([self.speed * p for p in move_vector])


    def draw(self):
        """
        Draws the paddle's texture to its surface.
        """
        scaled_image = pygame.transform.scale(
            self.texture, 
            (self.width, self.height)
        )
        self.image.blit(scaled_image, (0, 0))
    
    
    def update(self, time_passed):
        """
        Call during loop to update the paddle's position onscreen.
        
        param: time_passed, the amount of time that has passed since the
            last update().
        """
        if self.move:
            ## get new paddle position
            x, y = self.position
            new_x, new_y = [
                 x + self.vector[0] * time_passed * self.speed,
                 y + self.vector[1] * time_passed * self.speed
            ]
            ## cap xmovement by xbounds and ymovement by ybounds
            new_x = max(new_x, self.xbounds[0])
            new_x = min(new_x, self.xbounds[1] - self.width)
            new_y = max(new_y, self.ybounds[0])
            new_y = min(new_y, self.ybounds[1] - self.height)
            ## save new position
            self.set_xypos([new_x, new_y])


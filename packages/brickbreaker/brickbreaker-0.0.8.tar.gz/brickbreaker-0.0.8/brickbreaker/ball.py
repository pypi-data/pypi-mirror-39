#! /usr/bin/env python
# coding: utf-8


"""
ball.py - Holds the class for the breakout ball.
"""


from __future__ import division, print_function
import pygame
import math
import random
import brickbreaker.util as u


class Ball(pygame.sprite.Sprite):
    """
    A class for the ball in breakout.
    """
    
    ## constants for ball
    CW = False
    CCW = True
    BALL_SIZE = (17, 17)
    
    
    def __init__(self, img):
        """
        Constructor for the Ball class.
        
        param: img, a path to an image file to use for the ball. 
            Pygame supports a few formats but I'm expecting one 
            of jpg, png, or a non-animated gif.
        """
        ## there's some methods in the sprite class for groups that are 
        ## optional but might be helpful, haven't used any yet
        pygame.sprite.Sprite.__init__(self)
        self.texture = pygame.image.load(img)
        self.image = pygame.Surface(
            self.BALL_SIZE, 
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect()
        self.speed = 500
        self.position = [0, 0]
        self.vector = [0, 0]
        self.move = False
        self.rotate = False
        self.rotation_angle = 0
        self.rotation_speed = 12
        self.rotation_direction = self.CW
        self.rotated_rect = self.rect.copy()
        self.angle = 0


    def get_xypos(self):
        """
        Return the xy position of the ball.
        
        return: tuple, the x and y position of the ball's rect.
        """
        return self.position


    def get_xpos(self):
        """
        Return the x position of the ball.
        
        return: integer, the x position of the ball.
        """
        return self.position[0]
    
    
    def get_ypos(self):
        """
        Return the y position of the ball.
        
        return: integer, the y position of the ball rect.
        """
        return self.position[1]
    
    
    def get_vector(self):
        """
        Return the ball's current movement vector.
        
        return: list, the xy direction vector.
        """
        return self.vector


    def get_angle(self):
        """
        Return the ball's current angle.
        
        return: float, the angle the ball is traveling in degrees.
        """
        return self.angle * (180 / math.pi)
        
        
    def set_xypos(self, xy):
        """
        Set the ball position.
        
        param: xy, the ball's x and y position in a list.
        """
        self.position = xy
        self.rect.x, self.rect.y = xy
        
    
    def set_xpos(self, x):
        """
        Set the ball's x position.
        
        param: x, the ball's new x position.
        """
        self.position[0] = x
        self.rect.x = x
    
    
    def set_ypos(self, y):
        """
        Set the ball's y position.
        
        param: y, the ball's new y position. 
        """
        self.position[1] = y
        self.rect.y = y
    
    
    def set_vector(self, vec):
        """
        Set the movement vector for the ball. This controls which cardinal
        direction the ball moves in.
        
        param: vec, a list of 2 values for x and y. -1 is the negative 
            direction, 0 is not move, 1 is the positive direction.
        """
        self.vector = vec


    def set_angle(self, ang):
        """
        Sets the angle the ball will move in.
        
        param: ang, the new angle in degrees.
        """
        ## keep the angle from 0 to 2pi
        self.angle = (ang * (math.pi / 180)) % (2*math.pi)


    def can_move(self, tf):
        """
        Sets whether the ball will move or not.
        
        param: tf, a boolean True or False for ball movement.
        """
        self.move = tf
    
    
    def can_rotate(self, tf):
        """
        Sets whether the ball will rotate or not.
        
        param: tf, a boolean True or False for ball rotation.
        """
        self.rotate = tf
    
    
    def get_draw_rect(self):
        """
        Return a pygame rect that holds the location to blit the image to 
        a surface. Something like 'to_surf.blit(a_surf, obj.get_draw_rect())'.
        
        return: rect, dimensions of rotated ball image used to blit to a 
            surface.
        """
        return self.rotated_rect.copy()


    def generate_collision_points(self, count, center, radius):
        """
        Generates 'count' number of points on a circle edge from 0 to 2pi.
        These points are used during fine-grained collision detection to 
        detect how the ball needs to reflect after colliding with a block.
        
        param: count, the number of points to generate.
               center, the center xy position of the circle.
               radius, the radius of the circle.
        
        return: tuple, points on the circle to check for block collisions.
        """
        assert (count % 4 == 0), "'count' must be a multiple of four."
        c, hc = count, count/2
        x, y = center
        r = radius
        points = ()
        for num in range(0, c):
            points += (
                (
                    x + r * math.cos(num * math.pi / hc), 
                    y + r * math.sin(num * math.pi / hc)
                ),
            )
        return points 


    def testPaddleCollision(self, paddle):
        """
        Finds a paddle collision by checking if the ball rect overlaps
        with the paddle rect.
        
        param: paddle, a PlayerPaddle object. Needs to have a pygame.Rect
            object as a .rect variable.
        
        return: boolean, True if collision, False if not.
        """
        collision = self.rect.colliderect(paddle)
        ycoll_latch = False
        if collision:
            ycoll_latch = True
        return ycoll_latch


    def read_keys(self, keys):
        """
        Can read the keys that are pressed and act on them.
        
        param: keys, a dict of which pygame keys are currently pressed.
        """
        ## launch the ball from a standstill to some x and y direction
        if not self.move and keys[pygame.K_SPACE]:
            # self.set_angle(random.choice([15, 30, 45, 60, 75, 105, 120, 135, 150, 165]))
            self.set_angle(45)
            self.move = True
            self.rotate = True


    def draw(self):
        """
        Draws the ball's rotated texture to its surface.
        """
        scaled_image = pygame.transform.scale(
            self.texture, 
            self.BALL_SIZE
        )
        rotated_image = pygame.transform.rotate(scaled_image, self.rotation_angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = self.rect.center
        self.image = rotated_image
        self.rotated_rect = rotated_rect


    def update(self, time_passed):
        """
        Call during loop to update ball's position onscreen.
        
        param: time_passed, the amount of time that has passed since the
            last update().
        """
        ## handle rotation angle to make ball spin
        vx, vy = self.vector
        if vx < 0:
            self.rotation_direction = self.CCW
        else:
            self.rotation_direction = self.CW
        if self.rotate:
            if self.rotation_direction:
                self.rotation_angle = self.rotation_angle + self.rotation_speed
            else:
                self.rotation_angle = self.rotation_angle - self.rotation_speed 
        ## wrap rotation angle at full rotation
        self.rotation_angle = self.rotation_angle % 360
        ## update ball position
        if self.move:
            x, y = self.position
            ## set velocity vector based on angle, y axis is inverted in pygame
            ax, ay = u.angle_to_vector(self.angle)
            self.vector = [ax, -ay]
            ## update position from velocity vector
            self.position = [
                 x + self.vector[0] * time_passed * self.speed,
                 y + self.vector[1] * time_passed * self.speed
            ]
            self.rect.x, self.rect.y = self.position


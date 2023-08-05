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


BLACK = pygame.color.THECOLORS['black']
WHITE = pygame.color.THECOLORS['white']


pygame.font.init()
pygame.freetype.init()


class HUD(pygame.sprite.Sprite):
    """
    A heads up display for breakout. Shows the current score and number of
    extra lives remaining.
    """
    
    ## 255 is opaque, 0 is fully transparent
    TRANSPARENT = (0, 0, 0, 100)
    ## a small amount of padding to add if needed
    PADDING = 5
    ## can only display so many lives, even if there are more
    MAX_SHOW_LIVES = 5


    def __init__(self, size, lives_img = False):
        """
        Constructor for the HUD class.
        
        param: size, a tuple with the width and height the HUD needs to 
            be to fit onscreen.
                
        param: lives_img, an image to show for the lives counter. If no 
            image is supplied, it will just show numbers.
        """
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = size
        if lives_img:
            self.lives_texture = pygame.image.load(lives_img)
        else:
            self.lives_texture = None
        self.image = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect()
        ## default values, use setters to change per level
        self.score_val = 0
        self.highscore_val = 0
        self.lives_val = self.MAX_SHOW_LIVES
        self.level_val = "1"
        self.message = "All Your Block Are Belong To Us"
        self.screen_pos = self.set_screen_pos("top")
        self.font = pygame.font.Font(None, 40)
        self.lives_texture_size = (25, 25)
        self.label_pos = {
            "highscore" : (
                3 * self.width // 4,
                2 * self.height // 3 + self.PADDING
            ),
            "score" : (
                3 * self.width // 4, 
                self.height // 3 + self.PADDING
            ),
            "lives" : (
                3 * self.width // 4, 
                self.PADDING
            ),
        }


    def get_image(self):
        """
        Returns the surface the HUD is drawn to.
        
        return: pygame surface, contains the drawn HUD
        """
        return self.image


    def get_screen_pos(self):
        """
        Returns the screen position the HUD should be drawn at.
        
        return: string, either 'top' or 'bottom'
        """
        return self.screen_pos


    def get_size(self):
        """
        Returns the width and height of the HUD.
        
        return: tuple, HUD width and height as integers.
        """
        return self.width, self.height


    def set_score_val(self, score):
        """
        Set the displayed score to a new value.
        """
        self.score_val = score


    def set_highscore_val(self, score):
        """
        Set the displayed highscore to a new value.
        """
        self.highscore_val = score


    def set_lives_val(self, lives):
        """
        Set the displayed lives to a new value.
        """
        self.lives_val = min(self.MAX_SHOW_LIVES, lives)


    def set_level_val(self, level):
        """
        Set the displayed level to a new value.
        """
        self.level_val = level


    def set_screen_pos(self, loc):
        """
        Allow the HUD to be at the top of the screen or at the bottom.
        
        param: loc, a string of 'top' or 'bottom'
        """
        assert (
            loc == "top" or loc == "bottom"
        ), "Only 'top' or 'bottom' are valid screen locations." 
        self.screen_pos = loc


    def set_message(self, message):
        """
        Set a message to display in the HUD.
        
        param: message, text to display to the player.
        """
        self.message = message


    def draw(self):
        """
        Draws the HUD components to its image.
        """
        self.image.fill(self.TRANSPARENT)
        ## get a surface with the text drawn to it for each piece to 
        ## be put on the HUD
        lives_label = self.font.render(
            "Lives: ",
            True,
            WHITE
        )
        score_label = self.font.render(
            "Player Score: ",
            True,
            WHITE
        )
        highscore_label = self.font.render(
            "High Score: ",
            True,
            WHITE
        )
        score_amount = self.font.render(
            str(self.score_val),
            True,
            WHITE
        )
        highscore_amount = self.font.render(
            str(self.highscore_val),
            True,
            WHITE
        )
        self.image.blit(
            highscore_label, 
            (
                self.label_pos["highscore"][0] - (highscore_label.get_width() - lives_label.get_width()),
                self.label_pos["highscore"][1] - self.PADDING // 2
            )
        )
        if self.score_val > self.highscore_val:
            self.highscore_val = self.score_val
        self.image.blit(
            highscore_amount, 
            (
                self.width - self.PADDING - highscore_amount.get_width(),
                self.label_pos["highscore"][1]
            )
        )
        self.image.blit(
            score_label, 
            (
                self.label_pos["score"][0] - (score_label.get_width() - lives_label.get_width()),
                self.label_pos["score"][1]
            )
        )
        self.image.blit(
            score_amount, 
            (
                self.width - self.PADDING - score_amount.get_width(),
                self.label_pos["score"][1]
            )
        )
        self.image.blit(
            lives_label, 
            self.label_pos["lives"]
        )
        ## either show the number of lives or an icon image if one was 
        ## passed into the HUD constructor
        if self.lives_texture == None:
            lives_amount = self.font.render(
                str(self.lives_val),
                True,
                WHITE
            )
            self.image.blit(
                lives_amount, 
                (
                    self.width - self.PADDING - lives_amount.get_width(),
                    self.label_pos["lives"][1]
                )
            )
        else:
            ## scale the image down first
            scaled_image = pygame.transform.scale(
                self.lives_texture, 
                self.lives_texture_size
            )
            start_x = self.width - scaled_image.get_width() - self.PADDING
            for num in range(0, self.lives_val):
                self.image.blit(scaled_image, (start_x, self.label_pos["lives"][1]))
                start_x -= (scaled_image.get_width() + self.PADDING)
        ## player message needs a different font
        message_font = pygame.freetype.Font(None, 35)
        message = u.get_fitted_text_on_surface(
            self.message,
            self.width - self.width//4 - self.PADDING,
            message_font
        )
        ## blit message to image
        self.image.blit(
            message,
            (self.PADDING, 0)
        )


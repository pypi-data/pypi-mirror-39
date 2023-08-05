'''
Created on Oct 27, 2018

@author: brent

This file holds all the levels of the game
'''


import pygame
import brickbreaker.block as bl
import brickbreaker.object_definitions as obj


#this this is a matrix of bricks that will be loaded into the game

#colors are {r: red, b: blue, g: green, y: yellow}
### im not sure how to actually make the bricks colored yet



level1 = '''
g g
g
'''

level2 = '''
   yyyy
  gggggg
 gyy  yyg
  
 gyy  yyg
  gggggg
   yyyy
   
'''

test_level = [
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "    rrrrrrrrrrrrrrrrrrrrrrrr    ",
    "    yyyyyyyyyyyyyyyyyyyyyyyy    ",
    "    gggggggggggggggggggggggg    ",
    "    bbbbbbbbbbbbbbbbbbbbbbbb    ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
]
    

level_list = [level1, level2]


def get_levels():
    """
    Instantiates and returns a copy of each level.
    """
    return [
        Level(obj.level_1),
        Level(obj.level_2),
        Level(obj.level_3),
        Level(obj.level_4),
    ]


class Level(object):
    """
    Each Level has a specific block layout, a background, and a 
    soundtrack that will play.
    """
    
    
    def __init__(self, level_def):
        self.id = level_def["id"]
        self.name = level_def["name"]
        self.background = pygame.image.load(level_def["background"]).convert()
        self.soundtrack = level_def["soundtrack"]
        self.block_size = level_def["block_size"]
        self.blocks = self._load_level(level_def["block_layout"])


    def get_id(self):
        """
        Returns an id number unique to each level.
        
        return: integer, the level's id number.
        """
        return self.id


    def get_name(self):
        """
        Returns the level's name.
        
        return: string, the name of the level.
        """
        return self.name 


    def get_background(self):
        """
        Returns a pygame surface of the background image for this 
        level.
        
        return: surface, the background image.
        """
        return self.background
    
    
    def get_soundtrack(self):
        """
        Returns the music track/tracks to play.
        
        return: list, tuples of the path to the track and how many
            times to play it (0 means to loop forever)
        """
        return self.soundtrack


    def get_block_size(self):
        """
        Returns the size of the blocks in this level.
        
        return: tuple, the block width and height.
        """
        return self.block_size


    def get_blocks(self):
        """
        Returns the block layout for this level.
        
        return: list, contains all the blocks in the level.
        """
        return self.blocks


    def _load_level(self, level):
        """
        Creates a list of blocks from a grid of characters representing blocks.
        
        param: level, a list of strings that are the block layout for a level.
        
        return: list, all the blocks in the level.
        """
        level_blocks = []
        ## starting position is at the top left corner
        x = y = 0
        for row in level:
            for col in row:
                if col != ' ':
                    a_block = bl.Block(
                        col, x, y, self.block_size
                    )
                    level_blocks.append(a_block)
                ## x position is incremented by the block width for each character
                x += self.block_size[0]
            ## y position is incremented by block height for each row
            y += self.block_size[1]
            ## x position is reset to 0 at the start of each row
            x = 0
        return level_blocks


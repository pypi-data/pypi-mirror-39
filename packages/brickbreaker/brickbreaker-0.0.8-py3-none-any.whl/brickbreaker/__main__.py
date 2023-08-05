#! /usr/bin/env python
# coding: utf-8


"""
main.py - Script to run the game. Execute this to play.
"""


############################################################# imports ##
from __future__ import division, print_function
import pygame
import pygame.locals
import brickbreaker.game_manager as gman
import sys, os

## changes directory to scripts directory for game to find all
## the asset stuff it needs
os.chdir(os.path.dirname(__file__))

########################################################### constants ##
MAIN_SIZE = (1024, 768)
GAME_SIZE = MAIN_SIZE 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

######################################################## pygame setup ##
pygame.mixer.pre_init(
    frequency=22050, 
    size=-16, 
    channels=8, 
    buffer=4096
)
pygame.init()

############################################################ gameloop ##
def main():

    ############################################## setup for gameloop ##
    display_info = pygame.display.Info()
    ## main_screen = pygame.display.set_mode(
        ## (display_info.current_w, display_info.current_h),
        ## pygame.SRCALPHA|pygame.RESIZABLE|pygame.FULLSCREEN, 
        ## 32
    ## )
    main_screen = pygame.display.set_mode(
        MAIN_SIZE, 
        pygame.SRCALPHA|pygame.RESIZABLE, 
        32
    )
    game_screen = pygame.Surface(
        GAME_SIZE
    )
    pygame.display.set_caption('Breakout for Pygame')
    
    ## time variables for loop time
    acc_time = 0.0
    logic_interval = 1/90
    current_time = pygame.time.get_ticks() - 1

    ## game manager handles running the game
    gm = gman.GameManager(game_screen)
    
    ################################################# actual gameloop ##
    
    while True:
        
        ## update time variables
        new_time = pygame.time.get_ticks()
        frame_time = (new_time - current_time) / 1000
        current_time = new_time
        
        ## enables screen resizing with mouse on window edges
        now_screen_size = main_screen.get_size()
        new_screen_size = now_screen_size
        
        ## process queued events
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.size
            if event.type == pygame.QUIT:
                raise SystemExit
                
        ## get which keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            ## maybe pause/unpause game here eventually?
            raise SystemExit
        
        ## pass keys to be read by stuff that needs them
        gm.set_keys_pressed(keys)
        
        ## check for logic updates
        while frame_time > 0.0:
            ## calculate dt for updates
            dt = min(frame_time, logic_interval)
            frame_time -= dt
            acc_time += dt
            ## do game logic updates here
            gm.update(dt)

        ## draw screen updates once dt is spent 
        gm.draw()       
        main_screen.fill((255,0,0))
        ## resize the screen from earlier if needed
        if new_screen_size != now_screen_size:
            now_screen_size = new_screen_size
            main_screen = pygame.display.set_mode(
                new_screen_size, 
                pygame.SRCALPHA|pygame.RESIZABLE, 
                32
            )
        ## blit game surface to main surface
        main_screen.blit(
            pygame.transform.scale(
                gm.image, 
                now_screen_size
            ),
            (0, 0)
        )
        pygame.display.update()

    ################################################# end of gameloop ##

################################################################# run ##

# start mainloop
main()
# finished
sys.exit(0)
 

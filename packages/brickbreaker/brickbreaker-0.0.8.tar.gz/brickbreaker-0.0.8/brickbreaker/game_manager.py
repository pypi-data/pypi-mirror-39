#! /usr/bin/env python
# coding: utf-8

"""
game_manager.py - Manages game execution.
"""


import pygame
import pygame.font
import math
import sys
import brickbreaker.ball as b
import brickbreaker.paddle as p
import brickbreaker.hud as h
import brickbreaker.message as m
import brickbreaker.sound as snd
import brickbreaker.timer as tmr
import brickbreaker.level as lvl
import brickbreaker.object_definitions as obj
import brickbreaker.util as u


class GameManager(object):
    """
    A class to manage the different game states.
    """
    
    POSSIBLE_STATES = [
        "title", 
        "launch", 
        "inplay", 
        "lostball",
        "levelcomplete",
        "gameover",
        "wingame",
        "continue",
    ]
    
    
    def __init__(self, draw_surface):
        """
        Constructor for the game manager.
        
        param: draw_surface, a pygame surface to draw stuff to.
        """
        self.image = draw_surface
        self.screen_width, self.screen_height = draw_surface.get_size()
        self.ball = b.Ball(
            obj.beach_ball["texture"],
        )
        self.paddle = p.PlayerPaddle(
            obj.blue_paddle["texture"], 
            7 * self.screen_height // 8,
            (0, self.screen_width),
            (0, self.screen_height)
        )
        self.hud = h.HUD(
            (self.image.get_width(), self.image.get_height()//8), 
            obj.beach_ball["texture"],
        )
        self.delay_timer = tmr.get_timer()
        self.music = snd.get_music_player()
        self.se = snd.get_sound_effects_player()
        self.load_se()
        self.message = m.Message(self.image, "", 0)
        ## load starting level and set title state
        self.current_state = "title"
        self.all_levels = lvl.get_levels()
        self.set_level(1)


    def get_current_state(self):
        """
        Returns the current game state.
        
        return: string, value representing game state.
        """
        return self.current_state
    
    
    def set_current_state(self, state):
        """
        Sets the game state to transition to.
        
        param: state, the next state to change to.
        """
        assert (state in self.POSSIBLE_STATES), '"' + state + "' not a possible state."
        self.current_state = state

        
    def set_keys_pressed(self, keys):
        """
        Sets the keys currently pressed on the keyboard.
        
        param: keys, a dict of which pygame keys are currently pressed.
        """
        self.keys = keys


    def check_wall_collisions(self):
        """
        Checks whether the ball hits one of the walls or not. If the bottom 
        wall is hit the player will forfeit that ball and restart from the 
        paddle position.
        """
        display_width, display_height = self.image.get_size()
        hud_width, hud_height = self.hud.get_size()
        past_bottom = False
        if self.ball.rect.left < 0:
            self.se.play("paddle_wall_collide")
            self.ball.set_xpos(0)
            self.ball.set_angle(-self.ball.get_angle() + 180)
        elif self.ball.rect.right > display_width:
            self.se.play("paddle_wall_collide")
            self.ball.set_xpos(display_width - self.ball.rect.width)
            self.ball.set_angle(-self.ball.get_angle() + 180)
        if self.ball.rect.top < hud_height :
            self.se.play("paddle_wall_collide")
            self.ball.set_ypos(hud_height)
            self.ball.set_angle(-self.ball.get_angle())
        elif self.ball.rect.bottom > display_height:
            # self.ball.set_ypos(display_height - self.ball.rect.height)
            # self.ball.set_angle(-self.ball.get_angle())
            past_bottom = True
        return past_bottom


    def check_block_collisions(self):
        """
        This method will take a few points on the ball and check each block
        to see if the ball has collided with it. 
        """
        ## only using 4 points on the ball for now
        btop, bleft, bright, bbottom =  (
            self.ball.rect.midtop, 
            self.ball.rect.midleft, 
            self.ball.rect.midright, 
            self.ball.rect.midbottom
        )
        for block in self.level.get_blocks():
            if block.is_alive():
                top_collide = block.rect.collidepoint(bbottom)
                left_collide = block.rect.collidepoint(bright)
                right_collide = block.rect.collidepoint(bleft)
                bottom_collide = block.rect.collidepoint(btop)
                
                if top_collide or left_collide or right_collide or bottom_collide:
                    self.se.play("paddle_wall_collide")
                
                if top_collide:
                    self.score += block.get_worth()
                    self.hud.set_score_val(self.score)
                    block.hit()
                    ## move the ball out of the collision
                    self.ball.set_ypos(block.rect.y - self.ball.rect.height)
                    ## change the angle to where the ball needs to go
                    if self.ball.vector[1] > 0:
                        ## moving towards block is y axis reflection
                        self.ball.angle = -self.ball.angle
                    else:
                        ## moving away from block is x axis reflection
                        self.ball.angle = -self.ball.angle + math.pi
                elif left_collide and self.ball.vector[0] > 0:
                    self.score += block.get_worth()
                    self.hud.set_score_val(self.score)
                    block.hit()
                    self.ball.set_xpos(block.rect.x - self.ball.rect.width)
                    if self.ball.vector[0] > 0:
                        self.ball.angle = -self.ball.angle + math.pi
                    else:
                        self.ball.angle = -self.ball.angle
                elif right_collide:
                    self.score += block.get_worth()
                    self.hud.set_score_val(self.score)
                    block.hit()
                    self.ball.set_xpos(block.rect.x + block.rect.width)
                    if self.ball.vector[0] < 0:
                        self.ball.angle = -self.ball.angle + math.pi
                    else:
                        self.ball.angle = -self.ball.angle
                elif bottom_collide:
                    self.score += block.get_worth()
                    self.hud.set_score_val(self.score)
                    block.hit()
                    self.ball.set_ypos(block.rect.y + block.rect.height)
                    if self.ball.vector[1] < 0:
                        self.ball.angle = -self.ball.angle
                    else:
                        self.ball.angle = -self.ball.angle + math.pi
                ## check if the block died after being hit
                if not block.is_alive():
                    self.se.play("block_explode")
                    self.alive_blocks -= 1
                


    def check_paddle_collisions(self):
        """
        Compare the ball and the paddle to see if the ball needs to reflect
        away. If the ball has collided with the paddle, determine the zone on the paddle
        that the ball collided with to set the appropriate deflection angle
        """
        if self.ball.testPaddleCollision(self.paddle):
            self.se.play("paddle_wall_collide")             
            zones = [] 
            
            startPosX = self.paddle.rect.topleft[0]
            endPosX = self.paddle.rect.topright[0]
            
            intervalDist = (self.paddle.rect.width) / 6  #All zones are equal to 1/6 of the paddle's width except the center zone, which is the center 1/3               
            
            zones.append(startPosX)
            
            zoneStart = startPosX
            
            #using the paddle's current position, set the zones
            for i in range(0, 6):
                if i != 2 and i != 3:
                    zones.append(int(zoneStart + intervalDist))
                    zoneStart += intervalDist
                elif i == 2:
                    zones.append(int(zoneStart + (intervalDist * 2)))
                    zoneStart += intervalDist * 2
                else:
                    pass
                
            zones.append(endPosX)
            
            bottomCenterBallX = self.ball.rect.midbottom[0]
                        
            hitZone = 3 #default hit zone is center, in the case the zone fails to be determined correctly
            
            if bottomCenterBallX < startPosX: # the ball hit far left on the paddle
                hitZone = 1
            elif bottomCenterBallX > endPosX: # the ball hit far right
                hitZone = 5
            else:
                for num, zone in enumerate(zones): 
                    if zone > bottomCenterBallX: # the ball must be in the current zone once the next zone start is greater than the ball bottom center position
                        hitZone = num
                        break
            
            deflectionAngle = -self.ball.get_angle()
            
            originalAngle = 0
            
            if self.ball.get_vector()[0] > 0:
                originalAngle = 315
            else:
                originalAngle = 225
            
            if hitZone == 1 or hitZone == 5:
                if self.ball.get_vector()[0] > 0:
                    deflectionAngle = -originalAngle + ((self.ball.get_angle() / abs(self.ball.get_angle())) * -15)
                else:
                    deflectionAngle = -originalAngle + ((self.ball.get_angle() / abs(self.ball.get_angle())) * 15)
            elif hitZone == 2 or hitZone == 4:
                if self.ball.get_vector()[0] > 0:
                    deflectionAngle = -originalAngle + ((self.ball.get_angle() / abs(self.ball.get_angle())) * 15)
                else:
                    deflectionAngle = -originalAngle + ((self.ball.get_angle() / abs(self.ball.get_angle())) * -15)

            self.ball.set_ypos(self.paddle.rect.y - self.ball.rect.height)
            self.ball.set_angle(deflectionAngle)


    def state_title(self):
        """
        This state is the initial state of the game. 
        """
        self.message = m.Message(self.image, "     Welcome!    Press Enter To Start!", self.image.get_width() - ((self.image.get_width()//5) * 3))

        ## starting level, state, lives, and score
        if self.keys[pygame.K_RETURN]:
            ## set starting values and update hud
            self.lives = 3
            self.score = 0
            self.highscore = u.getLocalHighScore()
            self.hud.set_lives_val(self.lives)
            self.hud.set_score_val(self.score)
            self.hud.set_highscore_val(self.highscore)
            self.ball.move = False
            self.ball.rotate = False
            self.paddle.move = True
            self.paddle.center()
            self.set_current_state("launch")
            self.music.load()
            self.music.play()


    def state_launch(self):
        """
        The state that precedes 'inplay'. Here, the ball is perched on the paddle
        and the player can move the paddle around to position the ball in a more 
        favorable position before launching it.
        """
        self.hud.set_message(self.level.get_name())
        self.ball.set_xypos([self.paddle.get_xpos() + self.paddle.rect.width//2 - self.ball.rect.width//2, self.paddle.get_ypos() - self.ball.rect.height])
        self.ball.read_keys(self.keys)
        self.paddle.read_keys(self.keys)
        if self.ball.move:
            self.set_current_state("inplay")
            return
    
    
    def state_inplay(self):
        """
        The main state of the game. This is when the player is moving the ball
        around with the paddle trying to break blocks.
        """
        self.ball.read_keys(self.keys)
        self.paddle.read_keys(self.keys)
        past_bottom = self.check_wall_collisions()
        self.check_block_collisions()
        self.check_paddle_collisions()
        ## end state if past the bottom of the screen
        if past_bottom:
            self.set_current_state("lostball")
            return
        ## change state once all blocks are dead
        if self.alive_blocks <= 0:
            self.set_current_state("levelcomplete")
            return
    
    
    def state_lostball(self):
        """
        This state is entered when the ball drops off the screen below the paddle.
        """
        ## first run through lostball state, do this before 
        ## timer has been started
        if (
                not self.delay_timer.is_timing() and 
                not self.delay_timer.is_finished()
        ):
            self.lives -= 1
            self.hud.set_lives_val(self.lives)
            self.message.set_text_and_wrap("   Lives Remaining: " + str(self.lives), self.image.get_width()//2)
            if self.lives <= 0:
                ## setup for gameover state
                self.ball.move = False
                self.ball.rotate = False
                self.paddle.move = False
                self.set_current_state("gameover")
                return
            self.se.play("lose_ball")
            self.ball.move = False
            self.ball.rotate = False
            self.paddle.move = False
            ## now start the timer to counting to some duration
            self.delay_timer.set_duration(3)
            self.delay_timer.reset()
            self.delay_timer.start()
        ## once timer is finished do this 
        if self.delay_timer.is_finished():
            ## reset timer for other states
            self.delay_timer.reset()
            ## setup for launch state
            self.ball.move = False
            self.ball.rotate = False
            self.paddle.move = True
            self.set_current_state("launch")
            return


    def state_levelcomplete(self):
        """
        This state is entered when all the blocks on a level are destroyed.
        """
        ## first run through levelcomplete state, do this before 
        ## timer has been started
        if (
                not self.delay_timer.is_timing() and 
                not self.delay_timer.is_finished()
        ):
            self.music.stop()
            self.se.play("level_complete")
            self.ball.move = False
            self.paddle.move = False
            self.message.set_text_and_wrap("You destroyed all the blocks, LEVEL COMPLETE!!!       Current Score: " + str(self.score) + "          Lives Remaining: " + str(self.lives), self.image.get_width()//2)
            ## now start the timer to counting to some duration
            self.delay_timer.set_duration(5)
            self.delay_timer.reset()
            self.delay_timer.start()
        ## once timer is finished do this 
        if self.delay_timer.is_finished():
            ## reset timer for other states
            self.delay_timer.reset()
            level_num = self.level.get_id()
            if level_num >= len(self.all_levels):
                self.set_current_state("wingame")
                return
            else:
                self.set_level(level_num + 1)
                ## setup for launch state
                self.ball.move = False
                self.ball.rotate = False
                self.paddle.move = True
                self.paddle.center()
                self.music.load()
                self.music.play()
                self.set_current_state("launch")
                return


    def state_gameover(self):
        """
        This state is entered when the player has exhausted all their lives.
        """
        ## first run through gameover state, do this before 
        ## timer has been started
        if (
                not self.delay_timer.is_timing() and 
                not self.delay_timer.is_finished()
        ):
            self.music.stop()
            self.se.play("game_over")
            u.saveLocalScore(self.score)
            u.getLocalLeaderboard()
            self.message.set_text_and_wrap("   Lives Remaining: " + str(self.lives) + "            GAMEOVER...", self.image.get_width()//2)
            ## now start the timer to counting to some duration
            self.delay_timer.set_duration(10)
            self.delay_timer.reset()
            self.delay_timer.start()
        ## do this once timer is done
        if self.delay_timer.is_finished():
            ## reset timer incase some other state needs it
            self.delay_timer.reset()
            self.message.set_text_and_wrap("   Lives Remaining: " + str(self.lives) + "            GAMEOVER...       SPACE to start over    ESCAPE to quit...", self.image.get_width()//2)
            self.set_current_state("continue")


    def state_wingame(self):
        """
        This state is entered when the player completes all the levels of the 
        game.
        """
        ## first run through wingame state, do this before 
        ## timer has been started
        if (
                not self.delay_timer.is_timing() and 
                not self.delay_timer.is_finished()
        ):
            self.music.stop()
            self.se.play("game_complete")
            u.saveLocalScore(self.score)
            u.getLocalLeaderboard()
            self.message.set_text_and_wrap("You completed all the levels! GAME COMPLETE!!!      Score: " + str(self.score), self.image.get_width()//2)
            ## now start the timer to counting to some duration
            self.delay_timer.set_duration(7)
            self.delay_timer.reset()
            self.delay_timer.start()
        ## once timer is finished do this 
        if self.delay_timer.is_finished():
            ## reset timer incase some other state needs it
            self.delay_timer.reset()
            self.message.set_text_and_wrap("You completed all the levels! GAME COMPLETE!!!      Score: " + str(self.score) + "                SPACE to start over    ESCAPE to quit...", self.image.get_width()//2)
            self.set_current_state("continue")


    def state_continue(self):
        """
        This state shows the player the previously saved high scores and 
        prompts them to continue.
        """
        if self.keys[pygame.K_SPACE]:
            self.all_levels = lvl.get_levels()
            self.set_level(1)
            self.set_current_state("title")


    def draw(self):
        """
        Calls all objects to draw their image then uses the images to draw 
        the game image.
        """
        for block in self.level.get_blocks():
            block.draw()
        self.ball.draw()
        self.paddle.draw()
        self.hud.draw()
        self.image.fill((0,0,0))
        ## grab level background and scale to display size, then blit
        self.image.blit(
            pygame.transform.scale(
                self.level.get_background(), 
                self.image.get_size()
            ),
            (0, 0)
        )
        for block in self.level.get_blocks():
            self.image.blit(
                block.image,
                block.get_xypos()
            )
        
        self.image.blit(
            self.ball.image, 
            self.ball.get_draw_rect(),
        )
        self.image.blit(
            self.paddle.image, 
            self.paddle.get_xypos(),
        )
        self.image.blit(
            self.hud.image, 
            (0, 0),
        )
        ## draw message image instead if in title state
        message_states = ["title", "lostball", "levelcomplete", "gameover", "continue", "wingame"]
        self.message.draw()
        if self.get_current_state() in message_states:
            self.image.blit(
                self.message.image,
                (0, 0)
            )
    
    
    def set_level(self, level_id):
        """
        Changes the current level to another level by the given id.
        
        param: integer, a unique level id number.
        """
        ## all_levels is indexed starting at zero, levels are
        ## stored in order
        assert (level_id  > 0), "level_id must be greater than 0, " + str(level_id) + " given"
        self.level = self.all_levels[level_id - 1]
        self.hud.set_level_val(self.level.get_id())
        self.alive_blocks = len(self.level.get_blocks())
        self.music.set_playlist(self.level.get_soundtrack())
        self.music.restart_playlist()

    
    def load_se(self):
        """
        Loads all sound effects into the sound effect player.
        """
        self.se.add_sound("block_explode", "assets/se/block_explode.ogg")
        self.se.add_sound("lose_ball", "assets/se/lose_ball.ogg")
        self.se.add_sound("lose_ball_final", "assets/se/lose_final_ball.ogg")
        self.se.add_sound("paddle_wall_collide", "assets/se/paddle_wall_collide.ogg")
        self.se.add_sound("game_over", "assets/jingles/game_over.ogg")
        self.se.add_sound("level_complete", "assets/jingles/level_complete.ogg")
        self.se.add_sound("game_complete", "assets/jingles/game_complete.ogg")
    
    
    def update(self, time_passed):
        """
        Runs updates depending on the current state of the game.
        """
        self.delay_timer.update(time_passed)
        self.ball.update(time_passed)
        self.paddle.update(time_passed)
        self.music.update()
        if self.get_current_state() == "title":
            self.state_title()
        elif self.get_current_state() == "launch":
            self.state_launch()
        elif self.get_current_state() == "inplay":
            self.state_inplay()
        elif self.get_current_state() == "lostball":
            self.state_lostball()
        elif self.get_current_state() == "levelcomplete":
            self.state_levelcomplete()
        elif self.get_current_state() == "gameover":
            self.state_gameover()
        elif self.get_current_state() == "continue":
            self.state_continue()
        elif self.get_current_state() == "wingame":
            self.state_wingame()


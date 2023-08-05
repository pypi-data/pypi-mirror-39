#! /usr/bin/env python
# coding: utf-8


"""
util.py - Useful functions for game objects.
"""


from __future__ import division, print_function
import math
import pygame
import os
import sqlite3


WHITE = pygame.color.THECOLORS['white']

SQLITEFILE = "scores.sqlite"


def angle_to_vector(ang):
    """
    Returns a vector that represents the direction of a given angle.
    
    param: ang, an angle in radians.
    
    return: a list, the movement vector for the angle.
    """
    return [math.cos(ang), math.sin(ang)]


def distance(p, q):
    """
    Returns the distance between two points
    
    param: p, an iterable with an x and y value.
    
    param: q, an iterable with an x and y value.
    
    return: a float, the distance from p to q.
    """
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def get_fitted_text_on_surface(text, x_wrap, font, color=WHITE):
    """
    Returns a surface with the given text blitted to it.
    
    param: text, some text to write.
    
    param: x_wrap, the x distance to write until the text wraps to 
        a new line.
    
    param: font, a pygame.freetype.Font instance.
    
    param: color, the color the text will be.
    
    return: pygame surface, a surface of the given width containg the 
        given text.
    """
    ## print from bottom-left origin instead of upper-left
    font.origin = True
    words = text.split(" ")
    word_spacing = font.get_rect("  ")
    row_height = font.get_sized_height()
    surface = pygame.Surface(
        (x_wrap, row_height),
        pygame.SRCALPHA
    )
    surface.fill((0,0,0,0))
    max_width, max_height = surface.get_size()
    ## contain text inside of text area
    x, y = 0, row_height
    for word in words:
        word_box = font.get_rect(word)
        if (x + word_box.width + word_box.x) > max_width:
            x, y = 0, y + row_height
        if (y + word_box.height - word_box.y) > max_height:
            ## resize the height to accomodate text
            new_height = max_height + row_height
            temp_surface = pygame.Surface(
                (max_width, new_height), 
                pygame.SRCALPHA
            )
            temp_surface.fill((0,0,0,0))
            max_height = new_height
            temp_surface.blit(surface, (0, 0))
            surface = temp_surface.copy()
        font.render_to(surface, (x, y), None, color)
        x += (word_box.width + word_spacing.width)
    return surface 


def ensureSQLite():
    alreadyExisted = True
    
    if not os.path.isfile(SQLITEFILE):
        alreadyExisted = False
        highScore_table = "scores"
        player_attribute = "player"
        playerType = "text"
        score_attribute = "score"
        scoreType = "INTEGER"
        
        conn = sqlite3.connect(SQLITEFILE)
        
        c = conn.cursor()
        
        c.execute('CREATE TABLE {t} ({f1} {ty1}, {f2} {ty2})'\
                  .format(t=highScore_table, f1=player_attribute, ty1=playerType, f2=score_attribute, ty2=scoreType))
        
        conn.commit()
        conn.close()
        
    return alreadyExisted
        
        
def saveLocalScore(playerScore, player = "player"):
    ensureSQLite()
            
    conn = sqlite3.connect(SQLITEFILE)
    
    insert = conn.cursor()
    
    insert.execute("INSERT INTO scores(player, score) VALUES (?,?)", (player, playerScore,))
    
    conn.commit()
    conn.close()        
    
    
def getLocalLeaderboard():
    ensureSQLite()
    
    conn = sqlite3.connect(SQLITEFILE)
    
    selectTopScores = conn.cursor()
    
    selectTopScores.execute("SELECT * FROM scores order by score desc LIMIT 5")
    
    rows = selectTopScores.fetchall()
    
    topFive = []
    
    for row in rows:
        topFive.append({"player": row[0], "score": row[1]})
        
    return topFive

def getLocalHighScore():
    ensureSQLite()
    
    conn = sqlite3.connect(SQLITEFILE)
    
    getHighScore = conn.cursor()
    
    getHighScore.execute("SELECT * FROM scores order by score desc LIMIT 1")
    
    highScore = getHighScore.fetchone()[1]
    
    return highScore

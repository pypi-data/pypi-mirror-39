#! /usr/bin/env python
# coding: utf-8


"""
object_definitions.py - Holds info about game assets.
"""


from __future__ import division, print_function


beach_ball = {
    "texture" : "assets/sprites/ball.gif",
    "size" : (25, 25),
}


blue_paddle = {
    "texture" : "assets/sprites/bluepaddle.png",
    "size" : (96, 8),
}


level_1 = {
    "id" : 1,
    "name" : "Sunset in the Swamp",
    "background" : "assets/level_0/background.png",
    "soundtrack" : [
        ("assets/level_0/soundtrack_intro.ogg", 1, None),
        ("assets/level_0/soundtrack.ogg", 0, None),
    ],
    "block_size" : (32, 32),
    "block_layout" : [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "  rrr  rrr  rrr  rrr  rrr  rrr  ",
        "  yyy  yyy  yyy  yyy  yyy  yyy  ",
        "  ggg  ggg  ggg  ggg  ggg  ggg  ",
        "  bbb  bbb  bbb  bbb  bbb  bbb  ",
        "  rrr  rrr  rrr  rrr  rrr  rrr  ",
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
    ],
}


level_2 = {
    "id" : 2,
    "name" : "Clouds in the Desert",
    "background" : "assets/level_1/background.png",
    "soundtrack" : [
        ("assets/level_1/soundtrack.ogg", 0, None),
    ],
    "block_size" : (32, 32),
    "block_layout" : [
        "                                ",
        "                                ",
        "                                ",
        "bg             r             gb ",
        " bg           rrr           gb  ",
        "  bg         gbrbg         gb   ",
        "   bg       gb y bg       gb    ",
        "    bgggggggb  y  bgggggggb     ",
        "     bbbbbbb   y   bbbbbbb      ",
        "         bb    y    bb          ",
        "        bb     y     bb         ",
        "       bb      y      bb        ",
        "      bb       y       bb       ",
        "     bb        y        bb      ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
}


level_3 = {
    "id" : 3,
    "name" : "Wizard's Tower",
    "background" : "assets/level_2/background.png",
    "soundtrack" : [
        ("assets/level_2/soundtrack.ogg", 0, None),
    ],
    "block_size" : (32, 32),
    "block_layout" : [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "   rryyggbbggyyrryyggbbggyyrr   ",
        "    y                      y    ",
        "     rryyggbbggyyggbbggyyrr     ",
        "      y                  y      ",
        "       rryyggbbggbbggyyrr       ",
        "        y              y        ",
        "         rryygbbbbgyyrr         ",
        "    b     y          y     b    ",
        "    g      rrygbbgyrr      g    ",
        "    y       y      y       y    ",
        "   yry       rryyrr       yry   ",
        "    y         y  y         y    ",
        "               rr               ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
}


level_4 = {
    "id" : 4,
    "name" : "Space Force!...ATTACK!",
    "background" : "assets/level_3/background.png",
    "soundtrack" : [
        ("assets/level_3/soundtrack_intro.ogg", 1, 2100), 
        ("assets/level_3/soundtrack.ogg", 0, None)
    ],
    "block_size" : (32, 32),
    "block_layout" : [
        "                                ",
        "                                ",
        "                                ",
        "   yrrry  yrrry  yrrry  yrrry   ",
        "    yry    yry    yry    yry    ",
        "     y      y      y      y     ",
        "                                ",
        "                                ",
        "   gyyyg  gyyyg  gyyyg  gyyyg   ",
        "    gyg    gyg    gyg    gyg    ",
        "     g      g      g      g     ",
        "                                ",
        "                                ",
        "   bgggb  bgggb  bgggb  bgggb   ",
        "    bgb    bgb    bgb    bgb    ",
        "     b      b      b      b     ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
}

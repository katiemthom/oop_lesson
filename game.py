##uh

import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
    SLIDE = False

    def next_pos(self, direction):
        if direction == "up": 
            return (self.x, self.y - 1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x - 1, self.y)
        elif direction == "right":
            return (self.x + 1, self.y)
        return None

class Character(GameElement): 
    IMAGE = "Girl"

    def __init__(self): 
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up": 
            return (self.x, self.y - 1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x - 1, self.y)
        elif direction == "right":
            return (self.x + 1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    SLIDE = False

    def interact(self, player): 
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d itemss!" % (len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    SLIDE = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d items!" % (len(player.inventory)))
####   End class definitions    ####

def keyboard_handler(): 
    direction = None

    if KEYBOARD[key.UP]: 
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]: 
        direction = "left"
    if KEYBOARD[key.RIGHT]: 
        direction = "right"

    if direction: 
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x > GAME_WIDTH - 1 or next_y > GAME_HEIGHT - 1: 
            GAME_BOARD.draw_msg("Can't go there!")

        else: 
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                if existing_el.SLIDE: 
                    next_location_slide = existing_el.next_pos(direction)
                    next_x_slide = next_location_slide[0]
                    next_y_slide = next_location_slide[1]
                    barrier = GAME_BOARD.get_el(next_x_slide, next_y_slide)
                    if barrier is None: 
                        GAME_BOARD.del_el(existing_el.x, existing_el.y)
                        GAME_BOARD.set_el(next_x_slide, next_y_slide, existing_el)
                    else: 
                        GAME_BOARD.draw_msg("Something in the way!")
                else: 
                    existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID: 
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

def initialize():
    """Put game initialization code here"""

    rock_positions = [
    	(2, 1),
    	(1, 2),
    	(3, 2), 
    	(2, 3)
    ]

    rocks = []

    for pos in rock_positions: 
    	rock = Rock()
    	GAME_BOARD.register(rock)
    	GAME_BOARD.set_el(pos[0], pos[1], rock)
    	rocks.append(rock)

    rocks[-1].SLIDE = True
    rocks[-1].SOLID = False

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(1, 5, key)
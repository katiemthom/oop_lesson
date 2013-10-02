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

class Light_Rock(Rock): 

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

    def interact(self, player): 
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d itemss!" % (len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d items!" % (len(player.inventory)))
####   End class definitions    ####

def keyboard_handler(): 
    direction = None
    moving = True 

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

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el.__class__ is Rock:
            if existing_el.__class__ is Light_Rock:
                if is_blocked(existing_el):
                    moving = "Something in the way!"
            else: 
                moving = "Oww!"

        if next_x > GAME_WIDTH - 1 or next_y > GAME_HEIGHT - 1: 
            moving = "Can't go there!"

        if moving != True: 
            GAME_BOARD.draw_msg(moving)
        else: 
            if existing_el.__class__ is Light_Rock: 
                next_location_slide = existing_el.next_pos(direction)
                next_x_slide = next_location_slide[0]
                next_y_slide = next_location_slide[1]
                move_object(next_x_slide, next_y_slide, existing_el)
            if existing_el != None and existing_el.__class__ is not Rock:
                existing_el.interact(PLAYER)
            move_object(next_x, next_y,PLAYER)



        #set moving to true or falso

        

        #else: 
            #existing_el = GAME_BOARD.get_el(next_x, next_y)
        

            # if we're going to move
                # if there is a rock that can slide and has a clear path (exiting_el is a slidable rock that is unblocked) 
                # if there is an item and we pick it up "interact" (existing_el is not Rock)
                # if it's clear (existing_el is None)
                # move
            # else 
                # check if there is a rock that can slide and there is something in the way (existing_el is a slideable rock that is blocked)
                # check there is a rock that can't slide (existing el is an unslideable rock)
                # check or if we're going to walk off the game board  (next x or next y is off the board)
                # nested if's w/ messages 

            """
            if existing_el.__class__ is Light_Rock:
                next_location_slide = existing_el.next_pos(direction)
                next_x_slide = next_location_slide[0]
                next_y_slide = next_location_slide[1]
                barrier = GAME_BOARD.get_el(next_x_slide, next_y_slide)
                if barrier is None: 
                    move_object(next_x_slide, next_y_slide, existing_el)
                    move_object(next_x, next_y,PLAYER)
                else: 
                    GAME_BOARD.draw_msg("Something in the way!") 
            else: 
                    GAME_BOARD.draw_msg("Oww!")

            elif existing_el: 
                #pick up an item
                existing_el.interact(PLAYER)
                move_object(next_x, next_y,PLAYER)
            else: 
                #or just move
                move_object(next_x, next_y,PLAYER)
                """

def is_blocked(obj): 
    next_location = obj.next_pos(direction)
    next_x = next_location[0]
    next_y = next_location[1]
    barrier = GAME_BOARD.get_el(next_x, next_y)
    if barrier is None:
        return False
    else: 
        return True

def move_object(to_x, to_y, obj): 
    GAME_BOARD.del_el(obj.x, obj.y)
    GAME_BOARD.set_el(to_x, to_y, obj)

def initialize():
    """Put game initialization code here"""

    rock_positions = [
    	(2, 1),
    	(1, 2),
    	(3, 2), 
    ]

    rocks = []

    for pos in rock_positions: 
    	rock = Rock()
    	GAME_BOARD.register(rock)
    	GAME_BOARD.set_el(pos[0], pos[1], rock)
    	rocks.append(rock)

    light_rock = Light_Rock()
    GAME_BOARD.register(light_rock)
    GAME_BOARD.set_el(2, 3, light_rock)

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
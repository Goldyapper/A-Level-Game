#########################################################################################
                                     ###imports###
#########################################################################################

import pygame # imports pyton modules
from pygame.locals import * # imports local variables from pygame
pygame.init() #initiates pygame

#########################################################################################
                                     ###Variables###
#########################################################################################

moving_left =False
moving_right =False
vertical_momentum = 0#height off the ground variable
air_timer = 0#time in air

#########################################################################################
                                     ###Functions###
#########################################################################################

def collision_test(rect,tiles):# function to see if the player is clliding with and tiles 
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):# if the rect is touching the player
            hit_list.append(tile)#add the tile to the hit list
    return hit_list#returns all the tiles colliding with the player

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}#seting the moveent variables
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

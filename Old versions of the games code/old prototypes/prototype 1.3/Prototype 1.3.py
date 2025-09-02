import pygame, sys
import keyboard

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() #initiates pygame

#For the window

pygame.display.set_caption ('first prototype')#naming the window of the game

Window_Size =(600,400)# pixel size for the window

screen = pygame.display.set_mode(Window_Size,0,32)#initiates the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled


game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],#game map 0= air, 1=railx, 2=floor
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

floor_img = pygame.image.load('floor.png')#load the floor image into a variable
floor_img.set_colorkey((255,255,255))
rail_img = pygame.image.load('rails.png')#load the rails image into a variable
rail_img.set_colorkey((255,255,255))

while True: #game loop
    display.fill((146,244,225))#fill screen with one colour

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(rail_img,(x*16,y*16))#draw the rail if 1 and time by the pixel size
            if tile == '2':
                display.blit(floor_img,(x*16,y*16))#draw the floor if 2 and time by the pixel size
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))#if the tile is not air the rect will be added to the tile_rect variable
            x += 1
        y += 1


    screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
    pygame.display.update()#updates everthing on screen
    clock.tick(60)#frame rate 60fps

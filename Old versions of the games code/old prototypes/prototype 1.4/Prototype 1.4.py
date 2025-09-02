import pygame, sys # imports pyton modules
import keyboard
from pygame.locals import * # imports local variables from pygame
pygame.init() #initiates pygame

#For the window

pygame.display.set_caption ('first prototype')#naming the window of the game
Window_Size =(600,600)# pixel size for the window
screen = pygame.display.set_mode(Window_Size,0,32)#initiates the window
display = pygame.Surface((300,300)) # used as the surface for rendering, which is scaled
clock = pygame.time.Clock()

def load_map(path):
    f = open(path + '.txt','r')#opens file
    data = f.read()#reads file
    f.close()#closes file
    data = data.split('\n')#splits the data into different lines
    game_map = []
    for row in data:#reads each line 
        game_map.append(list(row))#makes a list for each line
    return game_map

game_map=load_map('map_1-2')#reads the file for the map

#different tiles for the map, add to this if i want to add more tiles part 1
Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
entrance_img = pygame.image.load('entrance.png')#load the filename image into a variable
entrance_img.set_colorkey((255,255,255))#white pixels of the player are transparent
exit_img = pygame.image.load('exit.png')#load the filename image into a variable
exit_img.set_colorkey((255,255,255))#white pixels of the player are transparent
big_block_img = pygame.image.load('big_block.png')#load the filename image into a variable
big_block_img.set_colorkey((255,255,255))#white pixels of the player are transparent

#background objects
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]# first number is times by how far the camera has moved to make the effect that objects are moving in the background, rest of the numbers are the bas data for the objects


while True: #game loop
    display.fill((0,225,225))#fill screen with one colour

    pygame.draw.rect(display,(0,100,0),pygame.Rect(0,120,300,80))#draws a green background taking up half the screen
    for background_object in background_objects:#goes through the background_objects list
        obj_rect = pygame.Rect(background_object[1][0],background_object[1][1],background_object[1][2],background_object[1][3])#the objects move slower in realtive to the first nummber in the background object data
        if background_object[0] == 0.5:#if the multiply is .5
            pygame.draw.rect(display,(34,139,34),obj_rect)#the colour will be a litter green
        else:
            pygame.draw.rect(display,(0,128,128),obj_rect)#if not the colour will be blue

    
    tile_rects = []#different tiles for the map, add to this if i want to add more tiles part 2
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(Platform_img,(x*16,y*16))#draw the platform if 1 and times by the pixel size
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the platforms hit box, the second pair being how big the hitbox is
            if tile == '2':
                display.blit(entrance_img,(x*16,y*15))#draw the entrance if 2 and times by the pixel size 
            if tile == '3':
                display.blit(exit_img,(x*16,y*15))#draw the exit if 3 and times by the pixel size 
            if tile == '4':
                display.blit(big_block_img,(x*16,y*16))#draw the big block if 4 and times by the pixel size
                tile_rects.append(pygame.Rect(x*16,y*16,32,32))#the blocks hit box, the second pair being how big the hitbox is
            x += 1
        y += 1


    screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
    pygame.display.update()#updates everthing on screen
    clock.tick(60)#frame rate 60fps

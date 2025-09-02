import pygame, sys # imports pyton modules
import keyboard
from pygame.locals import * # imports local variables from pygame
pygame.init() #initiates pygame

from movement_code_1 import *

clock = pygame.time.Clock()

#For the window

pygame.display.set_caption ('first prototype')#naming the window of the game
Window_Size =(800,800)# pixel size for the window
screen = pygame.display.set_mode(Window_Size,0,32)#initiates the window
display = pygame.Surface((400,400)) # used as the surface for rendering, which is scaled


true_scroll = [0,0]#sets the variable for how much the camera has moved

def load_map(path):
    f = open(path + '.txt','r')#opens file
    data = f.read()#reads file
    f.close()#closes file
    data = data.split('\n')#splits the data into different lines
    game_map = []
    for row in data:#reads each line 
        game_map.append(list(row))#makes a list for each line
    return game_map

game_map=load_map('map_1.1')#reads the file for the map


#different tiles for the map, add to this if i want to add more tiles part 1
Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
entrance_bottom_img = pygame.image.load('entrance_bottom.png')#load the filename image into a variable
entrance_bottom_img.set_colorkey((255,255,255))#white pixels of the player are transparent
entrance_top_img = pygame.image.load('entrance_top.png')#load the filename image into a variable
entrance_top_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent
#Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
#Platform_img.set_colorkey((255,255,255))#white pixels of the player are transparent

#player images

player_img = pygame.image.load('player.png').convert()#load the player image
player_img.set_colorkey((255,255,255))#white pixels of the player are transparent
player_rect = pygame.Rect(100,100,16,24)#player's hit box 

#background objects
background_objects = [[0.25,[60,10,70,400]],[0.25,[280,15,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]# first number is times by how far the camera has moved to make the effect that objects are moving in the background, rest of the numbers are the base data for the objects(first tow numbers are x and y position the second two are height and width)

while True: #game loop
    display.fill((0,225,225))#fill screen with one colour

    #camera movemt
    true_scroll[0] += (player_rect.x-true_scroll[0]-208)/20#x-axis camera movement, the -152 is so it is at the centre of the screen, the /20 is for smoth camera movement
    true_scroll[1] += (player_rect.y-true_scroll[1]-192)/20#y-axis camera movement, the -112 is so it is at the centre of the screen, the /20 is for smoth camera movement
    scroll = true_scroll.copy()#changes scroll value into intergs for smooth moevement for the tiles
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(0,100,0),pygame.Rect(50,120,200,400))#draws a green background taking up half the screen
    for background_object in background_objects:#goes through the background_objects list
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])#the objects move slower in realtive to the first nummber in the background object data
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
                display.blit(Platform_img,(x*16,y*16))#draw the platform if 1 and times by the pixel size and the scroll is for camera movement 
            if tile == '2':
                display.blit(entrance_bottom_img,(x*16,y*16))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            if tile == '3':
                display.blit(entrance_top_img,(x*16,y*16))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '4':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '5':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '6':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '7':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '8':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            #if tile == '9':
            #    display.blit(Platform_img,(x*16-scroll[0],y*16-scroll[1]))#draw the rail if 1 and times by the pixel size and the scroll is for camera movement 
            if tile != '0':
                 if tile != '2':
                     if tile != '3':
                         tile_rects.append(pygame.Rect(x*16,y*16,16,16))#if the tile is not air the rect will be added to the tile_rect variable
            x += 1
        y += 1

#movement
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
        
    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1


    #display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    display.blit(player_img,(player_rect.x,player_rect.y))
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:#when a key is pressed once
            if event.key == ord('d'):#if the d key is pressed
                moving_right = True
            if event.key == ord('a'): #if the a key is pressed
                moving_left = True
            if event.key == K_RIGHT: #if the right key is pressed
                moving_right = True
            if event.key == K_LEFT: #if the left key is pressed
                moving_left = True
            if event.key == ord('w'):#if the w key is pressed
                if air_timer < 6:#only jump when on the ground
                    vertical_momentum = -5
            if event.key == K_UP:#if the up key is pressed
                if air_timer < 6:#only jump when on the ground
                    vertical_momentum = -5
        if event.type == KEYUP:#when a key is stop being pressed
            if event.key == ord('d'):
                moving_right = False
            if event.key == ord('a'):
                moving_left = False
            if event.key == K_RIGHT: 
                moving_right = False
            if event.key == K_LEFT: 
                moving_left = False

    screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
    pygame.display.update()#updates everthing on screen
    clock.tick(60)#frame rate 60fps

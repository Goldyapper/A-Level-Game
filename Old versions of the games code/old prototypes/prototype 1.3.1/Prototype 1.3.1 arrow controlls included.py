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

#movement part 1 variables for movement  
moving_left =False
moving_right =False
vertical_momentum = 0
air_timer = 0#time in air

game_map = [['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','2','0','0','0','2','2','2','2','0','0','0','0','0','0','1'],
            ['1','0','0','2','1','0','0','0','1','1','1','1','0','0','0','0','0','0','1'],#game map 0= air, 1=rail, 2=floor
            ['1','2','2','1','1','0','0','0','1','1','1','1','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','2','2','2','1','1','1','1','2','2','2','2','2','2','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

floor_img = pygame.image.load('floor.png')#load the floor image into a variable
floor_img.set_colorkey((255,255,255))
rail_img = pygame.image.load('rails.png')#load the rails image into a variable
rail_img.set_colorkey((255,255,255))

player_img = pygame.image.load('player.png').convert()#load the player image
player_img.set_colorkey((255,255,255))#white pixels of the player are transparent

player_rect = pygame.Rect(100,100,16,24)#player's hit box 

def collision_test(rect,tiles):# function to see if the player is clliding with and tiles 
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list#returns all the tiles colliding with the player

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
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
            if event.key == K_LEFT: #if the right key is pressed
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

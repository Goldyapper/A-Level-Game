import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() #initiates pygame

#For the window

pygame.display.set_caption ('first prototype')#naming the window of the game

Window_Size =(400,400)# pixel size for the window

screen = pygame.display.set_mode (Window_Size,0,32)#initiates the window

#Player image

player_image = pygame.image.load('player.png')#loads an image from the folder and calls it player image

#variables for movement
moving_left =False
moving_right =False

player_location = [50,50]#spawn location
player_y_momentum = 0

player_rect= pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())#the collison for the player
test_rect = pygame .Rect (100,100,100,50)#collision test


while True: #game loop
    screen.fill((0,0,225))#fill screen with one colour
    screen.blit(player_image,player_location)#renders image at player location on screen

    if player_location[1] >Window_Size[1]-player_image.get_height():#test if the bottom of player image is at the bottom of the screen
        player_y_momentum = -player_y_momentum#bounce back up
    else:
        player_y_momentum += 0.2# falling momentum
    player_location[1] += player_y_momentum

    #player movement left and reight
    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    #collison rectangle for the player
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    #player collison
    if player_rect.colliderect(test_rect):#test if player is toucing the test collion
        pygame.draw.rect(screen,(225,0,0),test_rect)#if touching the object turns red
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)#if touching the object turns black

    for event in pygame.event.get(): #for an key press
        if event.type == QUIT:#closing the game
            pygame.quit()
            sys.exit

        #assigning keys to movement
        if event.type == KEYDOWN:#when a key is pressed once
            if event.key == K_RIGHT: #if the right key is pressed
                moving_right = True
            if event.key == K_LEFT: #if the right key is pressed
                moving_left = True
        if event.type == KEYUP:#when a key is stop being pressed
            if event.key == K_RIGHT: 
                moving_right = False
            if event.key == K_LEFT: 
                moving_left = False
        

    pygame.display.update()#updates everthing on screen
    clock.tick(60)#frame rate 60fps

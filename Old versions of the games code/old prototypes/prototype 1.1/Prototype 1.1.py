import pygame, sys

clock = pygame.time.Clock()#

from pygame.locals import *
pygame.init() #initiates pygame

pygame.display.set_caption ('first prototype')#naming the window of the game

Window_Size =(400,400)# pixel size for the window

screen = pygame.display.set_mode (Window_Size,0,32)#initiates the window

player_image = pygame.image.load('player.png')#loads an image from the folder and calls it player image

while True: #game loop

    screen.blit(player_image,(50,50))#renders image at 50 by 50 pixels on screen
        
    for event in pygame.event.get(): #for an key press
        if event.type == QUIT:#closing the game
            pygame.quit()
            sys.exit

    pygame.display.update()
    clock.tick(60)#frame rate 60fps

#########################################################################################
                                     ###imports###
#########################################################################################

import pygame, sys # imports pyton modules
from pygame.locals import * # imports local variables from pygame

pygame.init() #initiates pygame

#########################################################################################
                                     ###Variables###
#########################################################################################

Screen_width = 640  #screen will be 20 tiles wide
Screen_height = 640 #screen will be 20 tiles high

### Game Variables ###

tile_size = 32 #size of each tile 

#########################################################################################
                                     ###Opening the screen###
#########################################################################################

Screen = pygame.display.set_mode((Screen_width, Screen_height))#creates a pygmae display the size of screen width*screen height
pygame.display.set_caption('Untitled Platformer')#names the screen in the top left

#########################################################################################
                                     ###Classes###
#########################################################################################

class World(): #code for world

    def __init__(self,data): #init takes a self and data argument
        self.tile_list = []#creates a list to store the tiles

        ###load images###
        Platform_img = pygame.image.load('images/Platform.png')#load the filename image into a variable
        spikes_img = pygame.image.load('images/spikes.png')

        y = 0 #y co-ords
        for layer in data:
            x = 0 # x co-ords
            for tile in layer:
                if tile == 1:
                    img = pygame.transform.scale(Platform_img,(tile_size,tile_size))#scales all images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list
                if tile == 2:
                    img = pygame.transform.scale(spikes_img,(tile_size,tile_size))#scales all images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list

                x += 1 #moves to the next tile 
            y += 1 #moves to the layer
                
    def draw(self): #functions to draw the tiles
        for tile in self.tile_list: #every tile in the list
            Screen.blit(tile [0],tile[1]) #display the tiles
            
            




#########################################################################################
                                     ###Misc stuff###
#########################################################################################

world_map = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],   
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], #data for the world map
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],  
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], #0 for air, 1 for black ptalforms
[1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],   
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], 
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


world = World(world_map)

#########################################################################################
                                     ###Game loop###
#########################################################################################


run = True
while run:
    
    Screen.fill((0,225,225))#fill screen with one colour
    
    world.draw()
    
    for event in pygame.event.get(): #event loop
        if event.type == pygame.QUIT: #when the exit button  is clicked
            run = False #stop game loop
    
    pygame.display.update()#draws everything on to the screen 
    
pygame.quit()#exits pygame

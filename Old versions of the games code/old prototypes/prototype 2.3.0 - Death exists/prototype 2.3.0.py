#########################################################################################
                                     ###imports###
#########################################################################################

import pygame, sys # imports pyton modules
from pygame.locals import * # imports local variables from pygame

pygame.init() #initiates pygame

#########################################################################################
                                     ###Variables###
#########################################################################################

###Screen Variables###

clock = pygame.time.Clock()#used for capping clock ticks
fps = 60#60 frames per second

Screen_width = 640   #screen will be 20 tiles wide
Screen_height = 640 #screen will be 20 tiles high

### Game Variables ###

tile_size = 32 #size of each tile 
game_over = 0 #game over variable

#########################################################################################
                                     ###Opening the screen###
#########################################################################################

Screen = pygame.display.set_mode((Screen_width, Screen_height))#creates a pygmae display the size of screen width*screen height
pygame.display.set_caption('Untitled Platformer')#names the screen in the top left

#########################################################################################
                                     ###Classes###
#########################################################################################

class Player(): #code for player
    def __init__(self,x,y):#takes arguement self,x coords, y coords
        img = pygame.image.load('images/player.png')#opens image from images folder
        img.set_colorkey((255,255,255))#white pixels of the file are transparent
        dead_img = pygame.image.load('images/dead_player.png')#opens image from images folder
        dead_img.set_colorkey((255,255,255))#white pixels of the file are transparent
        self.dead_image = pygame.transform.scale(dead_img,(48,72))#scales image to be 48 pixels by 72 pixels
        self.image = pygame.transform.scale(img,(48,72))#scales image to be 48 pixels by 72 pixels
        self.rect = self.image.get_rect()#takes a rect from the image
        self.rect.x = x#sets the rects x coords
        self.rect.y = y#sets the rects y coords
        self.vel_y = 0#sets gravity speed to 0
        self.width = self.image.get_width()#gets the width of the player
        self.height = self.image.get_height()#get the height of the player
        self.jumped = False #player has jumped = no

    def update(self,game_over):#updates player

        ###Variables for this function###
        dx = 0#dx and dy are used to see if there is going to be a colliision when the player moves 
        dy = 0

        if game_over == 0:#only happens if game_over = 0

            key = pygame.key.get_pressed()#key presses


            ###Reading key Presses and moving###
            if key[K_w] and self.jumped == False:# if the up key is press and the player isn't jumping
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True
            if key[K_UP] and self.jumped == False:# if the up key is press and the player isn't jumping
                self.vel_y = - 10 #Moves player up by 15
                self.jumped = True
            if key[K_UP] or key[K_w]== False:#if up isn't being pressed
                self.jumped = False#self.jumped isn't true
            



            if key[pygame.K_LEFT] or key[pygame.K_a]:#if left key is pressed
                dx -= 5# moves player left by 5 pixels
            if key[pygame.K_RIGHT] or key[pygame.K_d]:#if right key is pressed
                dx += 5# moves player left by 5 pixels

        
            ###Gravity###
            self.vel_y += 1#falls by 1 every iteration
            if self.vel_y > 10:#stops the player falling faster than 10
                self.vel_y = 10
            dy += self.vel_y


            ###collision detection with tiles###
            for tile in world.tile_list:
            
                if tile[1].colliderect(self.rect.x +dx,self.rect.y,self.width,self.height):#if there is collision in the x directions
                   dx = 0 #resets x movemnt to 0

                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):#if there is collision in the y directions
                    if self.vel_y < 0: #if player has jumped
                        dy = tile[1].bottom - self.rect.top#the distance the player will move is the height between the bottom of the tile and the top of the player
                        self.vel_y = 0 #resets y velocity to 0
                    elif self.vel_y >= 0: #if player is landing on the ground
                        dy = tile[1].top - self.rect.bottom#the distance the player will move is the height between the top of the tile and the bottom of the player
                        self.vel_y = 0 #resets y velocity to 0

            ###collision detection with enemies###
            if pygame.sprite.spritecollide(self,spikes_group, False):#if spike sprites collide with the player
                game_over = -1
                
                
            self.rect.x += dx#player moves on the x axis by dx
            self.rect.y += dy#player moves on the right axis by dy

        elif game_over == -1:#if player has died
            self.image = self.dead_image
            
         
        Screen.blit(self.image,self.rect)#display the player image and rect
        pygame.draw.rect(Screen,(255,255,255),self.rect,1)#draws the players hitbox and a pixel wide white box areound it

        return game_over

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
                    spikes =  Spikes(x * tile_size,y * tile_size)#createas a spike instance and positions it at the x and y co-ords
                    spikes_group.add(spikes)#adds spikes tot the spikes group
                x += 1 #moves to the next tile 
            y += 1 #moves to the layer
                
    def draw(self): #functions to draw the tiles
        for tile in self.tile_list: #every tile in the list
            Screen.blit(tile [0],tile[1]) #display the tiles
            pygame.draw.rect(Screen,(0,0,255),tile[1],1)#draws the tiles hitbox and a pixel wide white box areound it



class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/spikes.png')
        img.set_colorkey((255,255,255))#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
            
#########################################################################################
                                     ###Misc stuff###
#########################################################################################

world_map = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],   
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1], 
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],   
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],   
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1], 
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],   
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1], #data for the world map
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],  
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1], #0 for air, 1 for black platlforms
[1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1],
[1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],   
[1,1,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,1,1], 
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

player = Player(100,Screen_height - 136)


spikes_group = pygame.sprite.Group()
world = World(world_map)

#########################################################################################
                                     ###Game loop###
#########################################################################################

run = True
while run:
    
    Screen.fill((0,225,225))#fill screen with one colour
    clock.tick(fps)
    world.draw()
    spikes_group.draw(Screen)
    
    game_over = player.update(game_over)#constantly loops the game_over until the is a colliision with an enemie/obstacle 
    
    for event in pygame.event.get(): #event loop
        if event.type == pygame.QUIT: #when the exit button  is clicked
            run = False #stop game loop
    
    pygame.display.update()#draws everything on to the screen 
    
pygame.quit()#exits pygame

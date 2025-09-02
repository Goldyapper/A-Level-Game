#########################################################################################
                                     ###imports###
#########################################################################################

import pygame, sys # imports pyton modules
from pygame.locals import * # imports local variables from pygame
from os import path# imports path to check if certain files exist
import pickle#import pickle module

pygame.init() #initiates pygame

#########################################################################################
                                     ###Global Variables###
#########################################################################################

###Color Variables###

white = (255,255,255)

###Screen Variables###

clock = pygame.time.Clock()#used for capping clock ticks
fps = 60#60 frames per second

Screen_width = 640   #screen will be 20 tiles wide
Screen_height = 640 #screen will be 20 tiles high


###text variables###

font = pygame.font.SysFont('Arial', 32)

### Game Variables ###

tile_size = 32 #size of each tile 
game_over = 0 #game over variable
max_level = 5 #max level variable
level = 1#level varaible 
Set = 1#set of level variable
SPX = 48 #spawn point on the x-axis
SPY = (Screen_height-32)#spawn point on the y-axis
run = True#Variable used for game loop
coin_count = 0#score variable for how many coins the player collects

###load images###
restart_img = pygame.image.load('images/restart.png')

#########################################################################################
                                     ###Opening the screen###
#########################################################################################

Screen = pygame.display.set_mode((Screen_width, Screen_height))#creates a pygmae display the size of screen width*screen height
pygame.display.set_caption('Untitled Platformer')#names the screen in the top left


#########################################################################################
                                     ###Functions###
#########################################################################################



def draw_text(text,font,colour,x,y):
    img = font.render(text, True, colour)#converts the text into an image with the colour of assignment
    Screen.blit(img, (x,y))#displays picture at co-ords of assignment
    


def reset_level(level):


    player.reset(SPX,SPY)#resets player at those co-ords, AKA their spawn point

    ###clear previous world map###
    exit_group.empty()#empties the exit group
    spikes_group.empty()#empties the exit group
    coin_group.empty()

    ###make new world map###
    if path.exists(f'Maps/Set_{Set}/level{level}_data'):#checks if the level data exists
        pickle_in = open(f'Maps/Set_{Set}/level{level}_data','rb')#f formats the stirng, curly brackets adds the level and set level variable to the stirng
        world_map = pickle.load(pickle_in)#loads data into world_map
    world = World(world_map)#world uses class world and gives it the arguemenr woeld

    return world


#########################################################################################
                                     ###Classes###
#########################################################################################



class Button():#code for buttons
    def __init__(self,x,y,image):
        self.image = image#loads image from the arguements
        self.rect = self.image.get_rect()#gets a rect from the image
        self.rect.x = x#sets the rects x co-ords from the arguements
        self.rect.y = y#sets the rects y co-ords from the arguements
        self.clicked = False#the button hasn't been clicked
        
    def draw(self): #drawing the button
        action = False#action is always false unless button is pressed
        m_pos = pygame.mouse.get_pos()#get mouse position

        if self.rect.collidepoint(m_pos):#if button is colliding with the mouse positon
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:#if left mouse button is clicked and button hasn't been clicked
                action = True#action is due when button is pressd
                self.clicked = True#the button has been presesed
               
        if pygame.mouse.get_pressed()[0] == 0:#if the mouse key has been realeased
            self.clicked = False# button hasn't been clicked

        Screen.blit(self.image,self.rect)#draws button on the screen

        return action# action is returned so that it can be used later



class Player(): #code for player
    def __init__(self,x,y):#takes arguement self,x coords, y coords
        self.reset(x,y)#calls the reset function


    def update(self,game_over):#updates player

        ###Variables for this function###
        dx = 0#dx and dy are used to see if there is going to be a colliision when the player moves 
        dy = 0

        if game_over == 0:#only happens if game_over = 0

            key = pygame.key.get_pressed()#key presses


            ###Reading key Presses and moving###
            if key[K_w] and self.jumped == False and self.in_air == False:# if the W key is press and the player isn't jumping
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True
            if key[K_UP] and self.jumped == False and self.in_air == False:# if the up key is press and the player isn't jumping
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True
            if key[K_SPACE] and self.jumped == False and self.in_air == False:# if the up key is press and the player isn't jumping
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True
            if key[K_UP] or key[K_w] or key[K_SPACE]== False:#if up/W/Space isn't being pressed
                self.jumped = False#self.jumped isn't true


            if key[pygame.K_LEFT] or key[pygame.K_a]:#if left key is pressed
                dx -= 5# moves player left by 5 pixels
            if key[pygame.K_RIGHT] or key[pygame.K_d]:#if right key is pressed
                dx += 5# moves player left by 5 pixels

        
            ###Gravity###
            self.vel_y += 1#falls by 1 every iteration
            if self.vel_y > 10:#stops the player falling faster than 10
                self.vel_y = 10
            dy += self.vel_y#adds gravity to players movement


            ###collision detection with tiles###
            self.in_air = True#player is in the air until proven otherwise
            for tile in world.tile_list:
            
                if tile[1].colliderect(self.rect.x +dx,self.rect.y,self.width,self.height):#if there is collision in the x directions
                   dx = 0 #resets x movemnt to 0

                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):#if there is collision in the y directions
                    if self.vel_y < 0: #if player is below the ground
                        dy = tile[1].bottom - self.rect.top#the distance the player will move is the height between the bottom of the tile and the top of the player
                        self.vel_y = 0 #resets y velocity to 0
                    elif self.vel_y >= 0: #if player is above the ground
                        dy = tile[1].top - self.rect.bottom#the distance the player will move is the height between the top of the tile and the bottom of the player
                        self.vel_y = 0 #resets y velocity to 0
                        self.in_air = False

            ###collision detection with enemies###
            if pygame.sprite.spritecollide(self,spikes_group, False):#if spike sprites collide with the player
                game_over = -1#player has died
                
            if pygame.sprite.spritecollide(self,exit_group, False):#if exit sprites collide with the player
                game_over = 1#player has won

            self.rect.x += dx#player moves on the x axis by dx
            self.rect.y += dy#player moves on the right axis by dy

        elif game_over == -1:#if player has died
            self.image = self.dead_image
            
         
        Screen.blit(self.image,self.rect)#display the player image and rect

        return game_over

    def reset(self,x,y):#reset function for when player is spawned/dies
        img = pygame.image.load('images/player.png')#opens image from images folder
        img.set_colorkey(white)#white pixels of the file are transparent
        dead_img = pygame.image.load('images/dead_player.png')#opens image from images folder
        dead_img.set_colorkey(white)#white pixels of the file are transparent
        self.dead_image = pygame.transform.scale(dead_img,(48,72))#scales image to be 48 pixels by 72 pixels
        self.image = pygame.transform.scale(img,(48,72))#scales image to be 48 pixels by 72 pixels
        self.rect = self.image.get_rect()#takes a rect from the image
        self.rect.x = x#sets the rects x coords
        self.rect.y = y#sets the rects y coords
        self.vel_y = 0#sets gravity speed to 0
        self.width = self.image.get_width()#gets the width of the player
        self.height = self.image.get_height()#get the height of the player
        self.jumped = False #player has jumped = no
        self.in_air = True #assumes player is in the air



class World(): #code for world

    def __init__(self,data): #init takes a self and data argument
        self.tile_list = []#creates a list to store the tiles

        ###load images###
        Platform_img = pygame.image.load('images/Platform.png')#load the filename image into a variable
        boundary_img = pygame.image.load('images/Boundary.png')#load the filename image into a variable

        ###oop that reads map and decides whata to display###
        y = 0 #y co-ords
        for layer in data:
            x = 0 # x co-ords
            for tile in layer:
                #######check before writing in nea######

                #tile 1 = boundary
                #tile 2 = platform
                #tile 3 = spikes
                #tile 4 = exit
                #tile 5 = coin

                if tile == 1:
                    img = pygame.transform.scale(boundary_img,(tile_size,tile_size))#scales all images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list
                if tile == 2:
                    img = pygame.transform.scale(Platform_img,(tile_size,tile_size))#scales all images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list
                if tile == 3:#change to 3 in the future
                    spikes =  Spikes(x * tile_size,y * tile_size)#createas a spike instance and positions it at the x and y co-ords
                    spikes_group.add(spikes)#adds spikes tot the spikes group
                if tile == 4:
                    exit = Exit(x * tile_size,y * tile_size - (tile_size))#createas a exit instance and positions it at the x and y co-ords
                    exit_group.add(exit)#adds exit to the exit group
                if tile == 5:
                    coin = Coin(x * tile_size + (tile_size // 2),y * tile_size + (tile_size // 2))#createas a spike instance and positions it at the x and y co-ords
                    coin_group.add(coin)#adds coin to the coin group
                x += 1 #moves to the next tile 
            y += 1 #moves to the layer
                
    def draw(self): #functions to draw the tiles
        for tile in self.tile_list: #every tile in the list
            Screen.blit(tile [0],tile[1]) #display the tiles
            pygame.draw.rect(Screen,(0,0,0),tile[1],1)#draws the tiles hitbox and a pixel wide white box areound it


###Spikes class###
class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/spikes.png')#loads the spikes image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))#scales image to be the size of a tile
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement 

###Exit class###
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/exit.png')#loads the exit image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 2)))#scales image to be a tile wide and 2 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement

###Coin class###
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Coin.png')#loads the exit image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size //2, tile_size //2))#scales image to be a tile wide and 2 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.center = (x,y)#sets the x co-ords of the rect from the arguement to the mid-point of the rect 
        
            
#########################################################################################
                                     ###Misc stuff###
#########################################################################################

###spawn point assignment###
player = Player(SPX,SPY)#creates a player instance at those co=ords, AKA their spawn point

###Sprite group stuff###
spikes_group = pygame.sprite.Group()#creates the spikes group
coin_group = pygame.sprite.Group()#creats the coin group
exit_group = pygame.sprite.Group()#creats the exit group

#score_coin = Coin(tile_size//2,tile_size//2)#assigns a coin to the top left corn for the score counter
#coin_group.add(score_coin)

###Check if the files containing the maps exist###
if path.exists(f'Maps/Set_{Set}/level{level}_data'):#checks if the level data exists
    pickle_in = open(f'Maps/Set_{Set}/level{level}_data','rb')#f formats the stirng, curly brackets adds the level and set level variable to the stirng
    world_map = pickle.load(pickle_in)#loads data into world_map
world = World(world_map)#loads world data into the variable world to be later called

###buttons###
restart_button = Button(Screen_width//2 -30, Screen_height//2, restart_img)

#########################################################################################
                                     ###Game loop###
#########################################################################################

while run:#game loop
        
    Screen.fill((0,225,225))#fill screen with one colour

    clock.tick(fps)#ticks are restricted to 60 fps

    world.draw()#draws the wolrd

    spikes_group.draw(Screen)#draws the spikes onto the screen
    exit_group.draw(Screen)#draws the exit onto the screen
    coin_group.draw(Screen)#draws the coin onto the screen

    score_coin = Coin(tile_size//2,tile_size//2)#assigns a coin to the top left corn for the score counter
    coin_group.add(score_coin)
    
    game_over = player.update(game_over)#constantly loops the game_over until the is a colliision with an enemie/obstacle 

    if game_over == 0:#if the player has neither died or completed a level
        if pygame.sprite.spritecollide(player,coin_group, True):#if coin sprites collide with the player, the coin diappears
            coin_count += 1#player's score increases
        draw_text('X ' + str(coin_count),font, white, tile_size, 0)#converts score into a string and displays it at the top left of the screen as white text in the desird font
        

    if game_over == -1:#if player has died
        if restart_button.draw():#draws button and returns the variable 'action'
            ###when player dies the level resets###
            world.data = []#clear world.data
            world = reset_level(level)#resets level with the arguement lece
            game_over = 0#game restarts
            coin_count = 0#player's score increases ####change with lives algorthm####

    if game_over == 1:#if player has completed the level
        level += 1 #level variable increaes
        if level <= max_level:#if level is 1-5

            if level == 4: #change's spawn point based on level
                SPX = (60)
                SPY = (Screen_height-224)
            else:
                SPX = (48)
                SPY = (Screen_height-32)

            world.data = []#clear world.data
            world = reset_level(level)#resets level with the arguement level
            game_over = 0#game retarts

        else:
            ###when the player has completed the set of levels###
            if restart_button.draw():#restart button is drawn
                level = 1#level starts back at 1
                world.data = []#clear world.data
                world = reset_level(level)#resets level with the arguement lece
                game_over = 0#game restarts
                coin_count = 0#player's score increases

    for event in pygame.event.get(): #event loop
        if event.type == pygame.QUIT: #when the exit button  is clicked
            run = False #stop game loop
    
    pygame.display.update()#draws everything on to the screen 
    
pygame.quit()#exits pygame

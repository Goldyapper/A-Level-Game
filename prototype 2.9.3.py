#########################################################################################
                                     ###module imports###
#########################################################################################

import pygame, sys # imports pygame modules
import time#import time module
import pickle#import pickle module

from pygame.locals import * # imports local variables from pygame
from pygame import mixer# imports a module to be used to controll the music
from os import path# imports path to check if certain files exist

pygame.mixer.init() #iniitiates mixer
pygame.init() #initiates pygame

#########################################################################################
                                     ###Global Variables###
#########################################################################################

###Color Variables###

white = (255,255,255)#sets the white variable to the RGB for white
black = (0,0,0)#sets the black variable to the RGB for black

###Screen Variables###

clock = pygame.time.Clock()#used for capping clock ticks
fps = 60#60 frames per second
Screen_width = 640   #screen will be 20 tiles wide
Screen_height = 640 #screen will be 20 tiles high

### Game Variables ###

tile_size = 32 #size of each tile
run = True #Variable used for game loop
game_over = 0 #game over variable
max_level = 5 #max level variable
Set = 1#set of level variable
level = 1#level varaible 
coin_count = 0#score variable for how many coins the player collects

#menu variables#

main_menu = True#sets main menu as true, meaning it will be displayed straight away
difficulty_menu = False#sets difficulty menu as false, meaning it wont be displayed untl being called upon
action_guide = False#sets action guide menu as false, meaning it wont be displayed untl being called upon
level_select = False#sets the level select menu as false, meaning it wont be displayed untl being called upon

#time variables

timer = False#sets the timer variable to false, meaning it won't start until it is set to true
minutes_temp = 0#sets the temporary minutes variable to 0
seconds_temp = 0#sets the temporary seconds variable to 0
centiseconds_temp = 0# one 100ths of seconds #sets the temporary centiseconds variable to 0

###text variables###

font_1 = pygame.font.SysFont('Arial', 32)#imports the font arial and the size of 32 to be used later
font_2 = pygame.font.SysFont('Courier',128)#imports the font couriner and the size of 128 to be used later

#########################################################################################
                                     ###Import images###
#########################################################################################

###for buttons###

    #used in most menus#

Return_to_main_menu_img = pygame.image.load('images/Return_to_main_menu.png')#loads the return to main menu image

    #main menu#

Start_game_img = pygame.image.load ('images/Start_game.png')#loads the start game image
Action_guide_img = pygame.image.load ('images/Action_guide.png')#loads the action guide option image
Close_img = pygame.image.load ('images/Close.png')#loads the close image

    #difficulty select#

Easy_img = pygame.image.load ('images/Easy.png')#loads the easy image 
Medium_img = pygame.image.load ('images/Medium.png')#loads the medium image 
Hard_img = pygame.image.load ('images/Hard.png')#loads the hard image

    #level select#

Set_1_img = pygame.image.load('images/set_1.png')#loads the set 1 image
Set_2_img = pygame.image.load('images/set_2.png')#loads the set 2 image
Set_3_img = pygame.image.load('images/set_3.png')#loads the set 3 image

###for background###

    #main menu#

Main_menu_BG_img = pygame.image.load('images/Main_menu_BG.png')#loads the main menu background image

    #action guide#

Action_guide_BG_img = pygame.image.load('images/Action_guide_BG.png')#loads the action guide background image

    #difficulty menu#

Difficulty_select_BG_img = pygame.image.load('images/Difficulty_select_BG.png')#loads the main menu background image

    #level select menu#

Level_select_BG_img = pygame.image.load('images/Level_select_BG.png')#loads the level select menu background image

    #display timer#

Display_timer_BG_1 = pygame.image.load('images/Display_timer_BG_1.png')#loads the display timer background image for set 1
Display_timer_BG_2 = pygame.image.load('images/Display_timer_BG_2.png')#loads the display timer background image for set 2
Display_timer_BG_3 = pygame.image.load('images/Display_timer_BG_3.png')#loads the display timer background image for set 3

#########################################################################################
                                     ###Import sounds###
#########################################################################################

###sound effects###

coin_sound = pygame.mixer.Sound('music/coin.mp3')#imports the coin sound effect 
coin_sound.set_volume(0.25)#sets the volume to .25
jump_sound = pygame.mixer.Sound('music/jump.mp3')#imports the jump sound effect 2
jump_sound.set_volume(0.1)#sets the volume to .05
click_sound = pygame.mixer.Sound('music/click.mp3')#imports the coin sound effect 
click_sound.set_volume(0.1)#sets the volume to .1
death_sound = pygame.mixer.Sound('music/death.wav')#imports the coin sound effect 
death_sound.set_volume(0.25)#sets the volume to .25

###background music###
    #for the menus#
pygame.mixer.music.load('Music/menu.wav')#loads the menu file
pygame.mixer.music.set_volume(.2)#sets the volume to .2
pygame.mixer.music.play(-1)#plays indefinetly 

#########################################################################################
                                     ###Setting the screen###
#########################################################################################

Screen = pygame.display.set_mode((Screen_width, Screen_height))#creates a pygmae display the size of screen width*screen height
pygame.display.set_caption('Untitled Platformer')#names the screen in the top left

#####################################################w####################################
                                     ###Functions###
#########################################################################################


def draw_text(text,font,colour,x,y):#code for drawing text onto the game screen

    img = font.render(text, True, colour)#converts the text into an image with the colour of assignment
    Screen.blit(img, (x,y))#displays picture at co-ords of assignment



def reset_level(level):#code to reset/load the level data

    player.reset(48,608)#resets player at those co-ords, AKA their spawn point

    ###clear previous world map###
    exit_group.empty()#empties the exit group
    spikes_group.empty()#empties the spikes group
    platform_group.empty()#empties platform group
    coin_group.empty()#empties the coin group
    left_spikes_group.empty()#empties the left spikes group
    right_spikes_group.empty()#empties the right spikes group

    ###make new world map###
    if path.exists(f'Maps/Set_{Set}/level{level}_data'):#checks if the level data exists

        pickle_in = open(f'Maps/Set_{Set}/level{level}_data','rb')#f formats the stirng, curly brackets adds the level and set variable to the stirng
        world_map = pickle.load(pickle_in)#loads data into world_map

    world = World(world_map)#world uses class world and gives it the arguemenr woeld

    return world#returns the world variable

#########################################################################################
                                     ###Classes###
#########################################################################################


class Button():#code for buttons


    def __init__(self,x,y,image):#arguements are the self, x and y co-ords and the image for the button

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
               click_sound.play()#plays the click sound effect 
               
        if pygame.mouse.get_pressed()[0] == 0:#if the mouse key has been realeased

            self.clicked = False# button hasn't been clicked

        Screen.blit(self.image,self.rect)#draws button on the screen

        return action# action is returned so that it can be used later



class Player(): #code for player


    def __init__(self,x,y):#takes arguement self,x coords, y coords

        self.reset(x,y)#calls the reset function
        self.lives = 0 #sets self.lives to the lives variable



    def update(self,game_over):#updates player

        ###Variables for this function###
        dx = 0#dx and dy are used to see if there is going to be a colliision when the player moves 
        dy = 0
        collision_limit = 16#limit to allow the player to collide with the moving platform
        animation_cooldown = 5#cooldown for the animation

        
        if game_over == 0:#only happens if the player hasn't died or completed a level

            key = pygame.key.get_pressed()#key presses

        ###Reading key Presses and moving###

            #if the W key is pressed#
            if key[K_w] and self.jumped == False and self.in_air == False:# if the W key is press and the player isn't jumping

                jump_sound.play()#plays the jump sound effect 
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True#self.jump is set to true
                
            #if the UP key is pressed#
            if key[K_UP] and self.jumped == False and self.in_air == False:# if the up key is press and the player isn't jumping

                jump_sound.play()#plays the jump sound effect 
                self.vel_y = - 15 #Moves player up by 15
                self.jumped = True#self.jump is set to true

            #if the Space bar is pressed#
            if key[K_SPACE] and self.jumped == False and self.in_air == False:# if the up key is press and the player isn't jumping

                self.vel_y = - 15 #Moves player up by 15
                jump_sound.play()#plays the jump sound effect 
                self.jumped = True#self.jump is set to true

            #if the Space bar/W/Up is not being pressed#
            if key[K_UP] or key[K_w] or key[K_SPACE]== False:#if up/W/Space isn't being pressed

                self.jumped = False#self.jumped isn't true

            #if the left key or A is pressed#
            if key[pygame.K_LEFT] or key[pygame.K_a]:#if left key is pressed

                dx -= 5# moves player left by 5 pixels
                self.counter += 1#increase the animation counter by 1
                self.direction = -1#set the direction to -1

            #if the right key or D is pressed#
            if key[pygame.K_RIGHT] or key[pygame.K_d]:#if right key is pressed

                dx += 5# moves player left by 5 pixels
                self.counter += 1#increase the animation counter by 1
                self.direction = 1#set the direction to 1

            #if the Right/D/Left/A is not being pressed#
            if key[pygame.K_RIGHT] == False and key[pygame.K_d] == False and key[pygame.K_LEFT]== False and key[pygame.K_a] == False:#if the the player isn't moving right or left

                self.counter = 0#ccounter resets
                self.index = 0#index resets

                if self.direction == 1:#if the player is facing right

                    self.image = self.imgs_right[self.index]#the image chanegs to the one at the index

                if self.direction == -1:#if the player is facing left

                    self.image = self.imgs_left[self.index]#the image chanegs to the one at the index
                
            ###animation###
            if self.counter > animation_cooldown:#if the counter has reacher the colldown count

                self.counter = 0#resets the counter to 0
                self.index += 1#increases the index by 1

                if self.index >= len(self.imgs_right):#if the index is bigger than the range of images

                    self.index = 0#reset the the index to 0

                if self.direction == 1:#if the player is moving right

                   self.image = self.imgs_right[self.index]#the image chanegs to the one at the index

                if self.direction == -1:#if the player is moving left

                    self.image = self.imgs_left[self.index]#the image chanegs to the one at the index
                
                
            ###Gravity###
            self.vel_y += 1#falls by 1 every iteration

            if self.vel_y > 10:#stops the player falling faster than 10

                self.vel_y = 10#caps the falling speed

            dy += self.vel_y#adds gravity to players movement

            ###collision detection with tiles###
            self.in_air = True#player is in the air until proven otherwise


            for tile in world.tile_list:#checks every tile

                ###collisions in the x axis###
                if tile[1].colliderect(self.rect.x +dx,self.rect.y,self.width,self.height):#if there is collision in the x directions

                   dx = 0 #resets x movemnt to 0

                ###collisions in the y axis###
                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):#if there is collision in the y directions

                    if self.vel_y < 0: #if player is below the ground

                        dy = tile[1].bottom - self.rect.top#the distance the player will move is the height between the bottom of the tile and the top of the player
                        self.vel_y = 0 #resets y velocity to 0

                    elif self.vel_y >= 0: #if player is above the ground

                        dy = tile[1].top - self.rect.bottom#the distance the player will move is the height between the top of the tile and the bottom of the player
                        self.vel_y = 0 #resets y velocity to 0
                        self.in_air = False#resets self.in_air to false

            ###collision detection with spikes###
            if pygame.sprite.spritecollide(self,spikes_group, False):#if spike sprites collide with the player

                player.lives -= 1#player has died and loses a life
                game_over = -1#game over canges to -1

            if pygame.sprite.spritecollide(self,left_spikes_group, False):#if left spike sprites collide with the player

                player.lives -= 1#player has died and loses a life
                game_over = -1#game over canges to -1
                
            if pygame.sprite.spritecollide(self,right_spikes_group, False):#if left spike sprites collide with the player

                player.lives -= 1#player has died and loses a life
                game_over = -1#game over canges to -1                
                
            if pygame.sprite.spritecollide(self,exit_group, False):#if exit sprites collide with the player

                game_over = 1#player has completed the level

            ###collisions with moving platforms###
            for platform in platform_group:#every platform regardless of the direction they move in

                ###collisions with the platforms in the x-axis###
                if platform.rect.colliderect(self.rect.x +dx,self.rect.y,self.width,self.height):#if the player moving in the x-axis collides with the platform

                    dx = 0#x collision resets
                    
                ###collisions with the platforms in the y-axis###
                if platform.rect.colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):#if the player moving in the y-axis collides with the platform

                    if abs((self.rect.top + dy) - platform.rect.bottom) < collision_limit:#it player jumps and is below the platform

                        self.vel_y = 0#the player stops moving up
                        dy = platform.rect.bottom - self.rect.top#calcualtes how far the player can jump                

                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collision_limit:#it player is above the platform

                        self.rect.bottom = platform.rect.top - 1 #sets the players bottom to the top of the platform -1, allowing him to move left and right
                        self.in_air = False
                        dy = 0#the player is moved by the platform therefore whilst standing on it, their y-axis

                ###move player sideways with the platform###
                    if platform.move_x != 0: #must be a horizontially moving platform

                        self.rect.x += platform.move_direction#moves the player the same amount as the platform is moving   

            ####final player movemt###
            self.rect.x += dx#player moves on the x axis by dx
            self.rect.y += dy#player moves on the right axis by dy
            
         
        Screen.blit(self.image,self.rect)#display the player image and rect

        return game_over#returns the game_over varaible to be use in the game loop



    def reset(self,x,y):#reset function for when player is spawned/dies

        self.imgs_right = []#used to store the right images
        self.imgs_left= []#used to store the left images
        self.index = 0#used for the animation index counter
        self.counter = 0#used for the speed in which the animation runs at

        #animating the player#
        for num in range (1,4):#for range 1 to 3

            img = pygame.image.load(f'images/player_{num}.png')#opens the numbered image from images folder
            img_right = pygame.transform.scale(img,(48,72))#scales image to be 48 pixels by 72 pixels
            img_right.set_colorkey((white))#white pixels of the file are transparent
            img_left = pygame.transform.flip(img_right,True,False)#flips the right image on the x axis and assigns it to the left image varable
            img_left.set_colorkey((white))#white pixels of the file are transparent
            self.imgs_right.append(img_right)#adds the images to the right image list
            self.imgs_left.append(img_left)#adds the images to the left image list

        self.image = self.imgs_right[self.index]#loads the image from the index point from the list

        #physics for the player image#
        self.rect = self.image.get_rect()#takes a rect from the image
        self.rect.x = x#sets the rects x coords
        self.rect.y = y#sets the rects y coords
        self.vel_y = 0#sets gravity speed to 0
        self.width = self.image.get_width()#gets the width of the player
        self.height = self.image.get_height()#get the height of the player
        self.jumped = False #player has jumped = no
        self.in_air = True #assumes player is in the air
        self.direction = 0#used to determine what way the player is facing



class World(): #code for world

    def __init__(self,data): #init takes a self and data argument

        self.tile_list = []#creates a list to store the tiles

    ###load images###
        Platform_img = pygame.image.load('images/Platform.png')#load the filename image into a variable

        #displays different bondary/set/level tiles depending on the level.
        boundary_img = pygame.image.load(f'images/Boundary_{Set}.png')#load the filename image into a variable depending on the set variable
        Set_img = pygame.image.load(f'images/Level_{Set}.png')#load the filename image into a variable depending on the set variable
        Level_img = pygame.image.load(f'images/{Set}_{level}.png')
        
        ###loop that reads map and decides what to display###
        y = 0 #y co-ords

        for layer in data:

            x = 0 # x co-ords

            for tile in layer:
                
                #######explatation for each number######

                #tile 1 = boundary
                #tile 2 = platform
                #tile 3 = spikes
                #tile 4 = exit
                #tile 5 = coin
                #tile 6 = horizontial platforms
                #tile 7 = vertical plaforms
                #tile 8 = left sidewards spikes
                #tile 9 = right sidewards spikes
                #tile 10 = set image
                #tile 11 = set image


                if tile == 1:

                    img = pygame.transform.scale(boundary_img,(tile_size,tile_size))#scales boundary images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list

                if tile == 2:

                    img = pygame.transform.scale(Platform_img,(tile_size,tile_size))#scales platform images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list

                if tile == 3:

                    spikes =  Spikes(x * tile_size,y * tile_size)#createas a spike instance and positions it at the x and y co-ords
                    spikes_group.add(spikes)#adds spikes to the spikes group

                if tile == 4:

                    exit = Exit(x * tile_size,y * tile_size - (tile_size))#createas a exit instance and positions it at the x and y co-ords
                    exit_group.add(exit)#adds exit to the exit group

                if tile == 5:

                    coin = Coin(x * tile_size + (tile_size // 2),y * tile_size + (tile_size // 2))#createas a coin instance and positions it at the center of the tile block
                    coin_group.add(coin)#adds coin to the coin group

                if tile == 6:

                    platform = Moving_Platform(x * tile_size ,y * tile_size,1,0)#creates a moving platform instance and positions it at the x and y co-ords and sets move_x to 1
                    platform_group.add(platform)#adds moving platform to the platform group

                if tile == 7:

                    platform = Moving_Platform(x * tile_size ,y * tile_size,0,1)#creates a moving platform instance and positions it at the x and y co-ords and sets move_y to 1
                    platform_group.add(platform)#adds moving  platform to the platform group

                if tile == 8:

                    left_spikes =  Left_Spikes(x * tile_size,y * tile_size)#creates a leftwards spike instance and positions it at the x and y co-ords
                    left_spikes_group.add(left_spikes)#adds leftwards spikes to the leftwards spikes group

                if tile == 9:

                    right_spikes =  Right_Spikes(x * tile_size,y * tile_size)#creates a rightward spike instance and positions it at the x and y co-ords
                    right_spikes_group.add(right_spikes)#adds rightward spikes to the rightward spikes group

                if tile == 10:

                    img = pygame.transform.scale(Set_img,(tile_size*3,tile_size))#scales set images to a tile high and 3 tiles long
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list
                    
                if tile == 11:

                    img = pygame.transform.scale(Level_img,(tile_size,tile_size))#scales level images to tile size
                    img_rect = img.get_rect()#takes the size of the image and creates a rect that is that size
                    img_rect.x = x * tile_size#x cordiante on the screen where the rect will be
                    img_rect.y = y * tile_size#y cordiante on the screen where the rect will be
                    tile = (img, img_rect)#saves info as a tuple called tile
                    self.tile_list.append(tile)#adding tile to tile list
                    

                x += 1 #moves to the next tile
                
            y += 1 #moves to the layer

                
    def draw(self): #functions to draw the tiles

        for tile in self.tile_list: #for every tile in the list

           Screen.blit(tile [0],tile[1]) #display the tiles



###Spikes class###
class Spikes(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/spikes.png')#loads the spikes image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))#scales image to be the size of a tile
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement 


###Left sidewards spikes class###
class Left_Spikes(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/Sidewards_spike_left.png')#loads the spikes left image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))#scales image to be the size of a tile
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement


###Right sidewards spikes class###
class Right_Spikes(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/Sidewards_spike_right.png')#loads the spikes right image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))#scales image to be the size of a tile
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement 


###Exit class###
class Exit(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/exit.png')#loads the exit image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 2)))#scales image to be a tile wide and 2 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement


###Coin class###
class Coin(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Coin.png')#loads the coin image
        self.image = pygame.transform.scale(img, (tile_size //2, tile_size //2))#scales image to be a 1/2 tile wide and 1/2 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.center = (x,y)#sets the x co-ords of the rect from the arguement to the mid-point of the rect 


###Heart class###
class Heart(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y):#arguemtns are self and x and y co-ords

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Heart.png')#loads the Heart image
        self.image = pygame.transform.scale(img, (tile_size, tile_size))#scales image to be a 1 tile wide and 1 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.center = (x,y)#sets the x co-ords of the rect from the arguement to the mid-point of the rect 


###Platform class###
class Moving_Platform(pygame.sprite.Sprite):#arguements are the bass class for game objects


    def __init__(self,x,y,move_x,move_y):#arguemtns are self and x and y co-ords,movement on the x direction and movement in the y direction

        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Moving_Platform.png')#loads the Moving Platform image
        self.image = pygame.transform.scale(img, (tile_size * 2, tile_size ))#scales image to be a 2 tiles wide and tile tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement
        self.move_counter = 0#sets the move counter
        self.move_direction = 1#sets the dierection to 1
        self.move_x = move_x#sets movement in the x direction to move_x
        self.move_y = move_y#sets movement in the y direction to move_y


    def update(self):#update function for the movement 

        self.rect.x += self.move_direction * self.move_x #moves the x co-ords by the self.move direction * self_move_x
        self.rect.y += self.move_direction * self.move_y#moves the y co-ords by the self.move direction * self_move_y
        self.move_counter += 1#increase the move counter

        if abs(self.move_counter) > 64:# if the self.move_counter value (ignores +/-) is bigger than 64

            self.move_direction *= -1#flips the move_direction value
            self.move_counter *= -1#flips the move_counter value
        
#########################################################################################
                                     ###Misc stuff###
#########################################################################################

###spawn point assignment###
player = Player(48,608)#creates a player instance at those co=ords, AKA their spawn point

###Creating sprite groups###
spikes_group = pygame.sprite.Group()#creates the spikes group
coin_group = pygame.sprite.Group()#creates the coin group
exit_group = pygame.sprite.Group()#creates the exit group
platform_group = pygame.sprite.Group()#Creates the moving platform group
left_spikes_group = pygame.sprite.Group()#creates the spikes group
right_spikes_group = pygame.sprite.Group()#creates the spikes group
heart_group = pygame.sprite.Group()#creates the hearts group

###buttons###

    #used for most menus#
Return_to_main_menu_button = Button(Screen_width - 290, Screen_height - 115,Return_to_main_menu_img)#creates a return to main menu button instance at give co-ords and loads the easy image

    #main menu buttons#
Start_game_button = Button(335,162, Start_game_img)#creates a start game button instance at give co-ords and loads the given image
Action_guide_button = Button(335,287, Action_guide_img)#creates an action guide button instance at give co-ords and loads the given image
Exit_button = Button(335,412, Close_img)#creates an close button instance at give co-ords and loads the medium image

    #difficulty select menu#
Easy_button = Button(55,162, Easy_img)#creates an easy button instance at give co-ords and loads the easy image
Medium_button = Button(55,287, Medium_img)#creates an medium button instance at give co-ords and loads the medium image
Hard_button = Button(55,412, Hard_img)#creates an hard button instance at give co-ords and loads the hard image

    #level select menu#   
Set_1_button = Button(305,162,Set_1_img)#creates a set 1 button instance at give co-ords and loads the set 1 image
Set_2_button = Button(305,287,Set_2_img)#creates a set 2 button instance at give co-ords and loads the set 2 image
Set_3_button = Button(305,412,Set_3_img)#creates a set 3 button instance at give co-ords and loads the set 3 image

#########################################################################################
                                     ###Game loop###
#########################################################################################

while run:#if run is true
 
    clock.tick(fps)#ticks are restricted to fps variable
    key = pygame.key.get_pressed()#key presses
    if key[pygame.K_ESCAPE]:#if ESC is pressed at any point
        run = False#game closes 
    

    ###main menu##
    if main_menu:#if main menu is true

        Screen.blit (Main_menu_BG_img,(0,0))#shows the background image of the main menu

        if Start_game_button.draw():#if the start game button is pressed

            difficulty_menu = True#difficulty menu is opened
            main_menu = False#main menu is closed            

        if Action_guide_button.draw():#if the action guide button is pressed

            action_guide = True#action guide is opened
            main_menu = False#main menu is closed

        if Exit_button.draw():#if the exit game button is pressed

            run = False #stops game loop and closes the game


    else:#if the main menu is not being displyed

        ###action guide menu###
        if action_guide:#if the difficulty menu is being displayed

            Screen.blit (Action_guide_BG_img,(0,0))#shows the background image of the action guide menu
            
            if Return_to_main_menu_button.draw():#return to main menu button is drawn

                main_menu = True #main menu is opened
                action_guide = False

        
        ###difficulty menu###
        elif difficulty_menu:#if the difficulty menu is being displayed

            Screen.blit(Difficulty_select_BG_img,(0,0))#shows the background image of the difficulty menu
            
            if Easy_button.draw():#if the easy button is pressed

                player.lives = 5#lives are set to 5
                difficulty_menu = False#difficulty menu is closed
                level_select = True #level select is opened
                
            if Medium_button.draw():#if the medium button is pressed

                player.lives = 3#lives are set to 3
                difficulty_menu = False#difficulty menu is closed
                level_select = True#level select is opened
 
            if Hard_button.draw():#if the hard button is pressed

                player.lives = 1#lives are set to 1
                difficulty_menu = False#difficulty menu is closed5
                level_select = True#level select is opened

            if Return_to_main_menu_button.draw():#return to main menu button is drawn

                main_menu = True #main menu is opened
                difficulty_menu = False


        ###level select menu###                
        elif level_select:#if the level select menu is being displayed

            Screen.blit(Level_select_BG_img,(0,0))#shows the background image of the level select menu

            if Set_1_button.draw():#if the set 1 button is pressed

                Set = 1#set variable is set to 1
                level_select = False#level select menu is closed
                time_start = time.time()#sets the time start variable to the current time
                timer = True#starts the timer loop
                world = reset_level(level)#resets level with the arguement level
                coin_count = 0#sets the coin count to 0
                pygame.mixer.music.stop()#stops all the currently playing music
                pygame.mixer.music.unload()#unloads the music the music queue
                pygame.mixer.music.load('music/Set_1.wav')#loads the set 1 file
                pygame.mixer.music.play(-1)#plays indefinetly 

            if Set_2_button.draw():#if the set 2 button is pressed

                Set = 2#set variable is set to 2
                level_select = False#evel select menu is closed
                time_start = time.time()#sets the time start variable to the current time
                timer = True#starts the timer loop
                world = reset_level(level)#resets level with the arguement level
                coin_count = 0#sets the coin count to 0
                pygame.mixer.music.stop()#stops all the currently playing music
                pygame.mixer.music.unload()#unloads the music the music queue
                pygame.mixer.music.load('music/Set_2.wav')#loads the set 2 file
                pygame.mixer.music.play(-1)#plays indefinetly 

            if Set_3_button.draw():#if the set 3 button is pressed

                Set = 3#set variable is set to 3
                level_select = False#evel select menu is closed
                time_start = time.time()#sets the time start variable to the current time
                timer = True#starts the timer loop
                world = reset_level(level)#resets level with the arguement level
                coin_count = 0#sets the coin count to 0
                pygame.mixer.music.stop()#stops all the currently playing music
                pygame.mixer.music.unload()#unloads the music the music queue
                pygame.mixer.music.load('music/Set_3.wav')#loads the set 2 file
                pygame.mixer.music.play(-1)#plays indefinetly 

                
            if Return_to_main_menu_button.draw():#return to main menu button is drawn

                main_menu = True #main menu is opened
                level_select = False

        ###level loop###
        else:#display the game

            ###displaying the game###
            
            if Set == 1:#if the player is on set 1
                Screen.fill((0,153,0))#fill screen with green


            if Set == 2:#if the player is on set 2
                Screen.fill((102,225,225))#fill screen with light blue


            if Set == 3:#if the player is on set 3
                Screen.fill((153,0,0))#fill screen with red


            game_over = player.update(game_over)#constantly loops the game_over until the is a colliision with an enemie/obstacle 

            world.draw()#draws the world

            ###loading and checking the sprite groups###

                #creating a coin in the top left corner#
            score_coin = Coin(tile_size//2,tile_size//2)#assigns a coin to the top left corner for the score counter
            coin_group.add(score_coin)#adds the score coin to the coin group

                #creates a heart in the top right corner
            Lives_Heart = Heart(Screen_width-(tile_size//2 + tile_size * 2),tile_size//2)#assigns a heart to the top right corner for the lives counter
            heart_group.add(Lives_Heart)#adds the heart for the heart group

                #draws the sprite groups#
            spikes_group.draw(Screen)#draws the spikes onto the screen
            exit_group.draw(Screen)#draws the exit onto the screen
            coin_group.draw(Screen)#draws the coin onto the screen
            platform_group.draw(Screen)#draws the platform onto the screen
            left_spikes_group.draw(Screen)#draws the rightwards spikes onto the screen
            right_spikes_group.draw(Screen)#draws the leftwards spikes onto the screen
            heart_group.draw(Screen)#draws the heart onto the screen


            if timer == True:#the timer loop
                
                seconds_temp = int(time.time() - time_start) - minutes_temp * 60#calcuating the seconds passed
                centiseconds_temp = round(time.time() - time_start - (minutes_temp * 60) - seconds_temp, 2)#calculates the centiseconds passed


                if seconds_temp >= 60:#if 60 seconds passes

                    minutes_temp += 1##increases the minutes by 1
                    seconds_temp = 0#resets seconds to 0
                    

            if game_over == 0:#if the player has neither died or completed a level

                platform_group.update()#updates the moving platform groups

                draw_text('X  ' + str(coin_count),font_1, white, tile_size*1.25, -2)#converts score into a string and displays it at the top left of the screen as white text in the desird font
                draw_text('X  ' + str(player.lives),font_1, white,Screen_width - (tile_size*1.75), -2)#converts score into a string and displays it at the top left of the screen as white text in the desird font

                if pygame.sprite.spritecollide(player,coin_group, True):#if coin sprites collide with the player, the coin diappears

                    coin_count += 1#player's score increases
                    coin_sound.play()#plays the coin sound effect 

                    
            if game_over == -1:#if player has died

                if player.lives == 0:#player has run out of lives

                    death_sound.play()#plays the death sound
                    world.data = []#clear world.data
                    level = 1#resets level to 1
                    pygame.mixer.music.stop()#stops the music
                    pygame.mixer.music.unload()#unloads the music queue
                    pygame.mixer.music.load('music/menu.wav')#loads the menu file
                    pygame.mixer.music.set_volume(.2)#sets the volume sto .2
                    pygame.mixer.music.play(-1)#plays indefinetly
                    timer = False#resets the timer to flase
                    main_menu = True#resets the main menu to True,opeing the main menu

                    
                else:#if the player has spare lives

                        ###when player dies the level resets###
                        world.data = []#clear world.data
                        world = reset_level(level)#resets level with the arguement lece
                        game_over = 0#game restarts

            if game_over == 1:#if player has completed the level

                level += 1 #level variable increaes

                if level <= max_level:#if is not the last level of the set

                    world.data = []#clear world.data
                    world = reset_level(level)#resets level with the arguement level
                    game_over = 0#game retarts

                else:#if the player has completed the set of levels
                    
                    ###when the player has completed the set of levels###
                    timer = False#stops the timer

                    ###deciding what background to display depending on what set thay had just beaten###
                    Display_timer_BG_img = pygame.image.load(f'images/Display_timer_BG_{Set}.png')                    
                    Screen.blit (Display_timer_BG_img,(0,0))#dispalys the display timer backgroud
                    
                    ###convert time into 2 digit interers###
                        #centiseconds#
                    c_seconds_temp = int((centiseconds_temp)*100)#converts centiseconds into an interger
                        
                    if c_seconds_temp < 10:#if the c_seconds_temp is less than 10

                       c_seconds = str('0' + str(c_seconds_temp))#puts a zero in front of the 1st digit

                    else:

                        c_seconds = c_seconds_temp#if it is two digits long, nothing changes

                        #seconds#
                    if seconds_temp < 10:#if the seconds_temp is less than 10

                       seconds = str('0' + str(seconds_temp))#puts a zero in front of the 1st digit

                    else:

                        seconds = seconds_temp#if it is two digits long, nothing changes

                        #minutes#
                    if minutes_temp < 10:#if the miutes_temp is less than 10

                        minutes = str('0' + str(minutes_temp))#puts a zero in front of the 1st digit

                    else:

                        minutes = minutes_temp#if it is two digits long, nothing chnages
                        
                    draw_text(f'{minutes}:{seconds}:{c_seconds}',font_2,black,16,200)#displays the time passed on screen, it is in the centre of the screen
                    

                    if Return_to_main_menu_button.draw():#return to main menu button is drawn

                        level = 1#level is rest to 0
                        world.data = []#clear world.data
                        world = reset_level(level)
                        game_over = 0#game over is reset to 0
                        main_menu = True#main menu is 
                        pygame.mixer.music.stop()#stops the music
                        pygame.mixer.music.unload()#unloads the music queue
                        pygame.mixer.music.load('music/menu.wav')#loads the menu file
                        pygame.mixer.music.set_volume(.2)#sets the volume to .1
                        pygame.mixer.music.play(-1)#plays indefinetly


    for event in pygame.event.get(): #event loop

        if event.type == pygame.QUIT: #when the exit button  is clicked

            run = False #stop game loop and closes the game
    
    pygame.display.update()#draws everything on to the screen 

pygame.quit()#exits pygame and ends the program
#########################################################################################
                                     ###imports###
#########################################################################################

import pygame, sys # imports pygame modules
import time#import time module
from pygame.locals import * # imports local variables from pygame
from os import path# imports path to check if certain files exist
import pickle#import pickle module

pygame.init() #initiates pygame

#########################################################################################
                                     ###Global Variables###
#########################################################################################

###Color Variables###

white = (255,255,255)
black = (0,0,0)

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
SPX = 48 #spawn point on the x-axis
SPY = (Screen_height-32)#spawn point on the y-axis
coin_count = 0#score variable for how many coins the player collects

#menu variables#
main_menu = True#sets main menu as true, meaning it will be displayed straight away
difficulty_menu = False#sets difficulty menu as false, meaning it wont be displayed untl being called upon
action_guide = False


#time variables

timer = False
minutes_temp = 0
seconds_temp = 0
centiseconds_temp = 0# one 100ths of seconds

###text variables###

font_1 = pygame.font.SysFont('Arial', 32)#imports the font arial and the size of 32 to be used later
font_2 = pygame.font.SysFont('Courier',128)#imports the font couriner and the size of 128 to be used later

#########################################################################################
                                     ###Import images###
#########################################################################################

###for buttons###
Return_to_main_menu_img = pygame.image.load ('images/Return_to_main_menu.png')#loads the return to main menu image
Easy_img = pygame.image.load ('images/Easy.png')#loads the easy image 
Medium_img = pygame.image.load ('images/Medium.png')#loads the medium image 
Hard_img = pygame.image.load ('images/Hard.png')#loads the hard image

Start_game_img = pygame.image.load ('images/Start_game.png')#loads the start game image
Action_guide_img = pygame.image.load ('images/Action_guide.png')#loads the action guide option image
Close_img = pygame.image.load ('images/Close.png')#loads the close image

###for background###

    #main menu#
Main_menu_BG_img = pygame.image.load('images/Main_menu_BG.png')#loads the main menu background image

    #difficulty menu#
Difficulty_select_BG_img = pygame.image.load('images/Difficulty_select_BG.png')#loads the main menu background image

    #display timer#
Display_timer_BG_1 = pygame.image.load('images/Display_timer_BG_1.png')#loads the display timer background image for set 1
Display_timer_BG_2 = pygame.image.load('images/Display_timer_BG_2.png')#loads the display timer background image for set 2
Display_timer_BG_3 = pygame.image.load('images/Display_timer_BG_3.png')#loads the display timer background image for set 3

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
    spikes_group.empty()#empties the spikes group
    platform_group.empty()#empties platform group
    coin_group.empty()#empties the coin group
    left_spikes_group.empty()#empties the left spikes group
    right_spikes_group.empty()#empties the right spikes group

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
        self.lives = 0 #sets self.lives to the lives variable


    def update(self,game_over):#updates player

        ###Variables for this function###
        dx = 0#dx and dy are used to see if there is going to be a colliision when the player moves 
        dy = 0
        collision_limit = 16#limit to allow the player to collide with the moving platform

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
                        self.in_air = False

            ###collision detection with spikes###
            if pygame.sprite.spritecollide(self,spikes_group, False):#if spike sprites collide with the player
                player.lives -= 1#player has died and loses a life
                game_over = -1#game lop canges to -1

            if pygame.sprite.spritecollide(self,left_spikes_group, False):#if left spike sprites collide with the player
                player.lives -= 1#player has died and loses a life
                game_over = -1#game lop canges to -1
                
            if pygame.sprite.spritecollide(self,right_spikes_group, False):#if left spike sprites collide with the player
                player.lives -= 1#player has died and loses a life
                game_over = -1#game lop canges to -1                
                
            if pygame.sprite.spritecollide(self,exit_group, False):#if exit sprites collide with the player
                game_over = 1#player has won


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
                        self.rect.x += platform.move_direction    


            ####final player movemt###
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
        #deisplays different bondary blocks depending on the level.
        boundary_img = pygame.image.load(f'images/Boundary_{Set}.png')#load the filename image into a variable

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
                if tile == 3:
                    spikes =  Spikes(x * tile_size,y * tile_size)#createas a spike instance and positions it at the x and y co-ords
                    spikes_group.add(spikes)#adds spikes to the spikes group
                if tile == 4:
                    exit = Exit(x * tile_size,y * tile_size - (tile_size))#createas a exit instance and positions it at the x and y co-ords
                    exit_group.add(exit)#adds exit to the exit group
                if tile == 5:
                    coin = Coin(x * tile_size + (tile_size // 2),y * tile_size + (tile_size // 2))#createas a spike instance and positions it at the x and y co-ords
                    coin_group.add(coin)#adds coin to the coin group
                if tile == 6:
                    platform = Moving_Platform(x * tile_size ,y * tile_size,1,0)#creates a platform instance and positions it at the x and y co-ords and sets move_x to 1
                    platform_group.add(platform)#adds platform to the platform group
                if tile == 7:
                    platform = Moving_Platform(x * tile_size ,y * tile_size,0,1)#creates a platform instance and positions it at the x and y co-ords and sets move_y to 1
                    platform_group.add(platform)#adds platform to the platform group
                if tile == 8:
                    left_spikes =  Left_Spikes(x * tile_size,y * tile_size)#creates a leftwards spike instance and positions it at the x and y co-ords
                    left_spikes_group.add(left_spikes)#adds leftwards spikes to the leftwards spikes group
                if tile == 9:
                    right_spikes =  Right_Spikes(x * tile_size,y * tile_size)#creates a rightward spike instance and positions it at the x and y co-ords
                    right_spikes_group.add(right_spikes)#adds rightward spikes to the rightward spikes group
                x += 1 #moves to the next tile 
            y += 1 #moves to the layer
                
    def draw(self): #functions to draw the tiles
        for tile in self.tile_list: #every tile in the list
            Screen.blit(tile [0],tile[1]) #display the tiles

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


###Left sidewards spikes class###
class Left_Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/Sidewards_spike_left.png')#loads the spikes image
        img.set_colorkey(white)#white pixels of the file are transparent
        self.image = pygame.transform.scale(img, (tile_size,tile_size))#scales image to be the size of a tile
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement


###Right sidewards spikes class###
class Right_Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer 
        img = pygame.image.load('images/Sidewards_spike_right.png')#loads the spikes image
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
        img = pygame.image.load('images/Coin.png')#loads the coin image
        self.image = pygame.transform.scale(img, (tile_size //2, tile_size //2))#scales image to be a 1/2 tile wide and 1/2 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.center = (x,y)#sets the x co-ords of the rect from the arguement to the mid-point of the rect 

###Heart class###
class Heart(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Heart.png')#loads the Heart image
        self.image = pygame.transform.scale(img, (tile_size, tile_size))#scales image to be a 1 tile wide and 1 tiles tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.center = (x,y)#sets the x co-ords of the rect from the arguement to the mid-point of the rect 

###Platform class###
class Moving_Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,move_x,move_y):
        pygame.sprite.Sprite.__init__(self)#runs the built-in sprite class initializer
        img = pygame.image.load('images/Moving_Platform.png')#loads the Moving Platform image
        self.image = pygame.transform.scale(img, (tile_size * 2, tile_size ))#scales image to be a 2 tiles wide and tile tall
        self.rect = self.image.get_rect()#gets a rect for the image
        self.rect.x = x#sets the x co-ords of the rect from the arguement 
        self.rect.y = y#sets the y co-ords of the rect from the arguement
        self.move_counter = 0#sets the move counter
        self.move_direction = 1#sets the dierection to 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x #moves the x co-ords by the self.move direction * self_move_x
        self.rect.y += self.move_direction * self.move_y#moves the y co-ords by the self.move direction * self_move_y
        self.move_counter += 1#increase the move counter
        if abs(self.move_counter) > 64:# if the self.move_counter value (ignores +/-) is bigger than 50
            self.move_direction *= -1#flips the move_direction value
            self.move_counter *= -1#flips the move_counter value
        
        
            
#########################################################################################
                                     ###c stuff###
#########################################################################################

###spawn point assignment###
player = Player(SPX,SPY)#creates a player instance at those co=ords, AKA their spawn point

###Sprite group stuff###
spikes_group = pygame.sprite.Group()#creates the spikes group
coin_group = pygame.sprite.Group()#creates the coin group
exit_group = pygame.sprite.Group()#creates the exit group
platform_group = pygame.sprite.Group()#Creates the moving platform group
left_spikes_group = pygame.sprite.Group()#creates the spikes group
right_spikes_group = pygame.sprite.Group()#creates the spikes group
heart_group = pygame.sprite.Group()#creates the hearts group

#uses reset_level function to assign data to the variable world
world = reset_level(level)#resets level with the arguement lece

###buttons###
Start_game_button = Button(335,162, Start_game_img)#creates a start game button instance at give co-ords and loads the given image
Action_guide_button = Button(335,287, Action_guide_img)#creates an action guide button instance at give co-ords and loads the given image
Exit_button = Button(335,412, Close_img)#creates an close button instance at give co-ords and loads the medium image

Return_to_main_menu_button = Button(Screen_width - 290, Screen_height - 115,Return_to_main_menu_img)#creates a return to main menu button instance at give co-ords and loads the easy image
Easy_button = Button(55,162, Easy_img)#creates an easy button instance at give co-ords and loads the easy image
Medium_button = Button(55,287, Medium_img)#creates an medium button instance at give co-ords and loads the medium image
Hard_button = Button(55,412, Hard_img)#creates an hard button instance at give co-ords and loads the hard image

#########################################################################################
                                     ###Game loop###
#########################################################################################
while run:#if run is ture
 
    clock.tick(fps)#ticks are restricted to 60 fps

    if main_menu:#if main menu is true

        Screen.blit (Main_menu_BG_img,(0,0))#shows the background image of the main menu

        if Start_game_button.draw():#if the start game button is pressed
            difficulty_menu = True#difficulty menu is opened
            main_menu = False#main menu is closed

        if Action_guide_button.draw():#if the start game button is pressed
            action_guide = True#difficulty menu is opened
            main_menu = False#main menu is closed

        if Exit_button.draw():#if the start game button is pressed
            run = False #stop game loop


    else:#if the main menu is not being displyed 

        if difficulty_menu:#if the difficulty menu is being displayed


            Screen.blit (Difficulty_select_BG_img,(0,0))#shows the background image of the difficulty menu
            
            if Easy_button.draw():#if the easy button is pressed
                player.lives = 5#lives are set to 5
                difficulty_menu = False#difficulty menu is closed
                time_start = time.time()#move to set of level buttons
                timer = True
                ###when the start game menu is coded, add it to be called here
                
            if Medium_button.draw():
                player.lives = 3#lives are set to 3
                difficulty_menu = False#difficulty menu is closed
                time_start = time.time()#move to set of level buttons
                timer = True
                ###when the start game menu is coded, add it to be called here
                
            if Hard_button.draw():
                player.lives = 1#lives are set to 1
                difficulty_menu = False#difficulty menu is closed5
                time_start = time.time()#move to set of level buttons
                timer = True
                ###when the start game menu is coded, add it to be called here
                

        else:#if the difficulty menu is not being displayed

            ###displaying the game###

            Screen.fill((0,225,225))#fill screen with one colour
            
            world.draw()#draws the wolrd

            score_coin = Coin(tile_size//2,tile_size//2)#assigns a coin to the top left corner for the score counter
            coin_group.add(score_coin)#adds the score coin to the coin group
            
            Lives_Heart = Heart(Screen_width-(tile_size//2 + tile_size * 2),tile_size//2)#assigns a heart to the top right corner for the lives counter
            heart_group.add(Lives_Heart)#adds the heart to the heart group

            spikes_group.draw(Screen)#draws the spikes onto the screen
            exit_group.draw(Screen)#draws the exit onto the screen
            coin_group.draw(Screen)#draws the coin onto the screen
            platform_group.draw(Screen)#draws the platform onto the screen
            left_spikes_group.draw(Screen)#draws the rightwards spikes onto the screen
            right_spikes_group.draw(Screen)#draws the leftwards spikes onto the screen
            heart_group.draw(Screen)#draws the heart onto the screen


            if timer == True:
                
                seconds_temp = int(time.time() - time_start) - minutes_temp * 60
                centiseconds_temp = round(time.time() - time_start - seconds_temp, 2)

                if seconds_temp >= 60:
                    minutes_temp += 1
                    seconds_temp = 0


            game_over = player.update(game_over)#constantly loops the game_over until the is a colliision with an enemie/obstacle 

            if game_over == 0:#if the player has neither died or completed a level

                platform_group.update()

                draw_text('X  ' + str(coin_count),font_1, white, tile_size*1.25, -2)#converts score into a string and displays it at the top left of the screen as white text in the desird font
                draw_text('X  ' + str(player.lives),font_1, white,Screen_width - (tile_size*1.75), -2)#converts score into a string and displays it at the top left of the screen as white text in the desird font

                if pygame.sprite.spritecollide(player,coin_group, True):#if coin sprites collide with the player, the coin diappears
                    coin_count += 1#player's score increases

                    
            if game_over == -1:#if player has died

                if player.lives == 0:#player has run out of lives

                    world.data = []#clear world.data
                    level = 1
                    timer = False
                    difficulty_menu = True
                    print ('Return to main menu')

                    
                else:#if the player has spare lives

                        ###when player dies the level resets###
                        world.data = []#clear world.data
                        world = reset_level(level)#resets level with the arguement lece
                        game_over = 0#game restarts
                        coin_count = 0#player's score resets 

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
                    if Set == 1:
                        Screen.blit (Display_timer_BG_1,(0,0))
                    if Set == 2:
                        Screen.blit (Display_timer_BG_2,(0,0))
                    if Set == 3:
                        Screen.blit (Display_timer_BG_3,(0,0))
                    
                    ###convert time into 2 digit interers###
                        #centiseconds#
                    c_seconds_temp = int((centiseconds_temp)*100)#converts centiseconds into an interger
                        
                    if c_seconds_temp < 10:
                       c_seconds = str('0' + str(c_seconds_temp))
                    else:
                        c_seconds = c_seconds_temp

                        #seconds#
                    if seconds_temp < 10:
                       seconds = str('0' + str(seconds_temp))
                    else:
                        seconds = seconds_temp

                        #minutes#
                    if minutes_temp < 10:
                       minutes = str('0' + str(minutes_temp))
                    else:
                        minutes = minutes_temp

                    draw_text(f'{minutes}:{seconds}:{c_seconds}',font_2,black,16,200)#displays the time passed on screen, it is in the centre of the screen
                    

                    if Return_to_main_menu_button.draw():#restart button is drawn

                        world.data = []#clear world.data
                        level = 1
                        print ('Return to main menu')
                        difficulty_menu = True 

                        #add code to bring user to main menu


    for event in pygame.event.get(): #event loop

        if event.type == pygame.QUIT: #when the exit button  is clicked

            run = False #stop game loop
    
    pygame.display.update()#draws everything on to the screen 
    
pygame.quit()#exits pygame

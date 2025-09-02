#########################################################################################
                                     ###imports###
#########################################################################################

import pygame, sys # imports pyton modules
from pygame.locals import * # imports local variables from pygame
from movement_code_1 import * #imports all the code from movemetn_code_1

#########################################################################################
                                ###Window initializaton###
#########################################################################################

pygame.display.set_caption ('first prototype')#naming the window of the game
Clock = pygame.time.Clock()#Used for the framerate of the game so it runs smootly
pygame.init() #initiates pygame
Window_Size =(600,600)# pixel size for the window
screen = pygame.display.set_mode(Window_Size,0,32)#initiates the window
display = pygame.Surface((300,300)) # used as the surface for rendering, which is scaled

#########################################################################################
                                    ###Variables###
#########################################################################################

font = pygame.font.SysFont(None, 30) #this is used to define the font for the main menu

Set_of_Level = '1'
Level = '1'


click = False


#########################################################################################
                                ###Platform images###
#########################################################################################

Platform_img = pygame.image.load('Platform.png')#load the filename image into a variable
Platform_img.set_colorkey((255,255,255))#white pixels of the file are transparent
entrance_img = pygame.image.load('entrance.png')#load the filename image into a variable
entrance_img.set_colorkey((255,255,255))#white pixels of the file are transparent
exit_img = pygame.image.load('exit.png')#load the filename image into a variable
exit_img.set_colorkey((255,255,255))#white pixels of the file are transparent
big_block_img = pygame.image.load('big_block.png')#load the filename image into a variable
big_block_img.set_colorkey((255,255,255))#white pixels of the file are transparent
spikes_img = pygame.image.load('spikes.png')#load the filename image into a variable
spikes_img.set_colorkey((255,255,255))#white pixels of the file are transparent


#########################################################################################
                                 ###Level name images###
#########################################################################################

Level_img = pygame.image.load('Level.png')#load the filename image into a variable
One_img = pygame.image.load ('1.png')#load the filename image into a variable
Two_img = pygame.image.load ('2.png')#load the filename image into a variable
Three_img = pygame.image.load ('3.png')#load the filename image into a variable
Four_img = pygame.image.load ('4.png')#load the filename image into a variable
Five_img = pygame.image.load ('5.png')#load the filename image into a variable
Dash_img = pygame.image.load ('-.png')#load the filename image into a variable



player_img = pygame.image.load('player.png').convert()#load the player image
player_img.set_colorkey((255,255,255))#white pixels of the player are transparent
player_rect = pygame.Rect(32,264,16,24)#first two numbers are the players spawn point and the second two are the player's hit box
      


#########################################################################################
                                ###Functions###
#########################################################################################

def draw_text(text, font, color, surface, x, y): #this function is used to write 
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def load_map(path): #this function is used to open the file containing the map, read it and display it
    f = open(path + '.txt','r')#opens file
    data = f.read()#reads file
    f.close()#closes file
    data = data.split('\n')#splits the data into different lines
    game_map = []
    for row in data:#reads each line 
        game_map.append(list(row))#makes a list for each line
    
    tile_rects = []#An variable to hold all of platforms
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
            if tile == '5':
                display.blit(spikes_img,(x*16,y*16))#draw the Spikes if 5 and times by the pixel size
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the platforms hit box, the second pair being how big the hitbox is

                              ###Displaying the Level Name###

            if tile == '!':
                display.blit(Level_img,(x*16,y*16))#draw level if ! and times by the pixel size
                tile_rects.append(pygame.Rect(x*80,y*16,80,16))#the blocks hit box, the second pair being how big the hitbox is
            if tile == '-':
                display.blit(Dash_img,(x*16,y*16))#draw dash if - and times by the pixel size
                tile_rects.append(pygame.Rect(x*80,y*16,80,16))#the blocks hit box, the second pair being how big the hitbox is
            if tile == '[':
                if Set_of_Level == '1':
                    display.blit(One_img,(x*16,y*16))#draw 1 if set of level 1 and tile = [  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Set_of_Level == '2':
                    display.blit(Two_img,(x*16,y*16))#draw 2 if set of level 2 and tile = [  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Set_of_Level == '3':
                    display.blit(Three_img,(x*16,y*16))#draw 3 if set of level 3 and tile = [  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
            if tile == ']':
                if Level == '1':
                    display.blit(One_img,(x*16,y*16))#draw 1 if level 1 and tile = ]  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Level == '2':
                    display.blit(Two_img,(x*16,y*16))#draw 2 if level 2 and tile = ]  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Level == '3':
                    display.blit(Three_img,(x*16,y*16))#draw 3 if level 3 and tile = ]  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Level == '4':
                    display.blit(Four_img,(x*16,y*16))#draw 4 if level 4 and tile = ]  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
                if Level == '5':
                    display.blit(Five_img,(x*16,y*16))#draw 5 if level 5 and tile = ]  and times by the pixel size
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))#the blocks hit box, the second pair being how big the hitbox is
            x += 1
        y += 1

def main_menu():
    
    while True:
        
        display.fill((69,69,69))#fill the screen with the colour grey
        draw_text('Speedrun', font, (0, 0, 255), display, 125, 50)
 
        mx, my = pygame.mouse.get_pos()#mx and my are code knowing where the mouse is on the screen
 
        game_button = pygame.Rect(50, 100, 200, 25)#this is the image size for the game button
        action_guide_button = pygame.Rect(50, 200, 200, 25)#this is the image size for button 2

        
        if game_button.collidepoint((mx/2, my/2)):#if the mouse is on the game button
            if click:# if the mouse is clicked
                game()#the game function is called
        #if action_guide_button.collidepoint((mx/2, my/2)):
         #   if click:
                #options()
                #add action guide
        pygame.draw.rect(display, (255, 0, 0), game_button)# this is the hitbox for the game button
        pygame.draw.rect(display, (255, 0, 0), action_guide_button)# this is the hitbox for button 2
 
        click = False 
        
        for event in pygame.event.get(): #if any button on the keyboard/mouse is pressed 
            if event.type == QUIT: #if the quit button is pressed
                pygame.quit() #closes pygame
                sys.exit() #closes the window
            if event.type == KEYDOWN: #if a key on the keyboard is pressed
                if event.key == K_ESCAPE: #if esc is pressed
                    pygame.quit() #close pygame
                    sys.exit() #close the window
            if event.type == MOUSEBUTTONDOWN:#if a mouse button is pressed#
                if event.button == 1:#if the left side of the mouse is pressed
                    click = True

        screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
        pygame.display.update()#updates everthing on screen
        Clock.tick(60)#frame rate 60fps
        


def draw_background():

    true_scroll = [0,0]#sets the variable for how much the camera has moved

    display.fill((0,225,225))#fill screen with one colour

    background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,50,120,400]]]# first number is times by how far the camera has moved to make the effect that objects are moving in the background, rest of the numbers are the base data for the object

                                    ###Camera movement###
      
    true_scroll[0] += (player_rect.x-true_scroll[0]-208)/20#x-axis camera movement, the -152 is so it is at the centre of the screen, the /20 is for smoth camera movement
    true_scroll[1] += (player_rect.y-true_scroll[1]-192)/20#y-axis camera movement, the -112 is so it is at the centre of the screen, the /20 is for smoth camera movement
    scroll = true_scroll.copy()#changes scroll value into intergs for smooth moevement for the tiles
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

                                   ###Background Objects Part 2###

    for background_object in background_objects:#goes through the background_objects list
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])#the objects move slower in realtive to the first nummber in the background object data
        if background_object[0] == 0.5:#if the multiply is .5
            pygame.draw.rect(display,(34,139,34),obj_rect)#the colour will be a litter green
        else:
            pygame.draw.rect(display,(0,128,128),obj_rect)#if not the colour will be blue


def game():
    running = True
    while running:
        draw_background()#calls the draw background function
        load_map('Map_'+Set_of_Level+'-'+Level)#reads the file for the map
        #Player()
        for event in pygame.event.get(): #if any button on the keyboard/mouse is pressed 
            if event.type == QUIT: #if the quit button is pressed
                pygame.quit() #closes pygame
                sys.exit() #closes the window
            if event.type == KEYDOWN: #if a key on the keyboard is pressed
                if event.key == K_ESCAPE: #if esc is pressed
                    running = False
        
        
        screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
        pygame.display.update()#updates everthing on screen
        Clock.tick(60)#frame rate 60fps



main_menu()#calls the main menu function


#########################################################################################
                            ###Starting the game loop###
#########################################################################################

while True: #game loop


    

#########################################################################################
                            ###Physics for the Movement###
#########################################################################################

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

#########################################################################################
                       ###reading the key presses for movement###
#########################################################################################
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:#when a key is pressed once
            if event.key == K_RIGHT: #if the right key is pressed
                moving_right = True
            if event.key == K_LEFT: #if the left key is pressed
                moving_left = True
            if event.key == K_UP:#if the up key is pressed
                if air_timer < 6:#only jump when on the ground
                    vertical_momentum = -4
        if event.type == KEYUP:#when a key is stop being pressed
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT: 
                moving_left = False
                
#########################################################################################
                 ###updates the screen for the game to run###
#########################################################################################

    screen.blit(pygame.transform.scale(display,Window_Size),(0,0))#scale up and display the display to show on the window
    pygame.display.update()#updates everthing on screen
    Clock.tick(60)#frame rate 60fps

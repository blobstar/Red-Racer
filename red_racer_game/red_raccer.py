# a game where you are a red racecar dodging oilspills and hopefully making it to the finish line 
# game is won by hitting the finish line

import pygame
import random

pygame.init()  # initialize pygame
clock = pygame.time.Clock()
screen_width = 480
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height)) # This creates the screen and gives it the width and height specified as a 2 item sequence.
pygame.display.set_caption('Red Racer Game')
framerate = 60 # Set the framerate
time = clock.tick(framerate)/1000.0 # sets a timer - important for scrolling bg
pygame.mouse.set_visible(1) # makes the mouse visible over the game window

racer = pygame.image.load("racer.png") # player obj 

oilSpill = pygame.image.load("oil.png") # oil spill to avoid object
finLine = pygame.image.load("fin.png") # finish line that ends the game

racer_height = racer.get_height() # get the necessary height and width of the racer sprite 
racer_width = racer.get_width()

oil_height = oilSpill.get_height() # height and width of oil spill

oil_width = oilSpill.get_width()

racerXPosition = 240 # middle of the x-axis
racerYPosition = 460 # comfortable starting position

oilCount = 0 # this variable counts the oil spills generated (we want 3)
oilXPosition = random.randint(0, 480) # generates a random starting initial position
oilYPosition = 0 - oil_height # - oil_height makes oil generation more realistic

finXPosition = 0
finYPosition = -2100 # the finish line is the furthest object

damp = 30 / 100 # dampening factor for movement of background
bg_speed = 3 * damp # Set the background scrolling speed

keyLeft = False # set bools for key-press event listeners
keyRight = False
keyUp = False
keyDown = False
# i used this excellent tutorial for a scrolling background: https://www.activestate.com/blog/how-to-use-pygame-for-game-development/
# it tends to be a bit too fast hence i added the var 'damp' which acts as a dampener for speed
class ScrollingBackground:
    def __init__(self, screenheight, imagefile): # basically draws 2 backgrounds and moves them down
        self.img = pygame.image.load(imagefile)
        self.coord = [0, 0]
        self.coord2 = [0, -screenheight]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]
    
    def Show(self, surface):
        surface.blit(self.img, self.coord) # renders the moving bg
        surface.blit(self.img, self.coord2)

    def UpdateCoords(self, speed_y, time):
        distance_y = speed_y * time # classical mechanics formula for distance
        self.coord[1] += distance_y 
        self.coord2[1] += distance_y

        if self.coord2[1] >= 0: # resets the coords for bg
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original

Highway = ScrollingBackground(screen_height, "background.png") # set the image for the scrolling bg

# <--------BEGIN GAME LOOP +++++++>
while True:
    screen.fill(0) # this fills the screen with black to reset the screen
    Highway.UpdateCoords(bg_speed, time)

    Highway.Show(screen)
    screen.blit(racer, (racerXPosition, racerYPosition))# This draws the player image to the screen at the postion specfied. I.e. (100, 50).
    screen.blit(oilSpill, (oilXPosition, oilYPosition)) # renders an oil-spill
    
    screen.blit(finLine, (finXPosition, finYPosition))
    finYPosition += (0.5 * damp) # moves finish line down
    oilYPosition += (0.5 * damp) # moves the oilspill down

    playerBox = pygame.Rect(racer.get_rect()) # Bounding box for the player:
    playerBox.top = racerYPosition
    playerBox.left = racerXPosition
    
    oilBox = pygame.Rect(oilSpill.get_rect())# Bounding box for the oilSpill:
    oilBox.top = oilYPosition
    oilBox.left = oilXPosition

    finBox = pygame.Rect(finLine.get_rect()) # Bounding box for the finish line
    finBox.top = finYPosition
    finBox.left = finXPosition
    
    pygame.display.update()
    
    for event in pygame.event.get(): # press x to close
        if event.type == pygame.QUIT:
            pygame.quit()    
    
    if event.type == pygame.KEYDOWN: # The following conditions tests for wether we pressed the 'direction' keys    
        if event.key == pygame.K_RIGHT: # pygame.K_UP represents a keyboard key constant. 
            keyRight = True
        if event.key == pygame.K_LEFT:
            keyLeft = True
        if event.key == pygame.K_UP:
            keyUp = True
        if event.key == pygame.K_DOWN:
            keyDown = True
            
    if event.type == pygame.KEYUP: # This event checks if the key is up(i.e. not pressed by the user).
        if event.key == pygame.K_RIGHT:
            keyRight = False
        if event.key == pygame.K_LEFT:
            keyLeft = False
        if event.key == pygame.K_UP:
            keyUp = False
        if event.key == pygame.K_DOWN:
            keyDown = False

    if keyRight == True: # the followuning changes the players position based on keypress
        if racerXPosition < (480 - racer_width): # This makes sure that the user does not move the player to the right the window.
            racerXPosition += (1 * damp) # multiply by the dampening factor
    
    if keyLeft == True:
        if racerXPosition > 0:# This makes sure that the user does not move the player to the left the window.
            racerXPosition -= (1 * damp)
    
    if keyUp == True:
        if racerYPosition > 0: # stops player moving out the top
            racerYPosition -= (1 * damp)
    
    if keyDown == True:
        if racerYPosition < (640 - racer_height): # stops the player moving out the bottom
            racerYPosition += (1 * damp) 
   
    if (oilYPosition > 640) and (oilCount < 2): # checks to see if the oil spill has moved out of focus and counts oilspill
        oilYPosition = 0 - oil_height
        oilXPosition = random.randint(0, (480 - oil_width))
        oilCount += 1 

    if playerBox.colliderect(oilBox): # Lose condition = collision detection with oil spill
        print("You lose!") # Display losing status to the user: 
        pygame.quit() # Quit game and exit window: 
        exit(0)

    if playerBox.colliderect(finBox): # Win condition = hitting the finish line
        print("You Win!")# Display winning status to the user:  
        pygame.quit() # Quit game and exit window:
        exit(0)
# <--------FIN GAME LOOP +++++++>

# <----------Sources++++++++++++>
# dropBox example.py
# https://www.activestate.com/blog/how-to-use-pygame-for-game-development/ (for scrolling background)
# https://www.w3schools.com/python/ref_random_randint.asp (for random nums)
# https://www.pygame.org/docs/ref/key.html (for keys)
# https://www.reddit.com/r/pygame/comments/7lh9fq/what_are_the_ways_to_create_a_timer/ (for keeping track of time)
# all sprites/images used are my own
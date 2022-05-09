# Basic Pygame Structure

import pygame                               # Imports pygame and other libraries
import random

# Define Classes (sprites) here
class Balloon(pygame.sprite.Sprite):

    def __init__(self,x,y,direction,balloonType):
        pygame.sprite.Sprite.__init__(self)

        self.Direction = direction
        self.BalloonType = balloonType

        if balloonType == 1:
            balloonImage = pygame.image.load("RedBalloon.png")
            self.Speed = 3
            self.Score = 5
        if balloonType == 2:
            balloonImage = pygame.image.load("YellowBalloon.png")
            self.Speed = 7
            self.Score = 15
        if balloonType == 3:
            balloonImage = pygame.image.load("GreenBalloon.png")
            self.Speed = 5
            self.Score = 10
        if balloonType == 4:
            balloonImage = pygame.image.load("BlueBalloon.png")
            self.Speed = 10
            self.Score = 0

        self.image = pygame.Surface([26,50])
        self.image.set_colorkey(black)
        self.image.blit(balloonImage,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def moveBalloons(self):

        if self.Direction == "right":
            self.rect.x += self.Speed
        if self.Direction == "left":
            self.rect.x -= self.Speed

class Dart(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        dartImage = pygame.image.load("Dart.png")
        self.image = pygame.Surface([24,19])
        self.image.set_colorkey(black)
        self.image.blit(dartImage,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 388
        self.rect.y = 190

    def moveDart(self,mousePosition):
        self.rect.x = mousePosition[0]
        self.rect.y = mousePosition[1]

pygame.init()                               # Pygame is initialised (starts running)

screen = pygame.display.set_mode([800,400]) # Set the width and height of the screen [width,height]
pygame.display.set_caption("Balloon Burst")       # Name your window
background_image = pygame.image.load("SkyBackground.png").convert()
pygame.mouse.set_visible(False)
done = False                                # Loop until the user clicks the close button.
clock = pygame.time.Clock()                 # Used to manage how fast the screen updates
black    = (   0,   0,   0)                 # Define some colors using rgb values.  These can be
white    = ( 255, 255, 255)                 # used throughout the game instead of using rgb values.
font = pygame.font.Font(None, 36)

popSound = pygame.mixer.Sound("pop.wav")

otherBalloons = pygame.sprite.Group()
blueBalloons = pygame.sprite.Group()
allBalloons = pygame.sprite.Group()

timeTillNextBalloon = random.randint(1000,2000)
mousePosition = [0]*2
score = 0

dart = Dart()
darts = pygame.sprite.Group()
darts.add(dart)

# Define additional Functions and Procedures here

# -------- Main Program Loop -----------
while done == False:

    for event in pygame.event.get():        # Check for an event (mouse click, key press)
        if event.type == pygame.QUIT:       # If user clicked close window
            done = True                     # Flag that we are done so we exit this loop

        if event.type == pygame.MOUSEMOTION:
            mousePosition[:] = list(event.pos)
            dart.moveDart(mousePosition)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hitBalloons = pygame.sprite.groupcollide(blueBalloons,darts,False, False)
            if len(hitBalloons) > 0:
                done = True
            hitBalloons = pygame.sprite.groupcollide(otherBalloons,darts,False, False)
            for balloon in (hitBalloons):
                score += balloon.Score
                popSound.play()
            pygame.sprite.spritecollide(dart,allBalloons, True, collided = None)


    # Update sprites here
    if pygame.time.get_ticks() > timeTillNextBalloon:
        timeTillNextBalloon += random.randint(1000,5000)
        yCoord = random.randint(50,350)
        balloonType = random.randint(1,4)
        balloon = Balloon(0,yCoord,"right",balloonType)
        if balloonType >=1 and balloonType <=3:
            otherBalloons.add(balloon)
        else:
            blueBalloons.add(balloon)
        allBalloons.add(balloon)

    # Check if balloon sprites have reached edge of screen
    for balloon in (allBalloons.sprites()):
        if balloon.rect.x < 0:
            balloon.Direction = "right"
        if balloon.rect.x > 774:
            balloon.Direction = "left"

    # Move each balloon in the allBalloons group
    for balloon in (allBalloons.sprites()):
        balloon.moveBalloons()

    screen.blit(background_image, [0,0])
    allBalloons.draw(screen)
    darts.draw(screen)
    # Add the score to the screen
    textImg = font.render(str(score),1,white)
    screen.blit( textImg, (10,10) )

    pygame.display.flip()                   # Go ahead and update the screen with what we've drawn.
    clock.tick(20)                          # Limit to 20 frames per second

pygame.quit()                               # Close the window and quit.


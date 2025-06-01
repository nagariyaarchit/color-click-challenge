import pygame
import random
from game_engine import Game
from game_engine import Room
from game_engine import TextRectangle
from game_engine import GameObject
from game_engine import Alarm
global clickCounter

#Create a new Game
g = Game(640,480)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

#Create Resources
clickCounter = 0
simpleBackground = g.makeBackground(BLACK)
gameFont = g.makeFont("Arial",30)

#Initializing the rectangle top
expected_color = random.choice([WHITE, RED, BLUE, GREEN])

#Making different colour of circles
whiteCircleImage = g.makeCircle(10,WHITE)
RedCircleImage = g.makeCircle(10,RED)
BlueCircleImage = g.makeCircle(10,BLUE)
GreenCircleImage = g.makeCircle(10,GREEN)


#Create a Room
r1 = Room("Game",simpleBackground)
g.addRoom(r1)

r2 = Room("Game",simpleBackground)
g.addRoom(r2)

r3 = Room("Game",simpleBackground)
g.addRoom(r3)


#Classes for Game Objects
class ClickButton(TextRectangle):

        def __init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor):
                TextRectangle.__init__(self, text, xPos, yPos, font, textColor, buttonWidth, buttonHeight, buttonColor)


        def update(self):
                # Check for a mouse click
                self.checkMousePressedOnMe(event)
                

                # Update Game State when mousebutton released
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:

                        #go to the next room
                        g.nextRoom()
                        # Add the Alarm_game instance to room 2
                        if b.mouseHasPressedOnMe:
                                # Easy button pressed, set duration to 60 seconds
                                alarm_game_r2 = Alarm_game(duration=60000)  
                        else:
                                # Hard button pressed, set duration to 30 seconds
                                alarm_game_r2 = Alarm_game(duration=30000)  
                        r2.addObject(alarm_game_r2)

                        # Prevent multiple mouse clicks
                        self.mouseHasPressedOnMe = False

                        
#class for respective circles
class Circle(GameObject):
        def __init__(self, picture, xPos, yPos, color):
                GameObject.__init__(self,picture)

                self.rect.center = (xPos,yPos)
                self.color = color
                #Create an Alarm
                self.timer = Alarm()
                self.set_random_relocation_interval()
                
                
        def set_random_relocation_interval(self):
                # Set a random interval for each circle
                self.a = random.randint(800,2000)
                self.timer.setAlarm(self.a)

        
        #Update game State based on input states
        def update(self):
                global clickCounter

                if self.timer.finished():
                        # Relocate the circle
                        self.relocate()
                        # Set a new random relocation interval
                        self.set_random_relocation_interval()

                        
                #Check for a mouse click
                self.checkMousePressedOnMe(event)
                
                #Update Game State when mousebutton released
                if self.mouseHasPressedOnMe and event.type == pygame.MOUSEBUTTONUP:
                        if self.color == expected_color:
                                clickCounter = clickCounter + 1
                                self.kill()
                        else:
                                clickCounter = 0
                                
                        rectanglePlatform.setText(str(clickCounter))
                        self.mouseHasPressedOnMe = False

        #relocating the circle
        def relocate(self):
                # Change the circle's position to a new random location
                self.rect.x = random.randint(20, g.windowWidth - 20)
                self.rect.y = random.randint(60, g.windowHeight - 20)
                

class Alarm_game(GameObject):
        
        def __init__(self, duration):
                GameObject.__init__(self)
                self.timer = Alarm()
                self.timer.setAlarm(duration)
                print("timer.set")
                
        def update(self):
                if self.timer.finished():
                        print("timer finished")
                        rectanglePlatform_r3.setText(str(clickCounter))
                        g.nextRoom()
                
                     
        
#Initialize objects and add to room
b = ClickButton("Easy", 240, g.windowHeight - 300, gameFont, BLACK, 150, 40, WHITE)
r1.addObject(b)

y = ClickButton("Hard", 240, g.windowHeight - 240, gameFont, BLACK, 150, 40, WHITE)
r1.addObject(y)

title = TextRectangle("GAME",10,10, gameFont, WHITE)
r1.addObject(title)


clickedTimes1 = TextRectangle("Hard mode is thrice as harder than easy mode",10,50, gameFont, WHITE)
r1.addObject(clickedTimes1)

#sending the colour generated for counting the circles
rectanglePlatform = TextRectangle("0",0,0,gameFont,BLACK,g.windowWidth,40,expected_color)
r2.addObject(rectanglePlatform)


#Initialize objects for the second room
circles = []
for i in range(0,43):
        x = random.randint(20,g.windowWidth-20)
        y = random.randint(60,g.windowHeight-20)
        white = Circle(whiteCircleImage, x, y, WHITE)
        circles.append(white)
        r2.addObject(white)
        
for i in range(0,43):
        x = random.randint(0,g.windowWidth-20)
        y = random.randint(60,g.windowHeight-20)
        red = Circle(RedCircleImage, x, y, RED)
        circles.append(red)
        r2.addObject(red)
        
for i in range(0,43):
        x = random.randint(20,g.windowWidth-20)
        y = random.randint(60,g.windowHeight-20)
        blue = Circle(BlueCircleImage, x, y, BLUE)
        circles.append(blue)
        r2.addObject(blue)
        
for i in range(0,43):
        x = random.randint(20,g.windowWidth-20)
        y = random.randint(60,g.windowHeight-20)
        green = Circle(GreenCircleImage, x, y, GREEN)
        circles.append(green)
        r2.addObject(green)
        
# Creating a new TextRectangle for room 3
rectanglePlatform_r3 = TextRectangle("0", 0, 0, gameFont, BLACK, g.windowWidth, 40, expected_color)
r3.addObject(rectanglePlatform_r3)

        
#Start Game
g.start()


while g.running :

        #How often the game loop executes each second
        dt = g.clock.tick(60)

        #Check Events
        for event in pygame.event.get():

                #Check for [x]
                if event.type == pygame.QUIT:
                        g.stop()

        #Update All objects in Room
        g.currentRoom().updateObjects()

        #updating the circles
        for circle in circles:
                circle.update()

        #Render Background to the game surface
        g.currentRoom().renderBackground(g)

        #Render Objects to the game surface
        g.currentRoom().renderObjects(g)

        #Draw everything on the screen
        pygame.display.flip()



pygame.quit()

       


import contextlib
import os
import sys
from pynput.keyboard import Key, Listener
with contextlib.redirect_stdout(None):
    import pygame
 
print("please Visit www.girrafee2d.com for more")
class App():
    pygame.init()
    
    def RenderWindow(self, width, height):
        global gameDisplay
        gameDisplay = pygame.display.set_mode((width, height))
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
         
    def Update(self):
        pygame.display.update()
         
    def FPS(self, amount):
        clock = pygame.time.Clock()
        clock.tick(amount)
         
    def SetTitle(self, title):
        pygame.display.set_caption(title)
         
    def Fill(self, color):
        gameDisplay.fill(color)
         
    def get_display():
        return gameDisplay
     
    def SetIcon(self, path):
        myIcon = pygame.image.load(path)
        pygame.display.set_icon(myIcon)
        
class Event():
    pygame.init()
    def type(self, myEvent):
        if myEvent == "QUIT":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
     
    
class Sprite():
     def  __init__(self):
        pygame.init()
        pygame.sprite.Sprite()
    
     def DrawRect(self, color, sizeX, sizeY, posX, posY):
         self.color = color
         self.sizeX = sizeX
         self.sizeY = sizeY
         self.posX = posX
         self.posY = posY
         layout = App()
         pygame.draw.rect(App.get_display(), self.color, [self.posX, self.posY, self.sizeX, self.sizeY])
     def getPosX(self):
        pass
class Keyboard():
    def checkForInput(self, key):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if key == "left" and event.key == pygame.K_LEFT:
                    return True
                else:
                    print("bitch")

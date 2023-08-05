import contextlib
import math
import os


print("Please Visit www.GiraffeGameEngine.io for more info")
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    from pytmx import load_pygame
    
    
    




class App():
    def __init__(self):
        pygame.init()
        
    def RenderWindow(self, width, height):
        global gameDisplay
        gameDisplay = pygame.display.set_mode((width, height))
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon = pygame.image.load("../Sprites/icon.png")
        pygame.display.set_icon(icon)
        

    def SetAssetsFolder(self):
        pass
    
    
    def Update(self):
        pygame.display.update()
        pygame.display.flip()

        
    def FPS(self, amount):
        clock = pygame.time.Clock()
        clock.tick(amount)

        
    def SetTitle(self, title):
        pygame.display.set_caption(title)

        
    def Fill(self, color):
        gameDisplay.fill(color)

        
    def get_display(self):
        return gameDisplay

    def SetIcon(self, path):
        myIcon = pygame.image.load(path)
        pygame.display.set_icon(myIcon)
        
    def quit(self):
        pygame.quit()
        quit()
        
class Event():
    def __init__(self):
        pygame.init()
        self.close = False
    
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.close = True
    
    
    
            
class Sprite(pygame.sprite.Sprite):
    def  __init__(self, path):
        pygame.init()
        self.image = pygame.image.load(path).convert()
        self.rect = self.image.get_rect()
        

    
    def LookAtMouse(self):
        x,y = pygame.mouse.get_pos()
        rel_x = x - self.posX
        rel_y = y - self.posY
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(App.get_display(self), angle)
       
    
    def PlaceImage(self, x, y):
        self.x = x
        self.y = y
        pygame.Surface.blit(App.get_display(self),self.image, (self.x, self.y))
    

        
class TileMap(pygame.sprite.Sprite):
    def __init__(self, path, SplitX, SplitY):
        gameMap = pytmx.TiledMap(path)
        Tiles = gameMap.get_tile_image(0, 0, 0)
        pygame.Surface.blit(App.get_display(self),Tiles,(SplitX, SplitY))
    
        
    
    
    



    
class Draw():
    def DrawRect(self, color, sizeX, sizeY, posX, posY):
            self.color = color
            self.sizeX = sizeX
            self.sizeY = sizeY
            self.posX = posX
            self.posY = posY
            pygame.draw.rect(App.get_display(self), self.color, [self.posX, self.posY, self.sizeX, self.sizeY])
    def DrawCircle(self):
        
        pass
    def DrawPolygon(self):
        pass
    def DrawTriangle(self):
        pass
    def DrawLine(self):
        pass
    

class Keyboard():
    def __init__(self):
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.moveLeft = True
        if keys[pygame.K_RIGHT]:
            self.moveRight = True
        if keys[pygame.K_UP]:
            self.moveUp = True
        if keys[pygame.K_DOWN]:
            self.moveDown = True
    def CheckKey(self, key):
        self.checkKey = False
        self.key = key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ("pygame.",key):
                    Self.checkKey = True
                else:
                    self.checkKey = False
        

class Vector2D(pygame.math.Vector2):
    def __init__(self, *args, **kwargs):
        pygame.math.Vector2.__init__(self, *args, **kwargs)
        
    
class Color():
    def __init__(self):
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
    def COLOR(self):
        pass

class Sound():
    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(path)
    def play(self, volume, RepeatRate):
        pygame.mixer.Sound.play(RepeatRate)
        pygame.mixer.Sound.set_volume(10)

    def pause(self):
        pygame.mixer.pause()
    def unpause(self):
       pygame.mixer.pause()

class Music():
    def __init__(self, path):
        pygame.init()
        pygame.mixer.init()
    def play(self):
        pygame.mixer.Music.play(RepeatRate)
        pygame.mixer.Music.set_volume(10)
    def Pause(self):
        pygame.mixer.pause()
    def Unpause(self):
        pygame.mixer.unpause()
        
        

class Physics2D():
    def __init__(self):
        pass

    
        
            
                    
    
             


     


    



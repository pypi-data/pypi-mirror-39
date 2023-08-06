import contextlib
import math
import os
import wget
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    from pytmx.util_pygame import load_pygame


print("Please Visit www.GiraffeGameEngine.io for more info")
print(os.getcwd())
print(__file__)

    
    
class App():
    _count = 0

    def __init__(self):
        pygame.init()
        _count += 1

        if _count is 1:
            url = "https://www.brandcrowd.com/gallery/brands/pictures/picture14107731716699.jpg"
            self.extension = "png"
            wget.download(url, ("{0}/../Sprites/icon.{1}").format(os.getcwd(), extension))
            iconPath = ("{0}/../Sprites/icon.{1}").format(os.getcwd(), extension)
            icon = pygame.image.load(iconPath)
            pygame.display.set_icon(icon)
        if _count is 2:
            return True
            
        
    def __del__(self):
        _count -= 1
        
    def RenderWindow(self, width=640, height=480, title="Giraffe2D Window"):
        global gameDisplay
        gameDisplay = pygame.display.set_mode((width, height))
        gameTitle = pygame.display.set_caption(title)

      
    
    def DoNotUse(self):
        os.mkdir("Sprites")
        os.mkdir("Sounds")
        os.mkdir("Models")
        
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
    def ExtentionDownload(self,ext):
        self.extension = ext

    @classmethod
    def get_display(self):
        return gameDisplay

    def SetIcon(self, path):
        myIcon = pygame.image.load(path)
        pygame.display.set_icon(myIcon)
        
    def quit(self):
        pygame.quit()
        
       
        
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
        angle = math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(App.get_display(self), angle)
       
    
    def PlaceImage(self, x, y):
        self.x = x
        self.y = y
        pygame.Surface.blit(App.get_display(self),self.image, (self.x, self.y))

        

class Tilemap():
    def __init__(self,x,y):
        tmx_data = load_pygame('GameMap.tmx')
    def UseTiles(self):
        pygame.Surface.blit(App.get_display(self),tmx_data, (x, y))
        
        


class Keyboard(object):
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
    def COLOR(self, color):                                         
        self.color = color
        return color                                                   

                    
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
    def play(self, Music, Volume, RepeatRateVolume):
        pygame.mixer.Music.play(RepeatRateVolume)
        pygame.mixer.Music.set_volume(Volume)
    def Pause(self):
        pygame.mixer.pause()
    def Unpause(self):
        pygame.mixer.unpause()
        
        

class Physics2D():
    def __init__(self):
        pass

    
        
            
                    
    
             


     


    



import pygame
import os


class Pipe:
    
    def __init__(self, screen, cords, width, height, color, speed, is_top=False):
        
        self.screen = screen
        self.x, self.y = cords
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        
        self.is_top = is_top
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.passed = False
        
        
        
        if not self.is_top:
            self.image = pygame.image.load(os.path.join(os.getcwd(), 'images', 'pipe-down.png'))
        else:
            self.image = pygame.image.load(os.path.join(os.getcwd(), 'images', 'pipe-top.png'))
        
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

    
    def move(self):
        self.rect.move_ip(-self.speed, 0)
        self.x = self.rect.x
        
    
    def is_off_screen(self):
        return self.x + self.width < 0
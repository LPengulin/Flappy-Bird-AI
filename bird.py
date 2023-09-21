import pygame
import os


class Bird:
    
    def __init__(self, screen, color, center, radius):
        
        self.screen = screen
        self.color = color
        self.x, self.y = center
        self.radius = radius
        self.velocity = 0
        
        #hitbox
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.image = os.path.join(os.getcwd(), 'images', 'bird.png')
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, (4 * self.radius, 4 * self.radius))
    
    def draw(self):
        #uncomment below to draw hitbox
        #pygame.draw.rect(self.screen, (0, 255, 255), self.rect)
        
        self.screen.blit(self.image, self.rect.topleft)
        
        
    
    def move(self, dx, dy):
        #moving the bird on the given delta
        self.x += dx
        self.y += dy
    
    
    def get_current_position(self):
        return self.x, self.y
        
    
    def apply_gravity(self, gravity):
        self.velocity += gravity
        self.y += self.velocity
        self.rect.y = self.y - self.radius
        
    def jump(self, force):
        self.velocity = -force 
        
    
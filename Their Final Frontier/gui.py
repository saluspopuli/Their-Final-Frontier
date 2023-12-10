import pygame

class UI:
    def __init__(self, x, y, image, scale):
        self.width = scale
        self.height = scale
        self.x = x
        self.y = y
        self.image = image
        
        self.scaled_image = pygame.transform.scale(self.image,(self.width, self.height))
    
    def render(self, screen):
        screen.blit(self.scaled_image, (self.x, self.y))
        
    
class Bullet_UI(UI):
    def __init__(self, x, y, scale):
        
        image = pygame.image.load(r"assets\UI\bullet.png")
        
        super().__init__(x, y, image, scale)
    
class Waypoint_UI(UI):
    def __init__(self, x, y, scale):
        
        image = pygame.image.load(r"assets\UI\waypoint.png")
        
        super().__init__(x, y, image, scale)
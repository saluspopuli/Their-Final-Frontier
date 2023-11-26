import pygame
import math

# Import the entity class
from entity import Entity

class Ship(Entity):
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=0, direction=0, turn_velocity= 1):
        image = pygame.image.load("assets\ship\ship.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.turn_velocity = turn_velocity


    def update(self):
        pass
    
            
    def pull(self, direction, velocity):
        
        dir_radians = -math.radians(direction+90)
        
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
            
            
        

        
        

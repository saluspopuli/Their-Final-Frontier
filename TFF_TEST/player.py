import pygame
import math

# Import the entity class
from entity import Entity

class Player(Entity):
    
    acceleration = 0.0001
    deceleration = 0.00005
    velocity_cap = 0.1
    tmp_rad = 0
    dir_cos = 0
    dir_sin = 0
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=0, direction=0, turn_velocity= 0.05):
        super().__init__(x, y, width, height, velocity, direction)
        self.turn_velocity = turn_velocity

        self.image = pygame.image.load("assets\player\player.png")


    def update(self):
        keys = pygame.key.get_pressed()
        
        dir_radians = -math.radians(self.direction+90)
        
        if (dir_radians != self.tmp_rad):
            self.dir_cos = math.cos(dir_radians)
            self.dir_sin = math.sin(dir_radians)
            self.tmp_rad = dir_radians
        
        if keys[pygame.K_w]: #forward movement
            self.velocity += self.acceleration          

        if keys[pygame.K_s]: #backwards movement
            self.velocity -= self.acceleration
        
        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin    
        
        if self.velocity != 0:
            self.velocity -= self.deceleration * (self.velocity / abs(self.velocity))
        
        if abs(self.velocity) > self.velocity_cap:
            self.velocity = self.velocity_cap * (self.velocity / abs(self.velocity))
          
        if keys[pygame.K_a]:
            self.direction += self.turn_velocity
            
        if keys[pygame.K_d]:
            self.direction -= self.turn_velocity


            
            
        

        
        

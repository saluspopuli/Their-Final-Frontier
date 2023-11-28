import pygame
import math

# Import the entity class
from entity import Entity

class Player(Entity):
    
    acceleration = 0.1
    deceleration = acceleration/3
    velocity_cap = 2
    tmp_rad = 0
    dir_cos = 0
    dir_sin = 0
    spacebar_pressed = False
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity = 0, direction=0, turn_velocity= 1):
        image = pygame.image.load("assets\player\player.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.turn_velocity = turn_velocity


    def update(self):
        # Puts keys pressed in a keys list
        keys = pygame.key.get_pressed()
        
        # Calculates player direction in radians
        dir_radians = -math.radians(self.direction+90)
        
        # If the direction has not changed, do not recalculate
        if (dir_radians != self.tmp_rad):
            self.dir_cos = math.cos(dir_radians)
            self.dir_sin = math.sin(dir_radians)
            self.tmp_rad = dir_radians
        
        if keys[pygame.K_w]: #forward movement
            self.velocity += self.acceleration          

        if keys[pygame.K_s]: #backwards movement
            self.velocity -= self.acceleration
        
        # Calculates new location based on velocity and direction
        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin    
        
        # This if block decelerates the player
        if self.velocity != 0:      
            self.velocity -= self.deceleration * (self.velocity / abs(self.velocity))
            
            # Because of float imprecision and whatnot, I just set velocity to zero
            # when it is really close to zero
            if abs(self.velocity) < 0.0005:
                self.velocity = 0
        
        # Ensures that velocity does not go beyond the player's velocity cap
        if abs(self.velocity) > self.velocity_cap:
            self.velocity = self.velocity_cap * (self.velocity / abs(self.velocity))
        
        # Turns the player left or right depending on key pressed
        # (Might change it to acceleration based in future?)  
        if keys[pygame.K_a]:
            self.direction += self.turn_velocity
            
        if keys[pygame.K_d]:
            self.direction -= self.turn_velocity


    # Pulls the player towards a specified angle
    def pull(self, direction, velocity):
        
        dir_radians = -math.radians(direction+90)
        
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
            
            
        

        
        

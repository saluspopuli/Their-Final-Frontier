import pygame
from entities.entity import Entity
import math

class Particles(Entity):
    
    def __init__(self, x, y, width, height, direction, velocity, color):
        
        super().__init__(x, y, width, height, direction, image = 0, collision_box = 0, has_collision = False)
        
        self.velocity = velocity
        
        dir_radians = math.radians(self.direction)+180
        
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
        
        info = pygame.display.Info()
        self.screenX, self.screenY = info.current_w, info.current_h
        
        self.color = color
        pass
    
    def update(self):

        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin
        
        if self.x > self.screenX+100 or self.x < -100 or self.y > self.screenY+100 or self.y < -100:
            self.lives = 0
        
        pass
    
    def render(self, screen):
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.width/2)
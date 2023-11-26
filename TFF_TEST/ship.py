import pygame
import math

from entity import Entity
from lagrange import Lagrange

class Ship(Entity):
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0):
        image = pygame.image.load("assets\ship\ship.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.lagrange = lagrange


    def update(self):
        x,y = pygame.mouse.get_pos()
        self.move_ship(x,y)
        
        
    def move_ship(self, target_x, target_y):
        # Calculate the direction to target
        dx = target_x - self.x
        dy = target_y - self.y

        direction = math.degrees(math.atan2(dy, dx))
        self.direction = -direction - 90
        
        dir_cos = math.cos(math.radians(direction))
        dir_sin = math.sin(math.radians(direction))
        
        self.x += self.velocity * dir_cos
        self.y += self.velocity * dir_sin

    def pull(self, direction, velocity):
        dir_radians = -math.radians(direction+90)
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
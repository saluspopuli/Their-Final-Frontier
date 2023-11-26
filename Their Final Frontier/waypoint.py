import pygame
import math

from entity import Entity
from lagrange import Lagrange

class Waypoint(Entity):
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0):
        image = pygame.image.load("assets\waypoint\waypoint.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.lagrange = lagrange


    def update(self):
        pass

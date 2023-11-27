import pygame
import math

from entity import Entity
from lagrange import Lagrange

class Ship(Entity):
    
    waypoint_line = [0]
    moving_flag = False
    tmp_x = 0
    lagrange_points = 5
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0):
        image = pygame.image.load("assets\ship\ship.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.lagrange = lagrange


    def update(self):  #TODO: change this, testing code only
        
        if self.moving_flag:
            self.tmp_x +=0.5    
            self.move_ship(self.tmp_x,self.lagrange.lagrange(self.x,self.lagrange_points))
        pass  
        
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
    
    def change_lagrange_points(self, dir, screenX):
        if dir:
            self.lagrange_points += 1
        else:
            self.lagrange_points -= 1
        
        self.draw_waypoint_line(screenX)
    
    def draw_waypoint_line(self, screenX):
        self.waypoint_line = []
        for x in range(screenX): #change the range puhon
            self.waypoint_line.append(self.lagrange.lagrange(x,self.lagrange_points))

    def render(self, screen):
        
        for x in range(len(self.waypoint_line)):
            pygame.draw.circle(screen, (255,255,255), (x,self.waypoint_line[x]), 2)
            
        rotated_image = pygame.transform.rotate(self.scaled_image, self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
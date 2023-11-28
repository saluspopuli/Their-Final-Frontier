import pygame
import math

from entity import Entity
from lagrange import Lagrange

class Ship(Entity):
    
    waypoint_line = [(0,0)]
    waypoint_step = 5
    lagrange_points = 5
    waypoint_line_render_index = 1
    follow_index = 0
    
    moving_flag = False
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0):
        image = pygame.image.load("assets\ship\ship.png")       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity
        self.lagrange = lagrange


    def update(self):  #TODO: change this, testing code only 
        
        if self.follow_index >= len(self.waypoint_line):
            self.follow_index = len(self.waypoint_line) - 1
            
        if self.moving_flag:
            tmpcoord = self.waypoint_line[self.follow_index]
            self.move_ship(tmpcoord[0],tmpcoord[1])
            
            if (self.x - tmpcoord[0]) > -0.1:
                self.follow_index += 1
        
    def move_ship(self, target_x, target_y):
        
        # Gets the distance between target x y and current x y
        dx = target_x - self.x
        dy = target_y - self.y

        # Calculates direction towards target
        direction = math.degrees(math.atan2(dy, dx))
        # Changes face direction of the sprite
        self.direction = -direction - 90
        
        dir_cos = math.cos(math.radians(direction))
        dir_sin = math.sin(math.radians(direction))
        
        self.x += self.velocity * dir_cos
        self.y += self.velocity * dir_sin

    # Pulls the player towards a specified angle
    def pull(self, direction, velocity):
        dir_radians = -math.radians(direction+90)
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
    
    # Mostly a debug function that dynamically changes the amount of lagrange points
    # that are considered
    def change_lagrange_points(self, dir, screenX):
        if dir:
            self.lagrange_points += 1
        else:
            self.lagrange_points -= 1
        
        self.draw_waypoint_line(screenX)
    
    def draw_waypoint_line(self, screenX):
        # Empties the waypoint line array
        self.waypoint_line = []
        
        # Creates a list of points from the left side of the screen to the right side
        # with a step of waypoint_step (because I don't need to generate points for
        # every x value)
        for x in range(0, screenX + 200, self.waypoint_step):
            self.waypoint_line.append((x,self.lagrange.lagrange(x,self.lagrange_points)))
               
    def render(self, screen):
        
        # Draws lines from x-1 point to x point for all lines in the waypoint_line list.
        # Obviously, it cannot start at zero because x-1 would not exist then
        for i in range(1, len(self.waypoint_line)):
            x = self.waypoint_line[i]
            x_prev = self.waypoint_line[i-1]
            
            #pygame.draw.circle(screen, (255,255,255), (x[0], x[1]), 2)
            pygame.draw.line(screen, (255,255,255), (x_prev[0], x_prev[1]), (x[0], x[1]), 3)
        
        # TODO: probably just delete this
        # Goes across the entire waypoint list and changes one line into green for a single
        # frame to create a small pulsing animation 
        if self.waypoint_line_render_index < len(self.waypoint_line):
            x = self.waypoint_line[self.waypoint_line_render_index]
            x_prev = self.waypoint_line[self.waypoint_line_render_index-1]
            
            pygame.draw.line(screen, (0,255,0), (x_prev[0],x_prev[1]), (x[0], x[1]), 8)
            self.waypoint_line_render_index += 1
        
        else:
            self.waypoint_line_render_index = 1
        
        # Renders the ship image normally       
        rotated_image = pygame.transform.rotate(self.scaled_image, self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
import pygame
import math
import random

from entities.entity import Entity

class Ship(Entity):
    
    waypoint_step = 5
    lagrange_points = 3
    waypoint_line_render_index = 1
    follow_index = 0
    
    can_move = True
    moving_flag = False
    
    collision_max_shake_frame = 15
    collision_shake_frame = collision_max_shake_frame
    
    collision_max_cooldown = 60*4
    collision_cooldown_frame = 0
    
    line_color = (201, 49, 32)
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0, has_collision = True):
        
        tmp_collision = 0
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width-(width * 0.4), height- (width * 0.4))    
            
        image = pygame.image.load("assets\ship\ship1.png").convert_alpha()       
        super().__init__(x, y, width, height, direction, image, tmp_collision, True)
        self.velocity = velocity
        self.lagrange = lagrange
        
        self.load_sprites("assets\ship")
        
        self.waypoint_line = [(0,0)]
        self.tmp_waypoint_line = []
        
        self.lives = 4
        
        self.state = 0
        self.state_save = 0
        
        self.checking = False
        self.font_small = pygame.font.Font(r"assets\font\nine0.ttf", 25)
        self.font_small.bold = True


    def update(self):
        
        self.state = self.state_save + 1 #State thing
        
        self.collision_box.center = (self.x, self.y)
        
        if self.can_move:
            self.state = self.state_save + 2
            pass
            
        if self.can_move and len(self.waypoint_line) < 5:
            
            if self.moving_flag:
                info = pygame.display.Info()
                self.move_ship(info.current_w + 300, info.current_h/2)
                
        elif self.can_move:
            
            if self.follow_index >= len(self.waypoint_line):
                self.follow_index = len(self.waypoint_line) - 1
                
            if self.moving_flag:
                tmpcoord = self.waypoint_line[self.follow_index]
                self.move_ship(tmpcoord[0],tmpcoord[1])
                
                if (self.x - tmpcoord[0]) > -0.1:
                    self.follow_index += 1
        else:
            self.collision_cooldown_frame += 1
            
            if self.collision_cooldown_frame >= self.collision_max_cooldown:
                self.collision_cooldown_frame = 0
                self.can_move = True
        
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
        dir_radians = -math.radians(direction)
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
    
    def handle_collision(self, entity):
        self.sound.play()
        self.can_move = False
        self.collision_shake_frame = 0 
    
        if self.collision_cooldown_frame == 0:
            self.state_save += 2 #State function
            self.lives -= 1
    
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
    
    def init_tmp_waypoint_line(self, screenX):
        for x in range(0, screenX + 200, self.waypoint_step):
            self.tmp_waypoint_line.append([x,-10])
                 
    def render(self, screen):
        
        if len(self.waypoint_line) == len(self.tmp_waypoint_line):
            for i in range(0, len(self.tmp_waypoint_line)):
                self.tmp_waypoint_line[i][1] -= (self.tmp_waypoint_line[i][1] - self.waypoint_line[i][1])/5
            
            # Draws lines from x-1 point to x point for all lines in the waypoint_line list.
            # Obviously, it cannot start at zero because x-1 would not exist then    
            for i in range(1, len(self.tmp_waypoint_line)):
                
                if (i%2 == 0):
                    x = self.tmp_waypoint_line[i]
                    x_prev = self.tmp_waypoint_line[i-1]
                    
                    
                    #pygame.draw.circle(screen, (255,255,255), (x[0], x[1]), 2)
                    pygame.draw.line(screen, self.line_color, (x_prev[0], x_prev[1]), (x[0], x[1]), 3)
        
        # TODO: probably just delete this
        # Goes across the entire waypoint list and changes one line into green for a single
        # frame to create a small pulsing animation 
        if self.waypoint_line_render_index < len(self.waypoint_line):
            x = self.waypoint_line[self.waypoint_line_render_index]
            x_prev = self.waypoint_line[self.waypoint_line_render_index-1]
            
            pygame.draw.circle(screen, self.line_color, x,4)
            pygame.draw.circle(screen, self.line_color, x_prev,2)
            
            if self.checking:
                text = self.font_small.render("({:.3f}, {:.3f})".format(x[0], x[1]), True, (0, 255, 0))
                screen.blit(text, (x[0], x[1]))
            
            pygame.draw.line(screen, self.line_color, (x_prev[0],x_prev[1]), (x[0], x[1]), 8)
            self.waypoint_line_render_index += 1
        
        else:
            self.waypoint_line_render_index = 1
        
        # Renders the ship image normally
        if self.collision_shake_frame <= self.collision_max_shake_frame:
            self.collision_shake_frame += 1
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x + random.randrange(-2,2), self.y + random.randrange(-2,2)))
        else:       
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_image, rotated_rect)
        
        #DEBUG RENDERING
        #pygame.draw.rect(screen,(0,255,0) ,self.collision_box)
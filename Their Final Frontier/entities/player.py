import pygame
import math
import random

# Import the entity class
from entities.entity import Entity

class Player(Entity):
    
    acceleration = 0.1
    deceleration = acceleration/3
    velocity_cap = 2
    tmp_rad = 0
    dir_cos = 0
    dir_sin = 0
    spacebar_pressed = False
    
    can_move = True
    
    collision_max_frames = 60*3
    collision_frame_counter = 0
    
    collision_max_shake_frame = 15
    collision_shake_frame = collision_max_shake_frame
    
    collision_max_cooldown_frame = 60*3
    collision_cooldown_frame = 30
    
    def __init__(self, 
                 x=0, 
                 y=0, 
                 width=50, 
                 height=50, 
                 velocity = 0, 
                 direction=0, 
                 turn_velocity= 1.3,
                 has_collision = True,
                 waypoints = 4,
                 bullets = 6):
        
        image = pygame.image.load("assets\player\player1.png")
        
        tmp_collision = 0
        collision_box_scale = 0.6
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width*collision_box_scale, height*collision_box_scale)     
        
        super().__init__(x, y, width, height, direction, image, tmp_collision, True)
        
        self.scaled_image = []
        self.load_sprites("assets\player")
        
        self.lives = 3
        
        self.velocity = velocity
        self.turn_velocity = turn_velocity
        
        self.weight = 1.5
        
        self.bullets = bullets
        self.waypoints = waypoints
        
        self.state_save = self.state
        
        self.start_frame = 0
        self.max_start_frame = 60

    def update(self):
        
        
        self.state = self.state_save
        
        self.collision_box.center = (self.x, self.y)
        
        # Puts keys pressed in a keys list
        keys = pygame.key.get_pressed()
        
        # Calculates player direction in radians
        dir_radians = -math.radians(self.direction+90)
        
        # If the direction has not changed, do not recalculate
        if (dir_radians != self.tmp_rad):
            self.dir_cos = math.cos(dir_radians)
            self.dir_sin = math.sin(dir_radians)
            self.tmp_rad = dir_radians
        
        if self.start_frame < self.max_start_frame:
            self.start_frame += 1
            self.velocity += self.acceleration
            self.state = self.state_save + 1
            
        elif self.can_move:
            if keys[pygame.K_w]: #forward movement
                self.state = self.state + 1
                self.velocity += self.acceleration          

            if keys[pygame.K_s]: #backwards movement
                self.state = self.state + 1
                self.velocity -= self.acceleration
                
            # Turns the player left or right depending on key pressed
            # (Might change it to acceleration based in future?)  
            if keys[pygame.K_a]:
                self.direction += self.turn_velocity
                
            if keys[pygame.K_d]:
                self.direction -= self.turn_velocity
            
        elif self.collision_frame_counter < self.collision_max_frames:
            self.collision_frame_counter += 1
        else:
            self.collision_frame_counter = 0
            self.can_move = True
        
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
            
        if self.collision_cooldown_frame > 0:
            self.collision_cooldown_frame -= 1
        

    def handle_collision(self, entity):
        from entities.bullet import Bullet
        
        if not isinstance(entity, Bullet):
            dx = entity.x - self.x
            dy = entity.y - self.y

            direction = math.degrees(math.atan2(dy, dx))
            
            self.pull(-direction, -5)
            self.velocity = -self.velocity/2
            
            self.can_move = False
            
            self.collision_shake_frame = 0
                      
        else:
            self.collision_shake_frame = self.collision_max_shake_frame/4
        
        if self.collision_cooldown_frame == 0:
            if not isinstance(entity, Bullet):
                self.state_save += 2
                self.lives -= 1     
                self.collision_cooldown_frame = self.collision_max_cooldown_frame
    
    
    # Pulls the player towards a specified angle
    def pull(self, direction, velocity):
        
        dir_radians = -math.radians(direction)
        
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
    
    def render(self, screen):
        
        if self.collision_shake_frame <= self.collision_max_shake_frame:
            self.collision_shake_frame += 1
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x + random.randrange(-2,2), self.y + random.randrange(-2,2)))
        else:
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_image, rotated_rect)
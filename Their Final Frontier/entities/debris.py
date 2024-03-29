import pygame
import math
from entities.entity import Entity

class Debris(Entity):
    
    collide_direction = 0
    collide_velocity = 0
    is_collided = False
    
    def __init__(self, x, y, width, height, direction, image, has_collision, turn_speed, turn_direction):    
        
        self.velocity = 0
        self.turn_speed = turn_speed/100
        self.sprite_direction = 0
        
        if turn_direction:
            self.turn_speed = -self.turn_speed
            
        tmp_collision = 0
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width-(width * 0.4), height- (width * 0.4))
        
        image = pygame.image.load(image).convert_alpha()
        
        super().__init__(x, y, width, height, direction, image, tmp_collision, has_collision)
        
        self.lives = int(1 + ((height-50)/10))
        
    def update(self):
            
        self.velocity = self.collide_velocity
        self.direction = self.collide_direction
        self.sprite_direction += self.turn_speed
        
        self.collision_box.center = (self.x, self.y)
        
        if self.is_collided:
            self.x += self.velocity * self.dir_cos
            self.y += self.velocity * self.dir_sin
            self.collide_velocity -= 0.006
            
            if self.collide_velocity < 0.001:
                self.collide_velocity = 0
                self.is_collided = False        
    
    def check_collision(self, entities):
        from entities.bullet import Bullet
        for entity in entities:
            if entity.has_collision and entity is not self and not isinstance(entity, Bullet):
                if self.collision_box.colliderect(entity.collision_box):
                    self.handle_collision(entity)    
                    entity.handle_collision(self)
     
    def handle_collision(self, entity):
        self.sound.play()
        
        dx = entity.x - self.x
        dy = entity.y - self.y

        self.collide_direction = math.degrees(math.atan2(dy, dx))
        dir_radians = math.radians(self.collide_direction+180)
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
        
        
        self.lives -= 1
        
        if abs(entity.velocity) < 0.001:
            self.collide_velocity = 0.2
        else:
            self.collide_velocity = abs(entity.velocity)*entity.weight
            
        
        self.is_collided = True
         
    def render(self, screen):
        
        rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.sprite_direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
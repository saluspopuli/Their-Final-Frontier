from entity import Entity
from player import Player
import math
import pygame

class Bullet(Entity):
    
    def __init__(self, x, y, width = 5, height = 5, direction = 0):
        
        image = 0
        
        collision_box_scale = 0.8
        collision_box = pygame.Rect(x,y,width*collision_box_scale, height*collision_box_scale)
        
        super().__init__(x, y, width, height, direction, image, collision_box, has_collision=True)
        
        self.weight = 0.1
        self.velocity = 8
        
        dir_radians = -math.radians(self.direction+90)
        
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
    
    def update(self):
        
        self.collision_box.center = (self.x, self.y)

        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin
        
        pass
    
    def check_collision(self, entities):     
        for entity in entities:
            if entity.has_collision and entity is not self and not isinstance(entity,Player):
                if self.collision_box.colliderect(entity.collision_box):
                    entities.remove(self)
                    entity.handle_collision(self)
                    
    
    
    def render(self, screen):
        pygame.draw.circle(screen, (255,0,0), (self.x,self.y), self.width/2)

    
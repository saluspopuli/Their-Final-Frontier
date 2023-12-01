import pygame
import os
import pygame

class Entity:
    
    
    
    def __init__(self, x, y, width, height, direction, image, collision_box = 0, has_collision = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.image = image
        self.scaled_image = []
        self.scaled_image.append(pygame.transform.scale(self.image, (self.width, self.height)))
        self.state = 0
        self.collision_box = collision_box
        self.has_collision = has_collision

    def update(self):
        
        pass
    
    def load_sprites(self, folder):  
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename))
                self.scaled_image.append(pygame.transform.scale(image, (self.width, self.height)))

    
    def check_collision(self, entities):     
        for entity in entities:
            if entity.has_collision and entity is not self:
                if self.collision_box.colliderect(entity.collision_box):
                    self.handle_collision(entity)
                    
    def handle_collision(self, entity):
        # Redefine this function in the objects otherwise it will do nothing
        pass
                        
    def render(self, screen):
        
        rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
        
        #DEBUG RENDERING
        #if self.has_collision:
            #pygame.draw.rect(screen,(0,255,0) ,self.collision_box)

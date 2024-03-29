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
        if image != 0:
            self.scaled_image = []
            self.scaled_image.append(pygame.transform.scale(self.image, (self.width, self.height)))
        self.state = 0
        self.collision_box = collision_box
        self.has_collision = has_collision
        self.weight = 1
        self.lives = 1
        
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(r"assets\sound\hit.wav")

    def update(self):
        
        pass
    
    def load_sprites(self, folder):
        self.scaled_image = []
        file_list = sorted(os.listdir(folder))
        for filename in file_list:
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                self.scaled_image.append(pygame.transform.scale(image, (self.width, self.height)))

    
    def check_collision(self, entities):
        
        if self.has_collision:   
            for entity in entities:
                if entity.has_collision and entity is not self:
                    if self.collision_box.colliderect(entity.collision_box):
                        self.handle_collision(entity)
                        
                        entity.handle_collision(self)
                    
    def handle_collision(self, entity):
        # Redefine this function in the objects otherwise it will do nothing
        pass
                        
    def render(self, screen):
        
        rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)

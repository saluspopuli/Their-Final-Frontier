import pygame

class Entity:
    def __init__(self, x, y, width, height, direction, image, collision_box = 0, has_collision = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.image = image
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        self.collision_box = collision_box
        self.has_collision = has_collision

    def update(self):
        
        pass

    def check_collision(self, entities):     
        for entity in entities:
            if entity.has_collision and entity is not self:
                if self.collision_box.colliderect(entity.collision_box):
                    self.handle_collision(entity)
                    
    def handle_collision(self, entity):
        # Redefine this function in the objects otherwise it will do nothing
        pass
                        
    def render(self, screen):
        rotated_image = pygame.transform.rotate(self.scaled_image, self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
        
        #DEBUG RENDERING
        #if self.has_collision:
            #pygame.draw.rect(screen,(0,255,0) ,self.collision_box)

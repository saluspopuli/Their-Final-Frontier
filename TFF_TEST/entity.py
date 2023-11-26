import pygame

class Entity:
    def __init__(self, x, y, width, height, velocity, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = direction

    def update(self):
        
        pass

    def render(self, screen):
        
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        rotated_image = pygame.transform.rotate(scaled_image, self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
        pass

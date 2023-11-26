import pygame

class Entity:
    def __init__(self, x, y, width, height, direction, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.image = image
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        
        pass

    def render(self, screen):
        rotated_image = pygame.transform.rotate(self.scaled_image, self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)

import pygame
import pygame_gui

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        # Draw button with transparent color
        pygame.draw.rect(surface, transparent, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
         
#VARIABLES
transparent = (0, 0, 0, 0)
black = (0, 0, 0)
import pygame
import math
from player import Player
from ship import Ship
from lagrange import Lagrange

# Pygame stuff ========================================================================
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Their Final Frontier")
window_icon = pygame.image.load("assets\window_icon.png")  # Update the file path here
pygame.display.set_icon(window_icon)

# Object initialization ================================================================
lagrange = Lagrange()

entities = [Player (280, 300),
            Ship(300,400,width=150,height=150, lagrange=lagrange)]

# FUNCTIONS ===========================================================================
def update():
    for entity in entities:
        entity.update()
    
def render(screen):
    for entity in entities:
        entity.render(screen)

# MAIN ================================================================================
if __name__ == "__main__":
    # Main game loop
    running = True
    while running:
        
        clock.tick(FPS)
        screen.fill((0,0,0)) #just draws black
        
        # Ensures that all events in the game are run
        for event in pygame.event.get():
            
            # Quits game if pygame detects the quit event type
            if event.type == pygame.QUIT:
                running = False
        
        update()
        render(screen)
                
        pygame.display.update()



    
    



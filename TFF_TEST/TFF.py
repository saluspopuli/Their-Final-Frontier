import pygame
import math
from player import Player

# Other variables
clock = pygame.time.Clock()
FPS = 60

# Player initialization
player = Player(280, 300)

#initializes pygame somehow
pygame.init()

# Creates the display
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Their Final Frontier")
window_icon = pygame.image.load("assets\window_icon.png")  # Update the file path here
pygame.display.set_icon(window_icon)

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
    
    player.update()
    player.render(screen)
            
    pygame.display.update()


    
    



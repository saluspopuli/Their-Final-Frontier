import pygame

#initializes pygame somehow
pygame.init()

screen = pygame.display.set_mode((800,600))



# Main game loop
running = True
while running:
    
    # Ensures that all events in the game are run
    for event in pygame.event.get():
        
        # Quits game if pygame detects the quit event type
        if event.type == pygame.QUIT:
            running = False
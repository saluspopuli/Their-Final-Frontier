import pygame
from game import Game

# Pygame stuff ========================================================================
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screenX = 1500
screenY = 600
screen = pygame.display.set_mode((screenX,screenY))

# Title and Icon
pygame.display.set_caption("Their Final Frontier Alpha")
window_icon = pygame.image.load("assets\window_icon.png")  # Update the file path here
pygame.display.set_icon(window_icon)

# Object Initializations
main_game = Game(screen, screenX, screenY, clock, FPS)

# Variables
running = True

# MAIN ================================================================================
if __name__ == "__main__":
       
    main_game.mainloop()
    
    



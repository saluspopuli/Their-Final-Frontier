import pygame
import pygame_gui
from game import Game
from menu import Menu

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

# Variables
running = {'value': True}

# Object Initializations
gui_manager = pygame_gui.UIManager((screenX,screenY))

main_menu = Menu(gui_manager, (screenX, screenY), screen, running, clock)
main_game = Game(screen, screenX, screenY, clock, running, FPS)

# MAIN ================================================================================
if __name__ == "__main__":
       
    #main_menu.mainloop()
    main_game.mainloop()
    
    



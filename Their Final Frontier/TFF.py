import pygame
import pygame_gui
import os
from game import Game
from menu import Menu
from button import Button

# Pygame stuff ========================================================================
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screenX = 1280
screenY = 720
screen = pygame.display.set_mode((screenX,screenY))

# Title and Icon
pygame.display.set_caption("Their Final Frontier Alpha")
window_icon = pygame.image.load("assets\window_icon.png")  # Update the file path here
pygame.display.set_icon(window_icon)

# Variables
running = {'value': True}

# Object Initializations
gui_manager = pygame_gui.UIManager((screenX,screenY))

running = {'value': True}


main_menu = Menu(gui_manager, (screenX, screenY), screen, running, clock)


# MAIN ================================================================================
if __name__ == "__main__":
       
    #main_menu.mainloop()
    difficulty = 2
    score = 0
    tmp_score = 0
    
    pygame.mixer.init()
    sound = pygame.mixer.Sound(r"assets\sound\bg_loop\bg_loop.wav")
    loop_channel = pygame.mixer.Channel(3)
    loop_channel.set_volume(1.5)
    loop_channel.play(sound,-1)
    
    checking = main_menu.mainloop()
    
    while running['value']:
        
        game = Game(screen, screenX, screenY, clock, running, FPS, difficulty, score, not checking)
        
        game_state, tmp_score = game.mainloop()
        
        if running['value']:      
            game.fadeout()
        
        score += tmp_score
        if game.game_flag:
            difficulty += 1
        else:
            main_menu = Menu(gui_manager, (screenX, screenY), screen, running, clock)
            checking = main_menu.mainloop()
            
    
    



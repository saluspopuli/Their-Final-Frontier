import pygame
import pygame_gui
from game import Game
from menu import Menu

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
    while running:
        game = Game(screen, screenX, screenY, clock, running, FPS, difficulty, score)
        loop_channel.set_volume(1.5)
        loop_channel.play(sound,-1)
        
        try:
            game_state, tmp_score = game.mainloop()
        except:
            break
        
        game.fadeout()
        
        score += tmp_score
        if game.game_flag:
            difficulty += 1
        else:
            break
            
    
    



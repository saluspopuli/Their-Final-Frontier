import pygame
import pygame_gui

class Menu:
    
    def __init__(self, gui_manager, screen_size, screen, running, clock):
        self.gui_manager = gui_manager
        self.screen_size = screen_size
        self.screen = screen
        self.running = running
        self.clock = clock
        self.state = 0 #This variable determines which menu will be displayed
        self.menu_flag = True
    
        
    def mainloop(self):
        
        while self.running['value'] and self.menu_flag:
            
            self.time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running['value'] = False
                    
                self.gui_manager.process_events(event)
            
            #THIS MENU WILL CONSTANTLY RUN AGAIN AND AGAIN SO NEVER EVER USE 
            #FOR LOOPS THAT ARE INDEFINITE
            
            match self.state:
                case 1:
                    self.main_menu()
                case 2:
                    self.intro()
                case 3:
                    self.play_game()
                case 4:
                    self.checking_mode()
                case _:
                    pass
            

            self.gui_manager.update(self.time_delta)
            self.screen.fill((0,0,255))
            self.gui_manager.draw_ui(self.screen) 
            pygame.display.update()
                    
            
    def main_menu(self):
        #PUT MAIN_MENU CODE HERE
        pass
    
    def intro(self):
        #PUT INTRO CODE HERE
        pass
    
    def play_game(self):
        #PUT PLAY_GAME CODE HERE
        pass
    
    def checking_mode(self):
        #PUT CHECKING_MODE CODE HERE
        pass

# CODE FOR TESTING, JUST RUN THE FILE TO SEE IF YOUR CHANGES WORK ======================

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screenX = 1280
screenY = 720
screen = pygame.display.set_mode((screenX,screenY))

# Title and Icon
pygame.display.set_caption("Their Final Frontier Alpha")

# Variables
running = {'value': True}

# Object Initializations
gui_manager = pygame_gui.UIManager((screenX,screenY))

main_menu = Menu(gui_manager, (screenX, screenY), screen, running, clock)

main_menu.mainloop()
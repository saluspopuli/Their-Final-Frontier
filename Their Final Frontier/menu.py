import pygame
import pygame_gui

class Menu:
    
    menu_flag = True
    menu_to_display = 0
    
    def __init__(self, gui_manager, screen_size, screen, running, clock):
        self.gui_manager = gui_manager
        self.screen_size = screen_size
        self.screen = screen
        self.running = running
        self.clock = clock
    
        
    def mainloop(self):
        
        while self.running['value'] and self.menu_flag:
            
            self.time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running['value'] = False
                    
                self.gui_manager.process_events(event)
            
            
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
        pass
    
    def intro(self):
        pass
    
    def play_game(self):
        pass
    
    def checking_mode(self):
        pass
        
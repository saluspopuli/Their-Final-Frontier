import pygame
import pygame_gui

class Menu:
    
    def __init__(self, gui_manager, screen_size, screen, running, clock):
        self.gui_manager = gui_manager
        self.screen_size = screen_size
        self.screen = screen
        self.running = running
        self.clock = clock
        
        self.initialize_elements()
    
    # UI element initializations
    def initialize_elements(self):
        self.title_label = pygame_gui.elements.UILabel(
                  relative_rect=pygame.Rect((self.screen_size[0] // 2 - 150, self.screen_size[1] // 2 - 250), (300, 500)),
                  text="Main Title",
                  manager=self.gui_manager
                  )
        
    def mainloop(self):
        
        while self.running['value']:
            
            self.time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running['value'] = False
                    
                self.gui_manager.process_events(event)
            
            self.gui_manager.update(self.time_delta)
            
            self.screen.fill((0,0,255))
            
            self.gui_manager.draw_ui(self.screen)
            
            pygame.display.update()
                    
            
        
        
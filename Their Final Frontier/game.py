import pygame
from player import Player
from ship import Ship
from lagrange import Lagrange
from waypoint import Waypoint

class Game():
    
    running = True
    init_player_pos = (300,400)
    init_player_dir = 270
    
    init_ship_pos = (-100, 400)
    init_ship_dir = 270
    
    def __init__(self, screen, screenX, screenY, clock, FPS = 60):
        self.screenX = screenX
        self.screenY = screenY
        
        self.ship = Ship(self.init_ship_pos[0],
                         self.init_ship_pos[1],
                         width=150,
                         height=150,
                         lagrange=Lagrange([(0,screenY/2)]),
                         direction = 270)
        
        self.player = Player(self.init_player_pos[0], self.init_player_pos[1], direction=self.init_player_dir)
        self.entities = [self.player,self.ship]
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.font = pygame.font.Font(None, 36)

    # FUNCTIONS ===========================================================================
    def update(self):
        for entity in self.entities:
            entity.update()
    
    def render(self,screen):
        for entity in reversed(self.entities):
            entity.render(screen)
    
    def mainloop(self):   
        
        while self.running:     
            self.clock.tick(self.FPS)
            # print("Current FPS: ", clock.get_fps())
            self.screen.fill((0,0,0)) #just draws black
            
            # Ensures that all events in the game are run
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.entities.append(Waypoint(self.player.x,self.player.y))
                    self.ship.lagrange.add_point(self.player.x,self.player.y)
                    self.ship.draw_waypoint_line(self.screenX)
                
                # EVENTS FOR DEBUGGING ===============================================================  
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #TODO: placeholder
                    self.ship.moving_flag = True
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT: #TODO: placeholder
                    self.ship.change_lagrange_points(False, self.screenX)
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: #TODO: placeholder
                    self.ship.change_lagrange_points(True, self.screenX)
            
            text = self.font.render("Lagrange points: " + str(self.ship.lagrange_points), True, (255, 255, 255))
            self.screen.blit(text, (20,20))       
            self.update()
            self.render(self.screen)
                    
            pygame.display.update()


    

    
    



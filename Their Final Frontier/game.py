import pygame
import random
from player import Player
from ship import Ship
from lagrange import Lagrange
from waypoint import Waypoint
from debris import Debris
import os

class Game():
    
    init_player_pos = (40,0)
    init_player_dir = 270
    
    init_ship_pos = (-100, 400)
    init_ship_dir = 270
    
    debris_list = []
    
    def __init__(self, screen, screenX, screenY, clock, running, FPS=60):
        self.screenX = screenX
        self.screenY = screenY
        self.running = running
        
        self.ship = Ship(self.init_ship_pos[0],
                         screenY/2,
                         width=150,
                         height=150,
                         lagrange=Lagrange([(0,screenY/2)]),
                         direction = 270)
        
        self.ship.init_tmp_waypoint_line(screenX)
        
        self.player = Player(self.init_player_pos[0], screenY/2, direction=self.init_player_dir)
        self.entities = [self.player,self.ship]
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.font = pygame.font.Font(None, 36)
        
        self.init_debris(10, "aasda") #TODO: move this 

    # FUNCTIONS ===========================================================================
    def update(self):
        for entity in reversed(self.entities):
            if entity.has_collision:
                entity.check_collision(self.entities)
        
        for entity in self.entities:
            entity.update()
    
    def render(self,screen):
        for entity in reversed(self.entities):
            entity.render(screen)
    

    def init_debris(self, number, randomseed):
        tmp_flag = True
        i = 1

        random.seed(randomseed)

        while tmp_flag:
            filename = os.path.join("assets", "debris", f"debris{i}.png")
            if os.path.exists(filename):
                self.debris_list.append(filename)
            else:
                tmp_flag = False
            i += 1

        for i in range(number):
            scale = random.randrange(50, 100)
            self.entities.insert(
                0,
                Debris(
                    random.randrange(150, self.screenX),
                    random.randrange(150, self.screenY),
                    scale,
                    scale,
                    random.randrange(0, 360),
                    random.choice(self.debris_list),
                    True,
                    random.randrange(1,100),
                    random.choice([True,False]) 
                )
            )
            
    def mainloop(self):   
        
        while self.running['value']:     
            self.clock.tick(self.FPS)
            print("Current FPS: ", self.clock.get_fps())
            self.screen.fill((0,0,0)) #just draws black
            
            # Ensures that all events in the game are run
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running['value'] = False
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if (self.player.x, self.player.y) not in self.ship.lagrange.coordinates:
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
            
            # TODO: get rid of these puhon
            text = self.font.render("Lagrange points: " + str(self.ship.lagrange_points), True, (255, 255, 255))
            
            self.screen.blit(text, (20,20))       
            self.update()
            self.render(self.screen)
                    
            pygame.display.update()


    

    
    



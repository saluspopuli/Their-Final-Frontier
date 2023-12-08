import pygame
import random
from player import Player
from ship import Ship
from lagrange import Lagrange
from waypoint import Waypoint
from debris import Debris
from bullet import Bullet
import os

class Game():
    
    init_player_pos = (40,0)
    init_player_dir = 270
    
    init_ship_pos = (-200, 400)
    init_ship_dir = 270
    
    game_flag = True
    
    ship_max_initial_movement = 60*8
    ship_initial_movement = 0
    
    def __init__(self, screen, screenX, screenY, clock, running, FPS=60, difficulty = 1):
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
        waypoints = 3  
        waypoints = int(waypoints + difficulty/5)  
        bullets = 6
        bullets = int (bullets + bullets/3)
        self.player = Player(self.init_player_pos[0], screenY/2, direction=self.init_player_dir,waypoints= waypoints, bullets = bullets)
        
        self.entities = [self.player,self.ship]
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.font = pygame.font.Font(None, 36)
        
        self.debris_list = []
        self.init_debris(difficulty*3, random.randrange(1,1293219)) #TODO: move this
        
        screen.fill((0,0,0)) 

    # FUNCTIONS ===========================================================================
    def update(self):
        for entity in reversed(self.entities):
            if entity.has_collision:
                entity.check_collision(self.entities)
        
        for entity in self.entities:
            if isinstance(entity, Bullet):
                if entity.x > self.screenX or entity.x < 0 or entity.y > self.screenY or entity.y < 0:
                    self.entities.remove(entity)
                else:
                    entity.update()
            else:
                entity.update()
    
    def render(self, screen):
        for entity in reversed(self.entities):
            entity.render(screen)
    
    def game_over(self):
        text = self.font.render("GAME OVER", True, (255, 255, 255))
            
        self.screen.blit(text, ((((self.screenX - text.get_width())/2)), (self.screenY - text.get_height())/2))
        pygame.display.update()
        
        for i in range(300):
            self.clock.tick(self.FPS)
            
        self.game_flag = False
             
        
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
                    random.randrange(0, self.screenY),
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
        
        while self.running['value'] and self.game_flag:     
            self.clock.tick(self.FPS)
            print("Current FPS: ", self.clock.get_fps())
            self.screen.fill((0,0,0)) #just draws black
            
            # Ensures that all events in the game are run
            for event in pygame.event.get():
                
                # Quits game if pygame detects the quit event type
                if event.type == pygame.QUIT:
                    self.running['value'] = False
                
                # Place waypoint if E is pressed and if player still has waypoints left
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.player.waypoints > 0 and self.player.can_move:
                    # Ensures new coord is not in the same place as another coord so that it doesn't
                    # throw an error
                    if not any(coord[0] == self.player.x for coord in self.ship.lagrange.coordinates):
                        self.entities.append(Waypoint(self.player.x,self.player.y))
                        self.ship.lagrange.add_point(self.player.x,self.player.y)
                        self.ship.draw_waypoint_line(self.screenX)
                        self.player.waypoints-=1
                        
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player.can_move and self.player.bullets > 0:
                    self.entities.append(Bullet(self.player.x, self.player.y, 8,8, self.player.direction))
                    self.player.bullets -= 1
                
                # Toggles fullscreen/windowed when F11 is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        # Switch to windowed mode
                        self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                    else:
                        #Switch to Fullscreen
                        self.screen = pygame.display.set_mode((self.screenX, self.screenY), pygame.FULLSCREEN)
                    
                # EVENTS FOR DEBUGGING ===============================================================  
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #TODO: placeholder
                    self.ship.moving_flag = True
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT: #TODO: placeholder
                    self.ship.change_lagrange_points(False, self.screenX)
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: #TODO: placeholder
                    self.ship.change_lagrange_points(True, self.screenX)
            
            # OTHER GAME CHECKS ===============================================
            
            # If player runs out of lives or if ship runs out of lives then end game
            if self.player.lives <= 0 or self.ship.lives <= 0:
                self.game_flag = False
            
            # If ship goes beyond upper and lower boundaries of screen then end game
            if self.ship.y > self.screenY + 200 or self.ship.y < 0 - 200:
                self.game_flag = False

            # If ship goes beyond right side of screen then you have won
            if self.ship.x > self.screenX + 100:
                return True
            
            # =================================================================
            
            # Important Game Logic ============================================
            
            if self.ship_initial_movement < self.ship_max_initial_movement and not self.ship.moving_flag:
                self.ship_initial_movement += 1
            elif not self.ship.moving_flag:
                self.ship.moving_flag = True
            # =================================================================
              
            self.update()
            self.render(self.screen)
            
            # UI ELEMENT RENDERING ============================================
            
            # TODO: PUT THESE INTO CHECKING MODE
            text = self.font.render("Lagrange points: " + str(self.ship.lagrange_points), True, (255, 255, 255))
            self.screen.blit(text, (20,80)) 
            
            t_waypoint_num = self.font.render("Waypoints Left: " + str(self.player.waypoints), True, (255, 255, 255))
            self.screen.blit(t_waypoint_num, (20,20))
            t_bullets_num = self.font.render("Bullets Left: " + str(self.player.bullets), True, (255, 255, 255))
            self.screen.blit(t_bullets_num, (20,50))
            
            if not self.ship.moving_flag:
                ship_movement_time = int((self.ship_max_initial_movement - self.ship_initial_movement)/self.FPS)
                t_ship_move_time = self.font.render("Ship moves in : " + str(ship_movement_time) + "s", True, (255, 255, 255))
                self.screen.blit(t_ship_move_time, (20,self.screenY - 50))
            
            # ====================================================================

            pygame.display.update()
            
            if not self.game_flag:
                self.game_over()


    

    
    



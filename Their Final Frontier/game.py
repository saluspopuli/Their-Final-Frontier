import pygame
import random
from lagrange import Lagrange
from entities.player import Player
from entities.ship import Ship
from entities.waypoint import Waypoint
from entities.debris import Debris
from entities.bullet import Bullet
from entities.particles import Particles
from gui import *
import os

class Game():
    
    init_player_pos = (-50,0)
    init_player_dir = 270
    
    init_ship_pos = (-200, 400)
    init_ship_dir = 270
    
    game_flag = True
    
    ship_max_initial_movement = 60*8
    ship_initial_movement = 0
    
    def __init__(self, screen, screenX, screenY, clock, running, FPS=60, difficulty = 1, score = 0):
        self.score = score
        self.entities = []
        self.HUD = []
        
        self.screenX = screenX
        self.screenY = screenY
        self.running = running
        
        pygame.mixer.init()
        self.sounds = []
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\explosion.wav"))   # 0
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\game_over.wav"))   # 1
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\hit.wav"))         # 2
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\laser.wav"))       # 3
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\place.wav"))       # 4
        self.sounds.append(pygame.mixer.Sound(r"assets\sound\rumbling.wav"))    # 5
        
        self.sounds[3].set_volume(0.8)
        self.sounds[4].set_volume(0.6)
        self.rumble_channel = pygame.mixer.Channel(2)
        self.rumble_volume = 0.35
        
        self.ship = Ship(self.init_ship_pos[0],
                         screenY/2,
                         width=150,
                         height=150,
                         lagrange=Lagrange([(0,screenY/2)]),
                         direction = 270)
        
        self.ship.init_tmp_waypoint_line(screenX)
        waypoints = 3  
        waypoints = int(waypoints + difficulty/3)  
        bullets = 6
        bullets = int(bullets + difficulty/2)
        
        self.max_waypoints = waypoints
        self.max_bullets = bullets
        
        self.player = Player(self.init_player_pos[0], screenY/2, direction=self.init_player_dir,waypoints= waypoints, bullets = bullets)
        
        self.entities.append(self.player)
        self.entities.append(self.ship)
        
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.font = pygame.font.Font(r"assets\font\nine0.ttf", 36)
        self.font_small = pygame.font.Font(r"assets\font\nine0.ttf", 20)
        
        self.debris_list = []
        self.init_debris(difficulty*3, random.randrange(1,1293219)) #TODO: move this
        
        self.surface = pygame.Surface((self.screenX, 200), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 100))
        #Random background choosing
        darkness = 100
        self.background = pygame.image.load(r"assets\\backgrounds\\" + str(random.randint(1,3)) + ".png")
        self.dark_surface = pygame.Surface(self.background.get_size())
        self.dark_surface.fill((darkness, darkness, darkness))
        self.background.blit(self.dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        

    # FUNCTIONS ===========================================================================
    def update(self):
        
        for entity in reversed(self.entities):
            if entity.has_collision:
                entity.check_collision(self.entities)
        
        for entity in self.entities:
            if isinstance(entity, Bullet) and (entity.x > self.screenX or entity.x < 0 or entity.y > self.screenY or entity.y < 0):
                self.entities.remove(entity)
            else:
                if entity.lives <= 0:        
                    if not isinstance(entity, Particles):
                        entity.update()
                        self.createParticles(entity)
                    
                    if not isinstance(entity, Ship) or not isinstance(entity, Player):
                        self.entities.remove(entity)
                        
                        if not isinstance(entity, Particles):
                            self.sounds[0].play()
                else:
                    entity.update()
                    
    def render(self, screen):
        #self.screen.blit(self.background, (0,0))
        
        for entity in reversed(self.entities):
            entity.render(screen)
            
        self.misc_ui_elements()

            
    def createParticles(self, entity):
        for i in range(0,random.randint(10,30)):
            scale = random.uniform(5,10)
            direction = entity.direction + random.uniform(-30,30)
            velocity = entity.velocity + random.uniform(1,3)
            tmp_color = random.randint(69,255)
            color = (tmp_color, int(tmp_color/1.4), int(tmp_color/3.6))
            self.entities.append(Particles(entity.x,entity.y,scale,scale,direction, velocity,color))
    
    def game_over(self):
        self.sounds[1].play()
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

    def fadeout(self):
        running = True
        darkness_frame = 80
        darkness = 0
        volume = self.rumble_volume
        dark_surface = pygame.Surface(self.background.get_size(), pygame.SRCALPHA)  # Set the surface with alpha channel
        
        while running:
            
            volume -= 0.005
            if volume >= 0:
                volume = 0
            self.rumble_channel.set_volume(volume)
            darkness_frame -= 1
            darkness += 5
            if darkness > 255:
                darkness = 255
            if darkness_frame <= 0:
                running = False
            self.clock.tick(self.FPS)
            dark_surface.fill((0, 0, 0, darkness))  # Set the fill color with alpha value
            self.render(self.screen)
            self.screen.blit(dark_surface,(0,0))
            pygame.display.update()
        
    def mainloop(self):   
        
        #test_var = 0 #TODO: ONLY USE FOR TESTING
        #self.player.bullets = 10000
        #self.player.waypoints = 10000
        
        while self.running['value'] and self.game_flag:     
            self.clock.tick(self.FPS)
            print("Current FPS: ", self.clock.get_fps())
            self.screen.blit(self.background, (0,0))
            
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
                        self.sounds[4].play()
                        
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player.can_move and self.player.bullets > 0:
                    self.entities.append(Bullet(self.player.x, self.player.y, 8,8, self.player.direction))
                    self.player.bullets -= 1
                    self.sounds[3].play()
                
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
                score = 0
                score += 50 * (self.max_bullets - (self.max_bullets - self.player.bullets))
                score += 50 * (self.max_waypoints - (self.max_waypoints - self.player.waypoints))
                tmp_screenY = self.screenY / 2
                score += 200 + int((tmp_screenY - abs(self.ship.y-tmp_screenY))*0.555556)
                return True, score
            
            # =================================================================
            
            # Important Game Logic ============================================
            
            if self.ship_initial_movement < self.ship_max_initial_movement and not self.ship.moving_flag:
                self.ship_initial_movement += 1
            elif not self.ship.moving_flag:
                self.ship.moving_flag = True
            
            self.rumble_channel.set_volume(self.rumble_volume)
            
            if ((self.ship.can_move and self.ship.moving_flag) or self.player.is_moving) and not self.rumble_channel.get_busy():
                self.rumble_channel.play(self.sounds[5])
            
            if not ( self.ship.can_move and self.ship.moving_flag) and not self.player.is_moving:
                self.rumble_channel.stop()
            
            # =================================================================
              
            self.update()
            self.render(self.screen)

            pygame.display.update()
            
            if not self.game_flag:
                self.game_over()
                
    def misc_ui_elements(self):
        # UI ELEMENT RENDERING ============================================
                
        # TODO: PUT THESE INTO CHECKING MODE
        text = self.font.render("Lagrange points: " + str(self.ship.lagrange_points), True, (255, 255, 255))
        self.screen.blit(text, (20,10)) 
        
        # t_waypoint_num = self.font.render("Waypoints Left: " + str(self.player.waypoints), True, (255, 255, 255))
        # self.screen.blit(t_waypoint_num, (20,20))
        # t_bullets_num = self.font.render("Bullets Left: " + str(self.player.bullets), True, (255, 255, 255))
        # self.screen.blit(t_bullets_num, (20,50))
        
        if not self.ship.moving_flag:
            ship_movement_time = int((self.ship_max_initial_movement - self.ship_initial_movement)/self.FPS)
            t_ship_move_time = self.font.render("Ship moves in : " + str(ship_movement_time) + "s", True, (255, 255, 255))
            self.screen.blit(t_ship_move_time, (20,self.screenY - 110))
            
        self.HUD = []
        
        #Bullet HUD
        tmp_bull = self.player.bullets
        if self.player.bullets > 13:
            tmp_bull = 13
            
        for i in range(tmp_bull):       
            self.HUD.append(Bullet_UI(10 + i*40, self.screenY-55,50))
            
        #Waypoint HUD
        tmp_waypoint = self.player.waypoints
        if self.player.waypoints > 8:
            tmp_waypoint = 8
            
        for i in range(tmp_waypoint):
            self.HUD.append(Waypoint_UI((self.screenX-60) - i*70, self.screenY-55, 50))
        
        self.screen.blit(self.surface, (0, self.screenY-60))  
        
        for element in self.HUD:
            element.render(self.screen)  
            
        # Score displaying
        
        t_score = self.font.render(str(self.score), True, (255, 255, 255))
        
        text_width = t_score.get_width()
        text_x = (self.screenX - text_width) // 2
        
        self.screen.blit(t_score, (text_x, self.screenY-40))
        
        t_score = self.font_small.render("Score:", True, (255, 255, 255))
        
        text_width = t_score.get_width()
        text_x = (self.screenX - text_width) // 2
        
        self.screen.blit(t_score, (text_x, self.screenY-60))
        
        # ====================================================================
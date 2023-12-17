import pygame
import pygame_gui
import os
import random
import math

# Pygame stuff ========================================================================
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screenX = 1280
screenY = 720
screen = pygame.display.set_mode((screenX,screenY))

# Title and Icon
pygame.display.set_caption("Their Final Frontier 1.0")
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
    loop_channel = pygame.mixer.Channel(4)
    loop_channel.set_volume(1.5)
    loop_channel.play(sound,-1)
    
    try:
        checking = main_menu.mainloop()
    except:
        checking = False
    
    try:
        while running['value']:
            game = None
            game = Game(screen, screenX, screenY, clock, running, FPS, difficulty, score, not checking)
            
            try:
                game_state, tmp_score = game.mainloop()
                
                if running['value']:      
                    game.fadeout()
            except:
                game_state = True
                tmp_score = 0  
            
                
            score += tmp_score
            if game.game_flag:
                difficulty += 1
            else:
                main_menu = Menu(gui_manager, (screenX, screenY), screen, running, clock)
                try:
                    checking = main_menu.mainloop()
                except:
                    cheking = False
    except:
        pass
            
# Variables
#These are PATHS variables containing the absolute path of the objects. 
title_path = os.path.join(r"assets\menu\title.png")
bg_path = os.path.join(r"assets\menu\bg.jpg")
start_btn_path = os.path.join(r"assets\menu\start_button.png")
check_btn_path = os.path.join(r"assets\menu\check_button.png")

running = {'value': True}

# Object Initializations
       
#Instantiates a button with parameters for X, Y, Width, Height, Text respectively.
start_btn_invis = Button(460, 430, 325, 65, "Start")
check_btn_invis = Button(460, 490, 427, 52, "Check")
screen_btn_invis = Button(0, 0, 1280, 720, "Screen")

class Menu:
    
    def __init__(self, gui_manager, screen_size, screen, running, clock):
        self.gui_manager = gui_manager
        self.screen_size = screen_size
        self.screen = screen
        self.running = running
        self.clock = clock
        self.state = 1 #This variable determines which menu will be displayed
        self.previous_state = self.state
        
        self.menu_flag = True
        self.previous = 0
          
        self.sound = pygame.mixer.Sound(r"assets\sound\place.wav")
        
        image = pygame.image.load(r"assets\player\player1.png")
        image = pygame.transform.rotate(image, -90)
        self.image = pygame.transform.scale(image, (50, 50))
        
        self.c1 = True
        self.c2 = True

        
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

            if self.previous_state != self.state:
                self.sound.play()
                self.previous_state = self.state
            
            match self.state:
                case 1:
                    self.main_menu()
                case 2:
                    self.intro()
                case 3:
                    self.play_game()
                case 4:
                    self.checking_mode()
                case 5:
                    return True
                case 6:
                    return False
                case _:
                    pass
            
            self.gui_manager.update(self.time_delta)
            self.gui_manager.draw_ui(self.screen) 
            pygame.display.update()           
            
    def main_menu(self):
        
        #These loads the images to pygame. 
        bg_overlay = pygame.image.load(bg_path)   
        title_overlay = pygame.image.load(title_path)
        start_btn_overlay = pygame.image.load(start_btn_path)
        check_btn_overlay = pygame.image.load(check_btn_path)
                
        self.screen.blit(bg_overlay, (0, 0))
        self.screen.blit(title_overlay, (0, 0))
        self.screen.blit(check_btn_overlay, (460, 490))
        self.screen.blit(start_btn_overlay, (460, 430))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_btn_invis.rect.collidepoint(event.pos):
                        #START BUTTON CLICK
                        self.previous = 3
                        self.state = 2
                        
                    elif check_btn_invis.rect.collidepoint(event.pos):
                        #CHECK BUTTON CLICK
                        self.previous = 4
                        self.state = 2
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        if start_btn_invis.rect.collidepoint(mouse_pos):
            if self.c1:
                self.sound.play()
                self.c1 = False
            self.screen.blit(self.image,(415,435))
        else:
            self.c1 = True
        
        if check_btn_invis.rect.collidepoint(mouse_pos):
            if self.c2:
                self.sound.play()
                self.c2 = False
            self.screen.blit(self.image,(415,490))
        else:
            self.c2 = True
        
                
            
    def intro(self):

        #These loads the images to pygame. 
        intro_overlay = pygame.image.load(r"assets\menu\Intro.jpg")
        self.screen.blit(intro_overlay, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            #If user presses a key, specifically space = next screen, esc = escape
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = self.previous

                elif event.key == pygame.K_ESCAPE:
                    self.state = 1
                    
            #If user clicks the left button, goes to the next screen.        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                        if screen_btn_invis.rect.collidepoint(event.pos):
                            #START BUTTON CLICK
                            self.state = self.previous
    
    def play_game(self):

        #These loads the images to pygame. 
        pm_overlay = pygame.image.load(r"assets\menu\pm_controls.jpg")
        self.screen.blit(pm_overlay, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            #If user presses a key, specifically space = start, esc = escape
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 6       
                elif event.key == pygame.K_ESCAPE:
                    self.state = 1
                    
            #If user clicks the left button, the game will start.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if screen_btn_invis.rect.collidepoint(event.pos):
                        self.state = 5
    
    def checking_mode(self):
        
        #These loads the images to pygame. 
        cm_overlay = pygame.image.load(r"assets\menu\cm_controls.jpg")
        self.screen.blit(cm_overlay, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 6
                elif event.key == pygame.K_ESCAPE:
                    self.state = 1
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if screen_btn_invis.rect.collidepoint(event.pos):
                        #START BUTTON CLICK
                        self.state = 6  
    
class Lagrange:
    
    def __init__(self, coordinates = [(0,0)]):
        self.coordinates = coordinates
        # Sorts the coordinates with respect to the x value
        self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
        # Updates the list of indices for the coordinates list
        self.indices = list(range(len(self.coordinates)))

    #Use another arg name for X as x is used for other things. 
    def lagrange(self, target_x, n): 
        
        lagrange_val = 0
        
        # Ensures that n will never go beyond the amount of coordinates currently loaded
        if n > len(self.coordinates):
            n = len(self.coordinates)
        
        # Gets the index of the data point that is right after the target_x
        root_index = len(self.coordinates)-1
        for i, coord in enumerate(self.coordinates):
            if coord[0] > target_x: 
                root_index = i
                break
        
        # Sorts the indices by which is closest to the root_index
        sorted_indices = sorted(self.indices, key=lambda idx: abs(idx - root_index))
        
        # TODO: @Jamille, documment this part of your code ok thx
        for i in range(n):
            # Getting Li
            li_var = 1 
            for j in range(n):  
                if j != i:   
                    li_var *= (target_x - self.coordinates[sorted_indices[j]][0]) / (self.coordinates[sorted_indices[i]][0] - self.coordinates[sorted_indices[j]][0])
            
            # Getting Lagrange. f(x) = Li(x)f(Xi) where f(X) = target_y.
            target_y = li_var * self.coordinates[sorted_indices[i]][1]
            lagrange_val += target_y
            
        return lagrange_val
    

    # Adds a data point 
    def add_point(self, x, y):
        # Check if the new (x, y) values already exist in the coordinates list
        if (x, y) not in self.coordinates:  
            # Adds new x and y values to the coordinates list
            self.coordinates.append((x, y))
            # Sorts the coordinates with respect to the x value
            self.coordinates = sorted(self.coordinates, key=lambda coord: coord[0])
            # Updates the list of indices for the coordinates list
            self.indices = list(range(len(self.coordinates)))

import pygame

class UI:
    def __init__(self, x, y, image, scale):
        self.width = scale
        self.height = scale
        self.x = x
        self.y = y
        self.image = image
        
        self.scaled_image = pygame.transform.scale(self.image,(self.width, self.height))
    
    def render(self, screen):
        screen.blit(self.scaled_image, (self.x, self.y))
        
    
class Bullet_UI(UI):
    def __init__(self, x, y, scale):
        
        image = pygame.image.load(r"assets\UI\bullet.png")
        
        super().__init__(x, y, image, scale)
    
class Waypoint_UI(UI):
    def __init__(self, x, y, scale):
        
        image = pygame.image.load(r"assets\UI\waypoint.png")
        
        super().__init__(x, y, image, scale)
        
class Game():
    
    init_player_pos = (-50,0)
    init_player_dir = 270
    
    init_ship_pos = (-200, 400)
    init_ship_dir = 270
    
    game_flag = True
    
    ship_max_initial_movement = 60*8
    ship_initial_movement = 0
    
    def __init__(self, screen, screenX, screenY, clock, running, FPS=60, difficulty = 1, score = 0, checking = False):
        self.score = score
        self.tmp_score = 0
        self.entities = []
        self.HUD = []
        self.waypoint_list = []
        
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
        
        self.sounds[3].set_volume(0.5)
        self.sounds[4].set_volume(0.6)
        self.rumble_channel = pygame.mixer.Channel(2)
        self.rumble_volume = 0.35
        self.rumble2_channel = pygame.mixer.Channel(3)
        self.rumble2_volume = 0.35
        self.rumble2_channel.set_volume(self.rumble2_volume)
        
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
        
        self.player = Player(self.init_player_pos[0], screenY/2, direction=self.init_player_dir,waypoints= waypoints, bullets = bullets)
        
        self.entities.append(self.player)
        self.entities.append(self.ship)
        
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.font = pygame.font.Font(r"assets\font\nine0.ttf", 36)
        self.font_small = pygame.font.Font(r"assets\font\nine0.ttf", 20)
        self.font_small_bold = pygame.font.Font(r"assets\font\nine0.ttf", 25)
        self.font_small_bold.bold = True
        
        self.debris_list = []
        self.init_debris(difficulty*3, random.randrange(1,1293219)) #TODO: move this
        
        self.surface = pygame.Surface((self.screenX, 200), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 100))
        #Random background choosing
        darkness = 100
        self.background = pygame.image.load(r"assets\\backgrounds\\" + str(random.randint(1,3)) + ".png").convert_alpha()
        self.dark_surface = pygame.Surface(self.background.get_size())
        self.dark_surface.fill((darkness, darkness, darkness))
        self.background.blit(self.dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.checking = checking
        if checking:
            self.ship.checking = True
        

    # FUNCTIONS ===========================================================================
    def update(self):
        
        for entity in reversed(self.entities):

            if entity.has_collision and not isinstance(entity, Debris):
                    entity.check_collision(self.entities)
            
            if isinstance(entity, Debris) and entity.is_collided:
                entity.check_collision(self.entities)
                    
            if isinstance(entity, Bullet) and (entity.x > self.screenX or entity.x < 0 or entity.y > self.screenY or entity.y < 0):
                try:
                    self.entities.remove(entity)
                except:
                    print("Error 001: I don't know why this happens, shouldn't break game")    
                          
            else:
                if entity.lives <= 0:        
                    if not isinstance(entity, Particles):
                        entity.update()
                        self.createParticles(entity)
                    
                    if not isinstance(entity, Ship) or not isinstance(entity, Player):
                        self.entities.remove(entity)
                        
                        if not isinstance(entity, Particles):
                            self.sounds[0].play()
                            self.tmp_score += 20
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
        
        self.entities = None
        
    def mainloop(self):   
        
        #test_var = 0 #TODO: ONLY USE FOR TESTING
        if self.checking:
            self.player.bullets = 100
            self.player.waypoints = 100
        
        pygame.event.set_allowed([pygame.QUIT,pygame.KEYDOWN])
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
                        tmp_waypoint = Waypoint(self.player.x,self.player.y)
                        self.waypoint_list.append(tmp_waypoint)
                        self.entities.append(tmp_waypoint)
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p and self.checking: #TODO: placeholder
                    self.ship.moving_flag = True
                    self.ship.velocity = 5
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.checking: #TODO: placeholder
                    self.ship.change_lagrange_points(False, self.screenX)
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.checking: #TODO: placeholder
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
                self.tmp_score += 30 * self.player.bullets
                self.tmp_score += 50 * self.player.waypoints
                tmp_screenY = self.screenY / 2
                self.tmp_score += 200 + int((tmp_screenY - abs(self.ship.y-tmp_screenY))*0.555556)
                return True, self.tmp_score
            
            # =================================================================
            
            # Important Game Logic ============================================
            
            if self.ship_initial_movement < self.ship_max_initial_movement and not self.ship.moving_flag:
                self.ship_initial_movement += 1
            elif not self.ship.moving_flag:
                self.ship.moving_flag = True
            
            self.rumble_channel.set_volume(self.rumble_volume)
            
            if (self.ship.can_move and self.ship.moving_flag) and not self.rumble_channel.get_busy():
                self.rumble_channel.play(self.sounds[5])
            
            if not ( self.ship.can_move and self.ship.moving_flag):
                self.rumble_channel.stop()
                
            if self.player.is_moving and not self.rumble2_channel.get_busy():
                self.rumble2_channel.set_volume(self.rumble2_volume)
                self.rumble2_channel.play(self.sounds[5])
            elif not self.player.is_moving:
                self.rumble2_channel.stop()
            
            # =================================================================
              
            self.update()
            self.render(self.screen)

            pygame.display.update()
            
            if not self.game_flag:
                self.game_over()
                
        return False, self.tmp_score
                
    def misc_ui_elements(self):
        # UI ELEMENT RENDERING ============================================
                
        if self.checking:
            text = self.font.render("Lagrange points: " + str(self.ship.lagrange_points), True, (255, 255, 255))
            self.screen.blit(text, (20,10))
            
            for waypoint in self.waypoint_list:
                text = self.font_small_bold.render("({:.3f}, {:.3f})".format(waypoint.x, waypoint.y), True, (0, 255, 0))
                self.screen.blit(text, (waypoint.x, waypoint.y - 10))
            
            
        
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
        if self.player.bullets > 12:
            tmp_bull = 12
            
        for i in range(tmp_bull):       
            self.HUD.append(Bullet_UI(10 + i*45, self.screenY-55,50))
            
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
        
        t_score = self.font.render(str(self.score + self.tmp_score), True, (255, 255, 255))
        
        text_width = t_score.get_width()
        text_x = (self.screenX - text_width) // 2
        
        self.screen.blit(t_score, (text_x, self.screenY-40))
        
        t_score = self.font_small.render("Score:", True, (255, 255, 255))
        
        text_width = t_score.get_width()
        text_x = (self.screenX - text_width) // 2
        
        self.screen.blit(t_score, (text_x, self.screenY-60))
        
        # ====================================================================
        
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        # Draw button with transparent color
        pygame.draw.rect(surface, transparent, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, black)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
         
#VARIABLES
transparent = (0, 0, 0, 0)
black = (0, 0, 0)

class Entity:
    
    def __init__(self, x, y, width, height, direction, image, collision_box = 0, has_collision = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.image = image
        if image != 0:
            self.scaled_image = []
            self.scaled_image.append(pygame.transform.scale(self.image, (self.width, self.height)))
        self.state = 0
        self.collision_box = collision_box
        self.has_collision = has_collision
        self.weight = 1
        self.lives = 1
        
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(r"assets\sound\hit.wav")

    def update(self):
        
        pass
    
    def load_sprites(self, folder):
        self.scaled_image = []
        file_list = sorted(os.listdir(folder))
        for filename in file_list:
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                self.scaled_image.append(pygame.transform.scale(image, (self.width, self.height)))

    
    def check_collision(self, entities):  
        if self.has_collision:   
            for entity in entities:
                if entity.has_collision and entity is not self:
                    if self.collision_box.colliderect(entity.collision_box):
                        self.handle_collision(entity)
                        entity.handle_collision(self)
                    
    def handle_collision(self, entity):
        # Redefine this function in the objects otherwise it will do nothing
        pass
                        
    def render(self, screen):
        
        rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)

class Bullet(Entity):
    
    def __init__(self, x, y, width = 5, height = 5, direction = 0):
        
        image = 0
        
        collision_box_scale = 0.8
        collision_box = pygame.Rect(x,y,width*collision_box_scale, height*collision_box_scale)
        
        super().__init__(x, y, width, height, direction, image, collision_box, has_collision=True)
        
        self.weight = 0.1
        self.velocity = 10
        
        dir_radians = -math.radians(self.direction+90)
        
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
    
    def update(self):
        
        self.collision_box.center = (self.x, self.y)

        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin
        
        pass
    
    def check_collision(self, entities):     
        for entity in entities:
            if entity.has_collision and entity is not self and not isinstance(entity,Player):
                if self.collision_box.colliderect(entity.collision_box):
                    entities.remove(self)
                    entity.handle_collision(self)
    
    def render(self, screen):
        pygame.draw.circle(screen, (255,0,0), (self.x,self.y), self.width/2)

class Debris(Entity):
    
    collide_direction = 0
    collide_velocity = 0
    is_collided = False
    
    def __init__(self, x, y, width, height, direction, image, has_collision, turn_speed, turn_direction):    
        
        self.velocity = 0
        self.turn_speed = turn_speed/100
        self.sprite_direction = 0
        
        if turn_direction:
            self.turn_speed = -self.turn_speed
            
        tmp_collision = 0
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width-(width * 0.4), height- (width * 0.4))
        
        image = pygame.image.load(image).convert_alpha()
        
        super().__init__(x, y, width, height, direction, image, tmp_collision, has_collision)
        
        self.lives = int(1 + ((height-50)/10))
        
    def update(self):
            
        self.velocity = self.collide_velocity
        self.direction = self.collide_direction
        self.sprite_direction += self.turn_speed
        
        self.collision_box.center = (self.x, self.y)
        
        if self.is_collided:
            self.x += self.velocity * self.dir_cos
            self.y += self.velocity * self.dir_sin
            self.collide_velocity -= 0.006
            
            if self.collide_velocity < 0.001:
                self.collide_velocity = 0
                self.is_collided = False        
        
    def handle_collision(self, entity):
        self.sound.play()
        
        dx = entity.x - self.x
        dy = entity.y - self.y

        collide_direction = math.degrees(math.atan2(dy, dx))
        dir_radians = math.radians(collide_direction+180)
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
        
        
        self.lives -= 1
        
        if abs(entity.velocity) < 0.001:
            self.collide_velocity = 0.2
        else:
            self.collide_velocity = abs(entity.velocity)*entity.weight
            
        
        self.is_collided = True
        
    def render(self, screen):
        
        rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.sprite_direction)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect)
        
class Particles(Entity):
    
    def __init__(self, x, y, width, height, direction, velocity, color):
        
        super().__init__(x, y, width, height, direction, image = 0, collision_box = 0, has_collision = False)
        
        self.velocity = velocity
        
        dir_radians = math.radians(self.direction)+180
        
        self.dir_cos = math.cos(dir_radians)
        self.dir_sin = math.sin(dir_radians)
        
        info = pygame.display.Info()
        self.screenX, self.screenY = info.current_w, info.current_h
        
        self.color = color
        pass
    
    def update(self):

        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin
        
        if self.x > self.screenX+100 or self.x < -100 or self.y > self.screenY+100 or self.y < -100:
            self.lives = 0
        
        pass
    
    def render(self, screen):
        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.width/2)
        
class Player(Entity):
    
    acceleration = 0.1
    deceleration = acceleration/3
    velocity_cap = 2
    tmp_rad = 0
    dir_cos = 0
    dir_sin = 0
    spacebar_pressed = False
    
    can_move = True
    
    collision_max_frames = 60*3
    collision_frame_counter = 0
    
    collision_max_shake_frame = 15
    collision_shake_frame = collision_max_shake_frame
    
    collision_max_cooldown_frame = 60*3
    collision_cooldown_frame = 30
    
    def __init__(self, 
                 x=0, 
                 y=0, 
                 width=50, 
                 height=50, 
                 velocity = 0, 
                 direction=0, 
                 turn_velocity= 1.3,
                 has_collision = True,
                 waypoints = 4,
                 bullets = 6):
        
        image = pygame.image.load("assets\player\player1.png").convert_alpha()
        
        tmp_collision = 0
        collision_box_scale = 0.6
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width*collision_box_scale, height*collision_box_scale)     
        
        super().__init__(x, y, width, height, direction, image, tmp_collision, True)
        
        self.scaled_image = []
        self.load_sprites("assets\player")
        
        self.lives = 3
        
        self.velocity = velocity
        self.turn_velocity = turn_velocity
        
        self.weight = 1.5
        
        self.bullets = bullets
        self.waypoints = waypoints
        
        self.state_save = self.state
        
        self.start_frame = 0
        self.max_start_frame = 60
        
        self.is_moving = False

    def update(self):
        
        self.is_moving = False
        self.state = self.state_save
        
        self.collision_box.center = (self.x, self.y)
        
        # Puts keys pressed in a keys list
        keys = pygame.key.get_pressed()
        
        # Calculates player direction in radians
        dir_radians = -math.radians(self.direction+90)
        
        # If the direction has not changed, do not recalculate
        if (dir_radians != self.tmp_rad):
            self.dir_cos = math.cos(dir_radians)
            self.dir_sin = math.sin(dir_radians)
            self.tmp_rad = dir_radians
        
        if self.start_frame < self.max_start_frame:
            self.start_frame += 1
            self.velocity += self.acceleration
            self.state = self.state_save + 1
            self.is_moving = True
            
        elif self.can_move:
            if keys[pygame.K_w]: #forward movement
                self.state = self.state + 1
                self.velocity += self.acceleration  
                self.is_moving = True        

            if keys[pygame.K_s]: #backwards movement
                self.state = self.state + 1
                self.velocity -= self.acceleration
                self.is_moving = True
                
            # Turns the player left or right depending on key pressed
            # (Might change it to acceleration based in future?)  
            if keys[pygame.K_a]:
                self.direction += self.turn_velocity
                
            if keys[pygame.K_d]:
                self.direction -= self.turn_velocity
            
        elif self.collision_frame_counter < self.collision_max_frames:
            self.collision_frame_counter += 1
        else:
            self.collision_frame_counter = 0
            self.can_move = True
        
        # Calculates new location based on velocity and direction
        self.x += self.velocity * self.dir_cos
        self.y += self.velocity * self.dir_sin    
        
        # This if block decelerates the player
        if self.velocity != 0:      
            self.velocity -= self.deceleration * (self.velocity / abs(self.velocity))
            
            # Because of float imprecision and whatnot, I just set velocity to zero
            # when it is really close to zero
            if abs(self.velocity) < 0.0005:
                self.velocity = 0
        
        # Ensures that velocity does not go beyond the player's velocity cap
        if abs(self.velocity) > self.velocity_cap:
            self.velocity = self.velocity_cap * (self.velocity / abs(self.velocity))
            
        if self.collision_cooldown_frame > 0:
            self.collision_cooldown_frame -= 1
        

    def handle_collision(self, entity):
        
        if not isinstance(entity, Bullet):
            dx = entity.x - self.x
            dy = entity.y - self.y

            direction = math.degrees(math.atan2(dy, dx))
            
            self.pull(-direction, -5)
            self.velocity = -self.velocity/2
            
            self.can_move = False
            
            self.collision_shake_frame = 0
                      
        else:
            self.collision_shake_frame = self.collision_max_shake_frame/4
        
        if self.collision_cooldown_frame == 0:
            if not isinstance(entity, Bullet):
                self.state_save += 2
                self.lives -= 1     
                self.collision_cooldown_frame = self.collision_max_cooldown_frame
    
    
    # Pulls the player towards a specified angle
    def pull(self, direction, velocity):
        
        dir_radians = -math.radians(direction)
        
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
    
    def render(self, screen):
        
        if self.collision_shake_frame <= self.collision_max_shake_frame:
            self.collision_shake_frame += 1
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x + random.randrange(-2,2), self.y + random.randrange(-2,2)))
        else:
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_image, rotated_rect)
        
class Ship(Entity):
    
    waypoint_step = 5
    lagrange_points = 3
    waypoint_line_render_index = 1
    follow_index = 0
    
    can_move = True
    moving_flag = False
    
    collision_max_shake_frame = 15
    collision_shake_frame = collision_max_shake_frame
    
    collision_max_cooldown = 60*4
    collision_cooldown_frame = 0
    
    line_color = (201, 49, 32)
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0, lagrange = 0, has_collision = True):
        
        tmp_collision = 0
        if has_collision:
            tmp_collision = pygame.Rect(x, y, width-(width * 0.4), height- (width * 0.4))    
            
        image = pygame.image.load("assets\ship\ship1.png").convert_alpha()       
        super().__init__(x, y, width, height, direction, image, tmp_collision, True)
        self.velocity = velocity
        self.lagrange = lagrange
        
        self.load_sprites("assets\ship")
        
        self.waypoint_line = [(0,0)]
        self.tmp_waypoint_line = []
        
        self.lives = 4
        
        self.state = 0
        self.state_save = 0
        
        self.checking = False
        self.font_small = pygame.font.Font(r"assets\font\nine0.ttf", 25)
        self.font_small.bold = True


    def update(self):
        
        self.state = self.state_save + 1 #State thing
        
        self.collision_box.center = (self.x, self.y)
        
        if self.can_move:
            self.state = self.state_save + 2
            pass
            
        if self.can_move and len(self.waypoint_line) < 5:
            
            if self.moving_flag:
                info = pygame.display.Info()
                self.move_ship(info.current_w + 300, info.current_h/2)
                
        elif self.can_move:
            
            if self.follow_index >= len(self.waypoint_line):
                self.follow_index = len(self.waypoint_line) - 1
                
            if self.moving_flag:
                tmpcoord = self.waypoint_line[self.follow_index]
                self.move_ship(tmpcoord[0],tmpcoord[1])
                
                if (self.x - tmpcoord[0]) > -0.1:
                    self.follow_index += 1
        else:
            self.collision_cooldown_frame += 1
            
            if self.collision_cooldown_frame >= self.collision_max_cooldown:
                self.collision_cooldown_frame = 0
                self.can_move = True
        
    def move_ship(self, target_x, target_y):
        
        # Gets the distance between target x y and current x y
        dx = target_x - self.x
        dy = target_y - self.y

        # Calculates direction towards target
        direction = math.degrees(math.atan2(dy, dx))
        # Changes face direction of the sprite
        self.direction = -direction - 90
        
        dir_cos = math.cos(math.radians(direction))
        dir_sin = math.sin(math.radians(direction))
        
        self.x += self.velocity * dir_cos
        self.y += self.velocity * dir_sin

    # Pulls the player towards a specified angle
    def pull(self, direction, velocity):
        dir_radians = -math.radians(direction)
        dir_cos = math.cos(dir_radians)
        dir_sin = math.sin(dir_radians)

        self.x += velocity * dir_cos
        self.y += velocity * dir_sin 
    
    def handle_collision(self, entity):
        self.sound.play()
        self.can_move = False
        self.collision_shake_frame = 0 
    
        if self.collision_cooldown_frame == 0:
            self.state_save += 2 #State function
            self.lives -= 1
    
    # Mostly a debug function that dynamically changes the amount of lagrange points
    # that are considered
    def change_lagrange_points(self, dir, screenX):
        if dir:
            self.lagrange_points += 1
        else:
            self.lagrange_points -= 1
        
        self.draw_waypoint_line(screenX)
    
    def draw_waypoint_line(self, screenX):
        # Empties the waypoint line array     
        self.waypoint_line = []
        
        # Creates a list of points from the left side of the screen to the right side
        # with a step of waypoint_step (because I don't need to generate points for
        # every x value)
        for x in range(0, screenX + 200, self.waypoint_step):
            self.waypoint_line.append((x,self.lagrange.lagrange(x,self.lagrange_points)))
    
    def init_tmp_waypoint_line(self, screenX):
        for x in range(0, screenX + 200, self.waypoint_step):
            self.tmp_waypoint_line.append([x,-10])
                 
    def render(self, screen):
        
        if len(self.waypoint_line) == len(self.tmp_waypoint_line):
            for i in range(0, len(self.tmp_waypoint_line)):
                self.tmp_waypoint_line[i][1] -= (self.tmp_waypoint_line[i][1] - self.waypoint_line[i][1])/5
            
            # Draws lines from x-1 point to x point for all lines in the waypoint_line list.
            # Obviously, it cannot start at zero because x-1 would not exist then    
            for i in range(1, len(self.tmp_waypoint_line)):
                
                if (i%2 == 0):
                    x = self.tmp_waypoint_line[i]
                    x_prev = self.tmp_waypoint_line[i-1]
                    
                    
                    #pygame.draw.circle(screen, (255,255,255), (x[0], x[1]), 2)
                    pygame.draw.line(screen, self.line_color, (x_prev[0], x_prev[1]), (x[0], x[1]), 3)
        
        # TODO: probably just delete this
        # Goes across the entire waypoint list and changes one line into green for a single
        # frame to create a small pulsing animation 
        if self.waypoint_line_render_index < len(self.waypoint_line):
            x = self.waypoint_line[self.waypoint_line_render_index]
            x_prev = self.waypoint_line[self.waypoint_line_render_index-1]
            
            pygame.draw.circle(screen, self.line_color, x,4)
            pygame.draw.circle(screen, self.line_color, x_prev,2)
            
            if self.checking:
                text = self.font_small.render("({:.3f}, {:.3f})".format(x[0], x[1]), True, (0, 255, 0))
                screen.blit(text, (x[0], x[1]))
            
            pygame.draw.line(screen, self.line_color, (x_prev[0],x_prev[1]), (x[0], x[1]), 8)
            self.waypoint_line_render_index += 1
        
        else:
            self.waypoint_line_render_index = 1
        
        # Renders the ship image normally
        if self.collision_shake_frame <= self.collision_max_shake_frame:
            self.collision_shake_frame += 1
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x + random.randrange(-2,2), self.y + random.randrange(-2,2)))
        else:       
            rotated_image = pygame.transform.rotate(self.scaled_image[self.state], self.direction)
            rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_image, rotated_rect)
        
        #DEBUG RENDERING
        #pygame.draw.rect(screen,(0,255,0) ,self.collision_box)

class Waypoint(Entity):
    
    def __init__(self, x=0, y=0, width=50, height=50, velocity=1, direction=0):
        image = pygame.image.load("assets\waypoint\waypoint.png").convert_alpha()       
        super().__init__(x, y, width, height, direction, image)
        self.velocity = velocity


    def update(self):
        pass
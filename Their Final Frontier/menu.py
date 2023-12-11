import os
import pygame
import pygame_gui
from button import Button

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
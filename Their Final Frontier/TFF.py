import pygame
from player import Player
from ship import Ship
from lagrange import Lagrange
from waypoint import Waypoint

# Pygame stuff ========================================================================
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Creates the display
screenX = 1500
screenY = 600
screen = pygame.display.set_mode((screenX,screenY))

# Title and Icon
pygame.display.set_caption("Their Final Frontier Alpha")
window_icon = pygame.image.load("assets\window_icon.png")  # Update the file path here
pygame.display.set_icon(window_icon)

# Object initialization ======================================a==========================
player = Player(280, 300)
ship = Ship(0,400,width=150,height=150,lagrange=Lagrange([(0,screenY/2)]))

entities = [player,ship]

font = pygame.font.Font(None, 36)

# FUNCTIONS ===========================================================================
def update():
    for entity in entities:
        entity.update()
    
def render(screen):
    for entity in reversed(entities):
        entity.render(screen)

# MAIN ================================================================================
if __name__ == "__main__":
    # Main game loop

    running = True
    while running:
        
        clock.tick(FPS)
        # print("Current FPS: ", clock.get_fps())
        screen.fill((0,0,0)) #just draws black
        
        # Ensures that all events in the game are run
        for event in pygame.event.get():
            
            # Quits game if pygame detects the quit event type
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                entities.append(Waypoint(player.x,player.y))
                ship.lagrange.add_point(player.x,player.y)
                ship.draw_waypoint_line(screenX)
            
            # EVENTS FOR DEBUGGING ===============================================================  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #TODO: placeholder
                ship.moving_flag = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT: #TODO: placeholder
                ship.change_lagrange_points(False, screenX)
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT: #TODO: placeholder
                ship.change_lagrange_points(True, screenX)
         
        text = font.render("Lagrange points: " + str(ship.lagrange_points), True, (255, 255, 255))
        screen.blit(text, (20,20))       
        update()
        render(screen)
                
        pygame.display.update()

    
    



import pygame
import pygame_gui

pygame.init()

window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(pygame.Color('#000000'))

    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
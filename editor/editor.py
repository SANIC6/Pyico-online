import pygame
from constants import COLORS

pygame.init()
WINDOW_SIZE = (128,128)
DISPLAY_SCALE = 4
screen = pygame.display.set_mode((WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE))
pygame.display.set_caption("Pyico Editor")

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_button_pressed = False
        self.mouse_idle_img = pygame.image.load("editor/assets/mouse/mouse_idle.png").convert_alpha()

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.left_button_pressed = pygame.mouse.get_pressed()[0]
    def draw(self, surface):
        surface.blit(self.mouse_idle_img, (self.x, self.y))


class Editor:
    def __init__(self):
        self.running = True
        self.game_screen = pygame.Surface(WINDOW_SIZE)
        self.mouse = Mouse()

    def run(self):
        while self.running:
            self.mouse.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.game_screen.fill((255, 255, 255))
            self.mouse.draw(self.game_screen)
            screen.blit(pygame.transform.scale(self.game_screen, (WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE)), (0, 0))
            pygame.display.flip()

        pygame.quit()

Editor().run()
    
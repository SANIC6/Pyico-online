from pathlib import Path

import pygame

from tools.constants import COLORS

import logging

logger = logging.getLogger(__name__)

WINDOW_SIZE = (128,128)
DISPLAY_SCALE = 4
_ASSETS_DIR = Path(__file__).resolve().parent / "editor/assets"

class Mouse:
    def __init__(self):
        self.pos =[0,0]
        self.left_button_pressed = False
        self.mouse_idle_img = pygame.image.load(str(_ASSETS_DIR / "mouse" / "mouse_idle.png")).convert_alpha()
    
    def states(self,sprite_editor_rect):
        if sprite_editor_rect.collidepoint(tuple(self.pos)):
            print('Sprite-Editor')
        else:
            print('not in ')
    def update(self,sprite_editor_box):
        self.pos = list(pygame.mouse.get_pos())
        
        self.pos[0] /= DISPLAY_SCALE
        self.pos[1] /= DISPLAY_SCALE


        
        self.states(sprite_editor_box)

        if pygame.mouse.get_pressed()[0]:
            self.left_button_pressed = True
        else:
            self.left_button_pressed = False
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > WINDOW_SIZE[0]:
            self.pos[0] = WINDOW_SIZE[0]
        if self.pos[1] > WINDOW_SIZE[1]:
            self.pos[1] = WINDOW_SIZE[1]
    def draw(self, surface):
        
        surface.blit(self.mouse_idle_img, (self.pos[0], self.pos[1]))


class Editor:
    def __init__(self):
        self.running = True
        self.game_screen = pygame.Surface(WINDOW_SIZE)
        pygame.mouse.set_visible(False)
        self.state = 'pixel'
        self.screen = pygame.display.set_mode((WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE))
        self.mouse = Mouse()
        self.sprite_editor_box = pygame.Rect(8,16,64,64)
        self.background = pygame.Rect(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1])
        self.top_bar = pygame.Rect(0, 0, WINDOW_SIZE[0], 8)
        self.bottom_bar = pygame.Rect(0, WINDOW_SIZE[1]-8, WINDOW_SIZE[0], 8)
        self.sprites_background = pygame.Rect(0, WINDOW_SIZE[1]-40, WINDOW_SIZE[0], 48)
        pygame.display.set_caption("Pyico Editor")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.game_screen.fill((255, 255, 255))
            pygame.draw.rect(self.game_screen, COLORS[8], self.background)
            pygame.draw.rect(self.game_screen, COLORS[5], self.top_bar)
            pygame.draw.rect(self.game_screen, COLORS[0], self.sprites_background)
            pygame.draw.rect(self.game_screen, COLORS[5], self.bottom_bar)
            pygame.draw.rect(self.game_screen, COLORS[0], self.sprite_editor_box)

            self.mouse.update(self.sprite_editor_box)
            self.mouse.draw(self.game_screen)
            self.screen.blit(pygame.transform.scale(self.game_screen, (WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE)), (0, 0))
            pygame.display.flip()

        pygame.quit()


def main() -> None:
    pygame.init()
    Editor().run()


if __name__ == "__main__":
    main()
    
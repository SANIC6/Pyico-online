from pathlib import Path

import pygame

from tools.constants import COLORS

import logging

logger = logging.getLogger(__name__)

WINDOW_SIZE = (160,144)
DISPLAY_SCALE = 4
_ASSETS_DIR = Path(__file__).resolve().parent / "editor/assets"

class Mouse:
    def __init__(self,game):
        self.pos =[0,0]
        self.left_button_pressed = False
        self.right_button_pressed = False
        self.color_index = 0
        self.game = game
        self.img_num = 0
        self.selected_sprite = 0
        self.state = 'sprite-editor'
        self.canvas: list = [[None] * 8 for _ in range(8)]
        self.cell_size = 8
        self.mouse_idle_img = pygame.image.load(str(_ASSETS_DIR / "mouse" / "mouse_idle.png")).convert_alpha()
    
    def palette(self):
        if not self.left_button_pressed:
            return
        for i, rect in enumerate(self.game.color_rect):
            if rect.collidepoint(int(self.pos[0]), int(self.pos[1])):
                if i in COLORS:
                    self.color_index = i
                break
    def select_sprite(self):
        if not self.left_button_pressed:
            return
        for i, rect in enumerate(self.game.sprite_rects):
            if rect.collidepoint(int(self.pos[0]), int(self.pos[1])):
                if i != self.selected_sprite:
                    self.selected_sprite = i
                    self.canvas = self.game.get_or_create_sprite(i)
                break
    def states(self,sprite_editor_rect):
        if sprite_editor_rect.collidepoint(int(self.pos[0]), int(self.pos[1])):
            self.state = 'sprite-editor'
        else:
            self.state = 'idk'
    def sprite_editor(self, sprite_editor_box):
        if not self.left_button_pressed and not self.right_button_pressed:
            return
        cx = int((self.pos[0] - sprite_editor_box.x) // self.cell_size)
        cy = int((self.pos[1] - sprite_editor_box.y) // self.cell_size)
        if 0 <= cx < 8 and 0 <= cy < 8:
            if self.left_button_pressed:
                self.canvas[cy][cx] = self.color_index
            elif self.right_button_pressed:
                self.canvas[cy][cx] = None
    def handle_input(self):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            self.left_button_pressed = True
        else:
            self.left_button_pressed = False
        if len(pressed) > 2 and pressed[2]:
            self.right_button_pressed = True
        else:
            self.right_button_pressed = False
        self.palette()
        self.select_sprite()
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[0] > WINDOW_SIZE[0]:
            self.pos[0] = WINDOW_SIZE[0]
        if self.pos[1] > WINDOW_SIZE[1]:
            self.pos[1] = WINDOW_SIZE[1]
    def update(self,sprite_editor_box):
        self.pos = list(pygame.mouse.get_pos())
        self.pos[0] /= DISPLAY_SCALE
        self.pos[1] /= DISPLAY_SCALE
        self.handle_input()
        self.states(sprite_editor_box)
        if self.state == 'sprite-editor':
            self.sprite_editor(sprite_editor_box)
    def draw_canvas(self, surface, sprite_editor_box):
        for y in range(8):
            for x in range(8):
                c = self.canvas[y][x]
                if c is not None and c in COLORS:
                    pygame.draw.rect(surface, COLORS[c], pygame.Rect(sprite_editor_box.x + x * self.cell_size, sprite_editor_box.y + y * self.cell_size, self.cell_size, self.cell_size))
    def draw(self, surface):
        
        surface.blit(self.mouse_idle_img, (self.pos[0], self.pos[1]))


class Editor:
    def __init__(self):
        self.running = True
        self.game_screen = pygame.Surface(WINDOW_SIZE)
        pygame.mouse.set_visible(False)
        self.sprite_data = {}
        self.state = 'pixel'
        self.screen = pygame.display.set_mode((WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE))
        self.color_rect = []
        self.sprite_rects = []
        self.sprite_cols = 9
        self.sprite_rows = 15
        self.mouse = Mouse(self)
        self.mouse.canvas = self.get_or_create_sprite(0)
        self.sprite_editor_box = pygame.Rect(8,16,64,64)
        self.background = pygame.Rect(0,0,WINDOW_SIZE[0],WINDOW_SIZE[1])
        self.top_bar = pygame.Rect(0, 0, WINDOW_SIZE[0], 8)
        self.bottom_bar = pygame.Rect(0, WINDOW_SIZE[1]-8, WINDOW_SIZE[0], 8)
        self.pallete_rect = pygame.Rect(8-3, 128-40-3, (8*8)+6, 16+6)
        self.sprites_background = pygame.Rect(128-48, 16, 72, WINDOW_SIZE[1])
        pygame.display.set_caption("Pyico Editor")

    @staticmethod
    def new_blank_canvas():
        return [[None] * 8 for _ in range(8)]
    def get_or_create_sprite(self, index):
        if index not in self.sprite_data:
            self.sprite_data[index] = self.new_blank_canvas()
        return self.sprite_data[index]
    def draw_pallete(self,x_pos,y_pos):
        self.color_rect.clear()
        color_index = 0
        for y in range(2):
            for x in range(8):
                if color_index < len(COLORS):
                    rect = pygame.Rect(x_pos+x*8, y_pos+y*8, 8, 8)
                    pygame.draw.rect(self.game_screen, COLORS[color_index], rect)
                    self.color_rect.append(rect)
                    if color_index == self.mouse.color_index:
                        pygame.draw.rect(self.game_screen, (255, 255, 255), rect, 1)
                color_index += 1

    def draw_sprite_slots(self):
        self.sprite_rects.clear()
        for y in range(self.sprite_rows):
            for x in range(self.sprite_cols):
                rect = pygame.Rect(
                    self.sprites_background.x + x * 8,
                    self.sprites_background.y + y * 8,
                    8, 8,
                )
                pygame.draw.rect(self.game_screen, COLORS[0], rect)
                self.sprite_rects.append(rect)
                if len(self.sprite_rects) - 1 == self.mouse.selected_sprite:
                    pygame.draw.rect(self.game_screen, (255, 255, 255), rect, 1)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.game_screen.fill((255, 255, 255))
            pygame.draw.rect(self.game_screen, COLORS[1], self.background)
            pygame.draw.rect(self.game_screen, COLORS[5], self.top_bar)
            pygame.draw.rect(self.game_screen, COLORS[0], self.sprites_background)
            pygame.draw.rect(self.game_screen, COLORS[5], self.bottom_bar)
            pygame.draw.rect(self.game_screen, COLORS[0], self.sprite_editor_box)
            pygame.draw.rect(self.game_screen, COLORS[0], self.pallete_rect,3)
            self.draw_pallete(8, 128-40)
            self.draw_sprite_slots()
            self.mouse.update(self.sprite_editor_box)
            self.mouse.sprite_editor(self.sprite_editor_box)
            self.mouse.draw_canvas(self.game_screen, self.sprite_editor_box)
            self.mouse.draw(self.game_screen)
            self.screen.blit(pygame.transform.scale(self.game_screen, (WINDOW_SIZE[0] * DISPLAY_SCALE, WINDOW_SIZE[1] * DISPLAY_SCALE)), (0, 0))
            pygame.display.flip()

        pygame.quit()


def main() -> None:
    pygame.init()
    Editor().run()


if __name__ == "__main__":
    main()
    
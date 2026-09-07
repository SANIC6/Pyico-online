import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pyico Editor")

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_button_pressed = False

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.left_button_pressed = pygame.mouse.get_pressed()[0]

class Editor:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((255, 255, 255))
            pygame.display.flip()

        pygame.quit()
    
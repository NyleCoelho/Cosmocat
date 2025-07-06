import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, GAMEOVER_OPTION

class WinScreen:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font('./assets/fonts/title.ttf', 50)
        self.option = 0
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.window.fill((0, 0, 0))
            title = self.font.render("Você Venceu!", True, C_WHITE)
            self.window.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 200))

            for i, opt in enumerate(GAMEOVER_OPTION):
                color = C_WHITE
                label = self.font.render(opt, True, color)
                x = WIN_WIDTH // 2 - label.get_width() // 2
                y = 350 + i * 60
                self.window.blit(label, (x, y))

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.option = (self.option - 1) % len(GAMEOVER_OPTION)
                    elif event.key == pygame.K_DOWN:
                        self.option = (self.option + 1) % len(GAMEOVER_OPTION)
                    elif event.key == pygame.K_RETURN:
                        return GAMEOVER_OPTION[self.option]

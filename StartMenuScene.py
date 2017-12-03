
import sys
from game import *

from menu import MenuScene


class StartMenuScene(MenuScene):

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        super(StartMenuScene, self).on_enter(previous_scene)

        def new_game():
            self.application.change_scene(get_message_scene())

        self.add_option("New Game", new_game, 48)
        self.add_option("Quit", sys.exit, 48)

        title_font = pygame.font.Font("assets/Creepster-Regular.ttf", 72)
        self.title_image = title_font.render("Adventitious Asylum", True, (255, 255, 255))

        # self.backdrop = pygame.image.load("assets/hallway.jpg").convert()
        self.backdrop = pygame.image.load("assets/cough.jpg").convert()
        scale_down = 0.666666
        backdrop_rect = self.backdrop.get_rect()
        self.backdrop = pygame.transform.smoothscale(self.backdrop, (int(backdrop_rect.width * scale_down), int(backdrop_rect.height * scale_down)))

    def draw(self, screen):
        screen.fill(black)

        screen.blit(self.backdrop, (0, 0))

        self.draw_menu_options(screen)

        screen.blit(self.title_image, (SCREEN_WIDTH / 2 - self.title_image.get_rect().width / 2, 50))

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(StartMenuScene())


import sys
from game import *

from menu import MenuScene


class MessageScene(MenuScene):

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        super(MessageScene, self).on_enter(previous_scene)

        def new_game():
            self.application.change_scene(get_platformer_scene())

        self.next_y += 200

        self.font_size = 48

        self.add_option("Escape!!!", new_game, self.font_size)

        messages = [
            "I'm sick of being cooped up in this asylum.",
            "There's nothing wrong with me anyway.",
            "I wonder if I can get outside?",
        ]

        message_font = pygame.font.Font("assets/GloriaHallelujah.ttf", 36)
        self.message_images = []
        for message in messages:
            self.message_images.append(message_font.render(message, True, (255, 255, 255)))

        self.backdrop = pygame.image.load("assets/lostPlace.jpg").convert()
        scale_down = 0.5211
        backdrop_rect = self.backdrop.get_rect()
        self.backdrop = pygame.transform.smoothscale(self.backdrop, (int(backdrop_rect.width * scale_down), int(backdrop_rect.height * scale_down)))

    def draw(self, screen):
        screen.fill(black)

        screen.blit(self.backdrop, (0, 0))

        self.draw_menu_options(screen)

        y_pos = 50
        for message_image in self.message_images:
            screen.blit(message_image, (80, y_pos))
            y_pos += self.font_size

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(MessageScene())


from game import *

from GameScene import GameScene


class PlatformerScene(GameScene):

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def draw(self, screen):
        screen.fill((50, 100, 255))z


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())


from game import *

from GameScene import GameScene


class BattleScene(GameScene):

    def on_enter(self, previous_scene):
        super(BattleScene, self).on_enter(previous_scene)

    def draw(self, screen):

        screen.fill((50, 100, 255))


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(BattleScene())

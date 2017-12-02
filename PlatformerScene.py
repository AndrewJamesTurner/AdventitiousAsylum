
from game import *

from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *

class PlatformerScene(GameScene):
    def __init__(self):
        self.rq = RenderQueue()
        LevelObjectPattern.init()
        testLO = {
            'type': "'naut",
            'x': 7,
            'y': 3
        }
        self.levelObjects = [LevelObject(testLO)]

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def draw(self, screen):
        for lo in self.levelObjects:
            lo.draw(self.rq)
        self.rq.flush(screen)


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())

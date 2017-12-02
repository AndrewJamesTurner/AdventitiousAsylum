
from game import *

from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *
from Level import Level

class PlatformerScene(GameScene):
    def __init__(self):
        self.rq = RenderQueue()
        LevelObjectPattern.init()

        self.level = Level.load('test.json')
        self.spedec = SpecEcController(LevelEntity(7, 0, 1, 2, 'arrow.png'))
        self.level.addEntity(self.spedec.le)

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.spedec.setInputs(keys)
        self.level.update(dt / 1000.0)

    def draw(self, screen):
        self.level.draw(self.rq)
        self.rq.flush(screen)

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())

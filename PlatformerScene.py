
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
        self.level.addEntity(LevelEntity(9,0,1,2,'health.png'))

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        print(self.level.collidingEntities(self.spedec.le))

        self.spedec.setInputs(keys)
        self.level.update(dt / 1000.0)

        # If we do a death animation, we might not adjust this
        self.camera_x = self.spedec.le.centre
        self.camera_y = self.spedec.le.middle

    def cameraPosition(self):
        def limit(aim, extent, limit0, limit1):
            if extent > (limit1 - limit0):
                return (limit0 + limit1) / 2
            return min(max(aim, limit0 + extent / 2), limit1 - extent / 2)

        x = limit(self.camera_x * BLOCK_SIZE, SCREEN_WIDTH,  0, self.level.width  * BLOCK_SIZE )
        y = limit(self.camera_y * BLOCK_SIZE, SCREEN_HEIGHT, 0, self.level.height * BLOCK_SIZE )
        return ( x - SCREEN_WIDTH / 2, y - SCREEN_HEIGHT / 2)

    def draw(self, screen):
        # Work out the camera position: Where the camera centres on

        self.level.surfdata.debug_draw(self.rq)
        self.level.draw(self.rq)
        self.rq.flush(screen, self.cameraPosition())

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())


from game import *

from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *
from Level import *
from sharedValues import get_shared_values
from player import Player
from orderly import Orderly


class PlatformerScene(GameScene):

    def __init__(self):

        self.rq = RenderQueue()
        LevelObjectPattern.init()
        Spawner.init()

        get_shared_values().player = Player("spedecWoman")

        self.level = Level.load('test.json')
        self.spedec = SpedEcController(self.level.getSpedEcEntity())
        self.aimCamera(self.spedec.le.centre, self.spedec.le.middle)

        self.level.addEntity(self.spedec.le)


    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.spedec.setInputs(keys)

        # Go back to last lamppost if we run out of health
        if get_shared_values().player.health <= 0:
            # TODO: reset this scene to the last lamppost
            self.application.change_scene(get_game_over_scene())

        # TODO: Win if we get to the end of the level
        # if self.spedec.??x position?? > ??level width??:
        #     self.application.change_scene(get_win_scene())

        for colliding_entity in self.level.collidingEntities(self.spedec.le):
            self.handle_collision(colliding_entity)

        #print(self.level.collidingEntities(self.spedec.le))
        self.level.setScreenRect(self.camera_left, self.camera_top, self.camera_right, self.camera_bottom)

        self.level.update(dt / 1000.0)

        # If we do a death animation, we might not adjust this
        self.aimCamera(self.spedec.le.centre, self.spedec.le.middle)

    def handle_collision(self, entity):
        """
        Called when the player collides with an entity.
        :param entity: The entity that the player collided with
        """
        # TODO: Only start a battle if entity is an orderly
        # if entity.??? == 'orderly':
        # TODO: Set the type of orderly in the shared values, so the battle scene can show the correct image
        get_shared_values().orderly = Orderly("doctor")
        # get_shared_values().enemy = ???
        self.level.levelEntities.remove(entity)  # safe to remove here, because if we lose the battle we won't be staying here
        self.application.change_scene(get_battle_scene())

    def aimCamera(self, x, y):
        def limit(aim, extent, limit0, limit1):
            if extent > (limit1 - limit0):
                return (limit0 + limit1) / 2
            return min(max(aim, limit0 + extent / 2), limit1 - extent / 2)

        blocks_w = SCREEN_WIDTH  / BLOCK_SIZE
        blocks_h = SCREEN_HEIGHT / BLOCK_SIZE

        x = limit(x, blocks_w, 0, self.level.width  )
        y = limit(y, blocks_h, 0, self.level.height )
        self.camera_left   = x - blocks_w / 2
        self.camera_right  = x + blocks_w / 2
        self.camera_top    = y - blocks_h / 2
        self.camera_bottom = y + blocks_h / 2

    def cameraPosition(self):
        return ( self.camera_left * BLOCK_SIZE, self.camera_top * BLOCK_SIZE )

    def draw(self, screen):
        #self.level.surfdata.debug_draw(self.rq)
        self.level.draw(self.rq)
        self.rq.flush(screen, camera_position = self.cameraPosition())

if __name__ == '__main__':

    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())

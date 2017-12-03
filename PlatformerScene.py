
from game import *

from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *
from Level import *

class PlatformerScene(GameScene):
    def __init__(self):
        self.rq = RenderQueue()
        LevelObjectPattern.init()
        Spawner.init()

        self.level = Level.load('test.json')
        self.spedec = SpedEcController(self.level.playerentity)
        self.level.addEntity(self.spedec.le)
        Spawner.setPlayerEntity(self.spedec.le)

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Go back to last lamppost if we run out of health
        if get_shared_values().health <= 0:
            # TODO: reset this scene to the last lamppost
            self.application.change_scene(get_game_over_scene())

        # TODO: Win if we get to the end of the level
        # if self.spedec.??x position?? > ??level width??:
        #     self.application.change_scene(get_win_scene())

        for colliding_entity in self.level.collidingEntities(self.spedec.le):
            self.handle_collision(colliding_entity)

        self.spedec.setInputs(keys)
        self.level.update(dt / 1000.0)

        # If we do a death animation, we might not adjust this
        self.camera_x = self.spedec.le.centre
        self.camera_y = self.spedec.le.middle

    def handle_collision(self, entity):
        """
        Called when the player collides with an entity.
        :param entity: The entity that the player collided with
        """
        # TODO: Only start a battle if entity is an orderly
        # if entity.??? == 'orderly':
        # TODO: Set the type of orderly in the shared values, so the battle scene can show the correct image
        # get_shared_values().enemy = ???
        self.level.levelEntities.remove(entity)  # safe to remove here, because if we lose the battle we won't be staying here
        self.application.change_scene(get_battle_scene())

    def cameraPosition(self):
        def limit(aim, extent, limit0, limit1):
            if extent > (limit1 - limit0):
                return (limit0 + limit1) / 2
            return min(max(aim, limit0 + extent / 2), limit1 - extent / 2)

        x = limit(self.camera_x * BLOCK_SIZE, SCREEN_WIDTH,  0, self.level.width  * BLOCK_SIZE )
        y = limit(self.camera_y * BLOCK_SIZE, SCREEN_HEIGHT, 0, self.level.height * BLOCK_SIZE )
        return ( x - SCREEN_WIDTH / 2, y - SCREEN_HEIGHT / 2)

    def draw(self, screen):
        #self.level.surfdata.debug_draw(self.rq)
        self.level.draw(self.rq)
        self.rq.flush(screen, camera_position = self.cameraPosition())

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())

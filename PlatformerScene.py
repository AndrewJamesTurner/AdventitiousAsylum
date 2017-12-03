
from game import *

from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *
from Level import *
from sharedValues import get_shared_values
from player import Player
from orderly import Orderly

from BattleScene import draw_health_bar

class PlatformerScene(GameScene):

    def __init__(self):
        self.rq = RenderQueue()
        LevelObjectPattern.init()
        Spawner.init()
        self.itemgen = ItemGenerator()

        get_shared_values().player = Player("spedecWoman")

        self.resetLevel()

    def resetLevel(self):
        self.level = Level.load(get_shared_values().levelfile)
        self.spedec = SpedEcController(self.level.getSpedEcEntity())
        self.aimCamera(self.spedec.le.centre, self.spedec.le.middle)

    def on_enter(self, previous_scene):
        super(PlatformerScene, self).on_enter(previous_scene)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.spedec.onKeydown(event.key)

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
        self.handle_collisions()
        self.level.setScreenRect(self.camera_left, self.camera_top, self.camera_right, self.camera_bottom)
        self.level.update(dt / 1000.0)
        self.spedec.flushInputs()

        # If we do a death animation, we might not adjust this
        self.aimCamera(self.spedec.le.centre, self.spedec.le.middle)

    def handle_collisions(self):
        """
        Checks collisions and applies rules based on that
        """
        colliding = self.level.collidingEntities(self.spedec.le)
        matches = { t:[ e for e in colliding if e.archetype == t]
                    for t in ['health','orderly','weapon'] }

        # Process health items first
        for health in matches['health']:
            get_shared_values().player.adjust_health(health.definition['amount'])
            self.level.dropEntity(health)

        # Process weapon pickups
        if self.spedec.get_item and matches['weapon']:
            weapon = matches['weapon'][0]
            self.level.dropEntity(weapon)
            game_item = self.itemgen.getItemByName(weapon.definition['name'])
            itemDropped = get_shared_values().player.add_item(game_item)
            if itemDropped:
                weaponName = itemDropped.name
                weapons = Spawner.entities['weapon']
                definitions = [ d for d in weapons if d['name'] == weaponName ]
                if definitions:
                    x, y = (self.spedec.le.centre, self.spedec.le.middle)
                    entity = LevelEntity(x, y, 'weapon', definitions[0])
                    self.level.addEntity(entity)
                else:
                    print("Can't drop item '%s'!" % weaponName)

        # Only process the first orderly to collide with
        if matches['orderly']:
            orderly = matches['orderly'][0]
            get_shared_values().orderly = Orderly(orderly.definition['name'])
            self.level.dropEntity(orderly)
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

    def drawInterface(self):
        margin = 8
        healthPercent = get_shared_values().player.health / get_shared_values().player.max_health
        draw_health_bar(self.rq, margin, margin, healthPercent,
                        SCREEN_WIDTH / 2 - 2*margin, 16)
        weapons = get_shared_values().player.items
        item_spacing = ( (SCREEN_WIDTH / 2) - (4 * THUMB_SIZE) ) / 5
        x = SCREEN_WIDTH / 2
        for i in weapons:
            x += item_spacing
            self.rq.add((x, margin), i.thumb)
            x += THUMB_SIZE

    def draw(self, screen):
        #self.level.surfdata.debug_draw(self.rq)
        self.level.draw(self.rq)
        self.rq.flush(screen, camera_position = self.cameraPosition())
        self.drawInterface()
        self.rq.flush(screen, erase=False)

if __name__ == '__main__':

    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(PlatformerScene())

from game import *
import pygame

class LevelEntity:
    """
    An entity that can roam around a level.
    Physics can be done on entities, and they interact with the surfdata.
    """
    def __init__(self, x, y, archetype, entityDefinition):
        self.archetype = archetype
        e = entityDefinition
        self.definition = e
        w = float( e['width']  * BLOCKS_PER_M )
        h = float( e['height'] * BLOCKS_PER_M )
        self.top = float(y)
        self.left = float(x)
        self.width = w
        self.height = h
        self.vel_x = 0
        self.vel_y = 0

        # Results of physics stuff - usable on the next frame
        self.hcontact = 0
        self.vcontact = 0
        self.offscreen = 0

        # Input actions
        self.go_u = 0
        self.go_d = 0
        self.go_l = 0
        self.go_r = 0
        self.jump = 0
        self.grab = 0

        if 'image' in e:
            rawimage = pygame.image.load(os.path.join(ASSETS_PATH, e['image'])).convert_alpha()
            self.image = pygame.transform.smoothscale(rawimage, (int(w * BLOCK_SIZE), int(h * BLOCK_SIZE)))
        else:
            self.image = None

    def draw(self, rq):
        draw_position = (self.left * BLOCK_SIZE, self.top * BLOCK_SIZE)
        if self.image is not None:
            rq.add(draw_position, self.image)

    def move(self, dx, dy):
        self.left += dx
        self.top += dy

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def centre(self):
        return self.left + 0.5 * self.width

    @property
    def middle(self):
        return self.top + 0.5 * self.height

class SpedEcController:
    """
    The player object (SPAREDESK)
    """
    def __init__(self, entity):
        self.le = entity
        self.flushInputs()

    def setInputs(self, keys):
        l = self.le
        l.go_u  = keys[pygame.K_UP] or keys[pygame.K_w]
        l.go_d  = keys[pygame.K_DOWN] or keys[pygame.K_s]
        l.grab  = keys[pygame.K_LSHIFT]
        l.go_l  = keys[pygame.K_LEFT] or keys[pygame.K_a]
        l.go_r  = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    def onKeydown(self, key):
        if key == pygame.K_RSHIFT or  key == pygame.K_TAB:
            self.get_item = 1
        elif key == pygame.K_SPACE:
            self.le.jump = 1

    def flushInputs(self):
        self.get_item = 0
        self.le.jump = 0

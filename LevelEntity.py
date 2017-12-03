from game import *
import pygame
from animation import Animation

class LevelEntity:
    """
    An entity that can roam around a level.
    Physics can be done on entities, and they interact with the surfdata.
    """
    def __init__(self, x, y, archetype, entityDefinition):
        self.archetype = archetype
        e = entityDefinition
        self.definition = e
        w = float( e['width'] )
        h = float( e['height'] )
        self.top = float(y)
        self.left = float(x)
        self.width = w
        self.height = h
        self.vel_x = 0
        self.vel_y = 0

        # Results of physics stuff - usable on the next frame
        self.hcontact = 0
        self.vcontact = 0

        # Input actions
        self.go_u = 0
        self.go_d = 0
        self.go_l = 0
        self.go_r = 0
        self.jump = 0
        self.grab = 0

        self.anim = None

        if archetype == 'player':
            self.anim = Animation(True,
                                  pygame.image.load('assets/characters/spedec-2/spedec-man-walk-2-sheet.png'), 180)
        else:
            if 'image' in e:
                rawimage = pygame.image.load(os.path.join(ASSETS_PATH, e['image'])).convert_alpha()
                self.image = pygame.transform.smoothscale(rawimage, (int(w * BLOCK_SIZE), int(h * BLOCK_SIZE)))
            else:
                self.image = None

    def draw(self, rq):
        draw_position = (self.left * BLOCK_SIZE, self.top * BLOCK_SIZE)

        im = None

        scale = (1, 1)
        if self.anim is not None:
            self.anim.step()
            im = self.anim.get_current_frame()
            sf_x = (1.0*BLOCK_SIZE*self.width)/im.get_width()
            sf_y = (1.0*BLOCK_SIZE*self.height)/im.get_height()
            scale = (sf_x, sf_y)
        elif self.image is not None:
            im = self.image

        if im is not None:
            rq.add(draw_position, im, scale, 50000)

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
        l.jump  = keys[pygame.K_SPACE]
        l.go_u  = keys[pygame.K_UP] or keys[pygame.K_w]
        l.go_d  = keys[pygame.K_DOWN] or keys[pygame.K_s]
        l.grab  = keys[pygame.K_LSHIFT]
        l.go_l  = keys[pygame.K_LEFT] or keys[pygame.K_a]
        l.go_r  = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    def onKeydown(self, key):
        if key == pygame.K_RSHIFT or  key == pygame.K_TAB:
            self.get_item = 1

    def flushInputs(self):
        self.get_item = 0

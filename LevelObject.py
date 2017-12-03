
import math
import json
from pygame import Surface, Rect, SRCALPHA

from game import *
from constants import *
from SurfData import *

class LevelObjectPattern:
    """
    A pattern for a level object.
    Has an image, which is shared by each LevelObject that uses this pattern
    """
    patternDefs = None
    pattern = {}

    def __init__(self, patternDefinition, id=None):
        p = patternDefinition
        self.definition = p
        self.id = id
        asset = p['image']
        width = p['width']
        height = p['height']

        if asset is not None:
            rawimage = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
            self.image = pygame.transform.smoothscale(rawimage, (width * BLOCK_SIZE, height * BLOCK_SIZE))
        else:
            self.image = None

        self.surfData = SurfData(p['width'], p['height'])
        self.surfData.applySurf(p, 0, 0)

        self.surface = self.surfData.debug_draw_to_surface().convert_alpha()

    @classmethod
    def init(cls):
        with open('patterns.json') as json_data:
            cls.patternDefs = json.load(json_data)

    @classmethod
    def get(cls, patternName):
        if patternName not in cls.pattern:
            cls.pattern[patternName] = LevelObjectPattern(cls.patternDefs[patternName])
        return cls.pattern[patternName]

class LevelObject:
    """
    An object that forms part of the game level.
    Has a position in blocks (x,y), caches related calculated draw position
    Shares data from a LevelObjectPattern.
    """
    def __init__(self, objectDefinition, surfdata=None):
        o = objectDefinition
        self.type = o['type']
        self.pattern  = LevelObjectPattern.get( self.type )
        x = o['x']
        y = o['y']
        self.z_index = o['z']

        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)

        if surfdata is not None:
            surfdata.applySurf(self.pattern.definition, x, y)

    def set_draw_position(self, x, y):
        # Snap to block sizes
        x, y = math.floor(x / BLOCK_SIZE), math.floor(y / BLOCK_SIZE)
        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)

    def draw(self, rq, debug_draw = False):
        if self.pattern.image is not None:
            rq.add(self.draw_position, self.pattern.image, z_index=self.z_index)
        if debug_draw and self.pattern.surface:
            rq.add(self.draw_position, self.pattern.surface, z_index=self.z_index+1)

class LevelEntity:
    """
    An entity that can roam around a level.
    Physics can be done on entities, and they interact with the surfdata.
    """
    def __init__(self, x, y, width, height, asset=None):
        self.top = float(y)
        self.left = float(x)
        self.width = float(width)
        self.height = float(height)
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

        if asset is not None:
            rawimage = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
            self.image = pygame.transform.smoothscale(rawimage, (width * BLOCK_SIZE, height * BLOCK_SIZE))
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

class SpecEcController:
    """
    The player object (SPAREDESK)
    """
    def __init__(self, entity):
        self.le = entity

    def setInputs(self, keys):
        l = self.le
        l.jump  = keys[pygame.K_SPACE]
        l.go_u  = keys[pygame.K_UP]
        l.go_d  = keys[pygame.K_DOWN]
        l.grab  = keys[pygame.K_LSHIFT]
        l.go_l  = keys[pygame.K_LEFT]
        l.go_r  = keys[pygame.K_RIGHT]

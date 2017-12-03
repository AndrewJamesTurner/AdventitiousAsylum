
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
        width = p['width']
        height = p['height']

        if 'image' in p:
            rawimage = pygame.image.load(os.path.join(ASSETS_PATH, p['image'])).convert_alpha()
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

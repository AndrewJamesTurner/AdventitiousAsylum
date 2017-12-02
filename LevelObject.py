
import math
import json

from game import *
from constants import *

class LevelObjectPattern:
    """
    A pattern for a level object.
    Has an image, which is shared by each LevelObject that uses this pattern
    """
    patternDefs = None
    pattern = {}

    def __init__(self, patternDefinition):
        p = patternDefinition
        self.definition = p
        asset = p['image']
        width = p['width']
        height = p['height']

        if asset is not None:
            rawimage = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
            self.image = pygame.transform.smoothscale(rawimage, (width * BLOCK_SIZE, height * BLOCK_SIZE))
        else:
            self.image = None

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
    z_index  = 0
    def __init__(self, objectDefinition, surfdata=None):
        o = objectDefinition
        self.pattern  = LevelObjectPattern.get( o['type'] )
        x = o['x']
        y = o['y']

        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)

        if surfdata is not None:
            surfdata.applySurf(self.pattern.definition, x, y)

    def draw(self, rq):
        if self.pattern.image is not None:
            rq.add(self.draw_position, self.pattern.image, z_index = self.z_index)

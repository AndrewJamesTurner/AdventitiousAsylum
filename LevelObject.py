
import math
import json
import pygame

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

    def set_draw_position(self, x, y):
        # Snap to block sizes
        x, y = math.floor(x / BLOCK_SIZE), math.floor(y / BLOCK_SIZE)
        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)

    def draw(self, rq):
        if self.pattern.image is not None:
            rq.add(self.draw_position, self.pattern.image, z_index = self.z_index)

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
        self.up   = 0
        self.down = 0
        self.jump    = 0
        self.grab    = 0

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

class SpecEcController:
    """
    The player object (SPAREDESK)
    """
    def __init__(self, entity):
        self.le = entity

    def setInputs(self, keys):
        l = self.le
        l.jump  = keys[pygame.K_SPACE]
        l.up    = keys[pygame.K_UP]
        l.down  = keys[pygame.K_DOWN]
        l.grab  = keys[pygame.K_LSHIFT]
        l.vel_x = 5.0 * ((1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0))

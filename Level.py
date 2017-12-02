
import math
import json
import numpy

from game import *
from constants import *
from LevelObject import *
from pygame import Rect, Surface, SRCALPHA

class SurfData:
    """
    Surface data for a level
    """
    TYPE = int
    MASK = {
        'block':  0x1,
        'stand':  0x2,
        'climb':  0x4,
        'damage': 0x8
    }
    SPACECHARS = [' ', '.']

    def __init__(self, width, height):
        self.ary = numpy.zeros((width, height), SurfData.TYPE)

        self.damage_image = Surface(BLOCK_SIZE, BLOCK_SIZE, SRCALPHA)
        self.damage_image.fill((255, 0, 0), Rect(0, 0, 0.3*BLOCK_SIZE, BLOCK_SIZE))

        self.block_image = Surface(BLOCK_SIZE, BLOCK_SIZE, SRCALPHA)
        self.block_image.fill((0, 255, 0))

        self.stand_image = Surface(BLOCK_SIZE, BLOCK_SIZE, SRCALPHA)
        self.stand_image.fill((0, 0, 255), Rect(0, 0, BLOCK_SIZE, 0.3 * BLOCK_SIZE))

        self.climb_image = Surface(BLOCK_SIZE, BLOCK_SIZE, SRCALPHA)
        self.climb_image.fill((255, 0, 255), Rect(0.7*BLOCK_SIZE, 0, 0.3*BLOCK_SIZE, BLOCK_SIZE))

    """
    Apply (merge - OR) surface data from a pattern
    Pattern format:
    {
      "<type>": [ "<linestr>", ... ]
    }
    """
    def applySurf(self, pattern, off_x, off_y):
        for surftype, strings in pattern['surfdata'].items():
            mask = SurfData.MASK[surftype]
            print("Applying surfdata: %s" % surftype)
            for j, s in enumerate(strings):
                for i, c in enumerate(s):
                    x = off_x + i
                    y = off_y + j
                    if c not in SurfData.SPACECHARS:
                        self.ary[x,y] |= mask

    # Debugging
    def printSurf(self):
        width, height = self.ary.shape
        for y in range(0,height):
            chars = ' #^#=#~#*#*#*#*#'
            line = [ self.ary[x, y] for x in range(0,width) ]
            list = [ chars[ int(i) ] for i in line ]
            print( ''.join(list) )

    def debug_draw(self, render_queue):
        for x in range(self.ary.size(1)):
            for y in range(self.ary.size(0)):
                data = self.ary[x, y]
                screen_x = x * BLOCK_SIZE
                screen_y = y * BLOCK_SIZE
                if data & self.MASK['damage']:
                    render_queue.add((screen_x, screen_y), self.damage_image, z_index=20)

                if data & self.MASK['climb']:
                    render_queue.add((screen_x, screen_y), self.climb_image, z_index=20)

                if data & self.MASK['block']:
                    render_queue.add((screen_x, screen_y), self.block_image, z_index=10)

                if data & self.MASK['stand']:
                    render_queue.add((screen_x, screen_y), self.stand_image, z_index=30)


class Level:
    """
    An in-game level
    """
    def __init__(self, levelDefinition):
        l = levelDefinition
        self.width   = l['width']
        self.height  = l['height']
        self.gravity = l['gravity'] * GRAVITY

        # Calculate the player's jump impulse velocity
        # v**2 = u**2 + 2*a*s
        # v = 0 at the top of the jump
        self.jump_v = -math.sqrt( 2 * self.gravity * l['jumpheight'] )

        self.surfdata = SurfData(self.width, self.height)

        self.levelObjects = []
        for obj in l['objects']:
            self.addObject(obj)

    @classmethod
    def load(cls, filename):
        with open(os.path.join(LEVELS_PATH, filename)) as json_data:
            return Level(json.load(json_data))

    def addObject(self, objectDefinition):
        o = LevelObject(objectDefinition, self.surfdata)
        self.levelObjects.append(o)

    def draw(self, rq):
        pass

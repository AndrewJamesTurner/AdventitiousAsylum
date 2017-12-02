
import math
import json
import numpy

from game import *
from constants import *
from LevelObject import *

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

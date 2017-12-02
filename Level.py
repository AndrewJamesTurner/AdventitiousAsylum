
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

    def check(self, mask, x0, y0, x1, y1):
        width, height = self.ary.shape
        for y in range(max(0, int(y0)), min(height, int(y1) + 1)):
            for x in range(max(0, int(x0)), min(width, int(x1) + 1)):
                if (mask & self.ary[x, y]):
                    return True
        return False

class Level:
    """
    An in-game level
    """
    CONTACT_CEILING = -1
    CONTACT_FLOOR   = 1
    CONTACT_LEFT    = -1
    CONTACT_RIGHT   = 1

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
            o = LevelObject(obj, self.surfdata)
            self.addObject(o)
        self.levelEntities = []

    @classmethod
    def load(cls, filename):
        with open(os.path.join(LEVELS_PATH, filename)) as json_data:
            return Level(json.load(json_data))

    def addObject(self, lObject):
        self.levelObjects.append(lObject)

    def addEntity(self, lEntity):
        self.levelEntities.append(lEntity)

    def dropEntity(self, lEntity):
        self.levelEntities.remove(lEntity)

    # Update all of the entities
    def update(self, dt):
        for le in self.levelEntities:
            # Apply inputs
            print("J%d vC%d" % (le.jump, le.vcontact))
            if le.jump and le.vcontact == Level.CONTACT_FLOOR:
                le.vel_y = self.jump_v

            # Gravity
            le.vel_y += (self.gravity * dt)

            # Calculate delta movement
            dx = le.vel_x * dt
            dy = le.vel_y * dt

            # Do H movement
            if dx != 0:
                xp = dx + (le.right if (dx > 0) else le.left)
                if self.surfdata.check(0x1, xp, math.floor(le.top), xp, math.ceil(le.bottom) - 1):
                    le.vel_x = 0.0
                    le.hcontact = Level.CONTACT_RIGHT if (dx > 0) else Level.CONTACT_LEFT
                else:
                    le.move(dx, 0)
                    le.hcontact = 0

            # Do V movement
            if dy != 0:
                yp = dy + (le.bottom if (dy > 0) else le.top)
                surfmask = 0x1
                if dy > 0 and not le.dropoff:
                    surfmask = 0x3

                if self.surfdata.check(surfmask, math.floor(le.left), yp, math.ceil(le.right) - 1, yp):
                    le.vel_y = 0.0
                    le.vcontact = Level.CONTACT_FLOOR if (dy > 0) else Level.CONTACT_CEILING
                else:
                    le.move(0, dy)
                    le.vcontact = 0

    def draw(self, rq):
        for lo in self.levelObjects:
            lo.draw(rq)
        for le in self.levelEntities:
            le.draw(rq)

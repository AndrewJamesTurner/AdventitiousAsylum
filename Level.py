
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

        self.damage_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        self.damage_image.fill((255, 0, 0), Rect(0, 0, 0.3*BLOCK_SIZE, BLOCK_SIZE))

        self.block_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        self.block_image.fill((0, 255, 0))

        self.stand_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        self.stand_image.fill((0, 0, 255), Rect(0, 0, BLOCK_SIZE, 0.3 * BLOCK_SIZE))

        self.climb_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
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
        for x in range(self.ary.shape[0]):
            for y in range(self.ary.shape[1]):
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

    def check(self, mask, x0, y0, x1, y1):
        print("Check for %x in %d,%d : %d,%d" % (mask, x0, y0, x1, y1))
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
        CLIMBABLE = SurfData.MASK['climb']

        for le in self.levelEntities:
            # Apply inputs
            if le.jump and le.vcontact == Level.CONTACT_FLOOR:
                le.vel_y = self.jump_v

            # Gravity
            if le.grab and self.surfdata.check(CLIMBABLE,
                                    math.floor(le.left),
                                    math.floor(le.top),
                                    math.ceil(le.right) - 1,
                                    math.ceil(le.bottom) - 1):
                le.vel_y = 5.0 * ((1 if le.down else 0) - (1 if le.up else 0))
            else:
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
                if(dy > 0):
                    yc = le.bottom
                    yp = yc + dy
                    transition = ( 1 if math.ceil(yc) == math.floor(yp) else 0 )
                else:
                    yc = le.bottom
                    yp = yc + dy
                    transition = ( 1 if math.floor(yc) == math.ceil(yp) else 0 )

                move = 1
                if transition:
                    surfmask = ( 0x3 if (dy > 0) and not le.down else 0x1 )
                    if self.surfdata.check(surfmask, math.floor(le.left), yp, math.ceil(le.right) - 1, yp):
                        move = 0
                if move:
                    le.move(0, dy)
                    le.vcontact = 0
                else:
                    le.vel_y = 0.0
                    le.vcontact = Level.CONTACT_FLOOR if (dy > 0) else Level.CONTACT_CEILING

    def draw(self, rq):
        for lo in self.levelObjects:
            lo.draw(rq)
        for le in self.levelEntities:
            le.draw(rq)

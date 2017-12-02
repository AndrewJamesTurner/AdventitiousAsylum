
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

    images_initialised = False

    @classmethod
    def load_debug_surfaces(cls):
        cls.damage_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        cls.damage_image.fill((255, 0, 0), Rect(0, 0, 0.3 * BLOCK_SIZE, BLOCK_SIZE))

        cls.block_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        cls.block_image.fill((0, 255, 0))

        cls.stand_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        cls.stand_image.fill((0, 0, 255), Rect(0, 0, BLOCK_SIZE, 0.3 * BLOCK_SIZE))

        cls.climb_image = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        cls.climb_image.fill((255, 0, 255), Rect(0.7 * BLOCK_SIZE, 0, 0.3 * BLOCK_SIZE, BLOCK_SIZE))

    def __init__(self, width, height):
        self.ary = numpy.zeros((width, height), SurfData.TYPE)

        if not SurfData.images_initialised:
            SurfData.load_debug_surfaces()

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

    def debug_draw_to_surface(self):
        surface = Surface((self.ary.shape[0]*BLOCK_SIZE, self.ary.shape[1]*BLOCK_SIZE), SRCALPHA)
        for x in range(self.ary.shape[0]):
            for y in range(self.ary.shape[1]):
                data = self.ary[x, y]
                screen_x = x * BLOCK_SIZE
                screen_y = y * BLOCK_SIZE

                if data & self.MASK['block']:
                    surface.blit(SurfData.block_image, (screen_x, screen_y))

                if data & self.MASK['damage']:
                    surface.blit(SurfData.damage_image, (screen_x, screen_y))

                if data & self.MASK['climb']:
                    surface.blit(SurfData.climb_image, (screen_x, screen_y))

                if data & self.MASK['stand']:
                    surface.blit(SurfData.stand_image, (screen_x, screen_y))
        return surface

    def check(self, mask, x0, y0, x1, y1):
        #print("Check for %x in %d,%d : %d,%d" % (mask, x0, y0, x1, y1))
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
        self.playerspeed = l['playerspeed']

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

    def collides(self, e1, e2):
        if e1 is e2:
            return False
        xcollide = not ( e1.left > e2.right  or e2.left > e1.right  )
        ycollide = not ( e1.top  > e2.bottom or e2.top  > e1.bottom )
        return (xcollide and ycollide)

    def collidingEntities(self, entity):
        return [ e for e in self.levelEntities if self.collides(entity, e) ]

    # Update all of the entities
    def update(self, dt):
        for le in self.levelEntities:
            # Apply inputs
            if le.vcontact == Level.CONTACT_FLOOR:
                if le.jump:
                    le.vel_y = self.jump_v
                speedtarget = 0.0
                if le.go_r:
                    speedtarget += self.playerspeed
                if le.go_l:
                    speedtarget -= self.playerspeed
                speeddiff = speedtarget - le.vel_x
                if abs(speeddiff) < PLAYER_ACCEL:
                    le.vel_x = speedtarget
                else:
                    le.vel_x += numpy.sign(speeddiff) * PLAYER_ACCEL
            else:
                if le.jump and le.hcontact != 0:
                    le.vel_y = 0.5 * self.jump_v
                    le.vel_x = self.jump_v * le.hcontact

            # Gravity
            if le.grab and self.surfdata.check(SurfData.MASK['climb'],
                                    math.floor(le.left),
                                    math.floor(le.top),
                                    math.ceil(le.right) - 1,
                                    math.ceil(le.bottom) - 1):
                le.vel_y = 5.0 * ((1 if le.go_d else 0) - (1 if le.go_u else 0))
            else:
                le.vel_y += (self.gravity * dt)

            # Calculate delta movement
            dx = le.vel_x * dt
            dy = le.vel_y * dt

            # Do H movement
            if dx != 0:
                if(dx > 0):
                    xc = le.right
                    xp = xc + dx
                    transition = ( 1 if math.ceil(xc) == math.floor(xp) else 0 )
                else:
                    xc = le.left
                    xp = xc + dx
                    transition = ( 1 if math.floor(xc) == math.ceil(xp) else 0 )

                move = 1
                if transition:
                    if self.surfdata.check(SurfData.MASK['block'],
                                            xp, math.floor(le.top),
                                            xp, math.ceil(le.bottom) - 1):
                        move = 0

                if move:
                    le.move(dx, 0)
                    le.hcontact = 0
                else:
                    le.vel_x = 0.0
                    le.hcontact = Level.CONTACT_RIGHT if (dx > 0) else Level.CONTACT_LEFT

            # Do V movement
            if dy != 0:
                if(dy > 0):
                    yc = le.bottom
                    yp = yc + dy
                    transition = ( 1 if math.ceil(yc) == math.floor(yp) else 0 )
                else:
                    yc = le.top
                    yp = yc + dy
                    transition = ( 1 if math.floor(yc) == math.ceil(yp) else 0 )

                move = 1
                if transition:
                    surfmask = SurfData.MASK['block']
                    if (dy > 0) and not le.go_d:
                        surfmask |= SurfData.MASK['stand']
                    surfmask |= ( 0x3 if (dy > 0) and not le.go_d else 0x1 )
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

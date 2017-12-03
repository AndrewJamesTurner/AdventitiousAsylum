
import math
import json
import numpy
import random

from game import *
from sharedValues import get_shared_values
from constants import *
from LevelObject import *
from SurfData import *
from LevelEntity import *

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
        self.jump_v = -math.sqrt( 2 * self.gravity * l['jumpheight'] / BLOCKS_PER_M )

        self.surfdata = SurfData(self.width, self.height)

        if 'objects' in l:
            self.levelObjects = [ LevelObject(o, self.surfdata) for o in l['objects'] ]
        else:
            print("Warning: Level has no objects")
            self.levelObjects = []
        if 'spawners' in l:
            self.spawners = [ Spawner(s, self) for s in l['spawners'] ]
        else:
            print("Warning: Level has no spawners")
            self.spawners = []
        self.levelEntities = []

        for s in [ s for s in self.spawners if s.type in ['oneshot'] ]:
            s.update(0)

    def getSpedEcEntity(self):
        return [ e for e in self.levelEntities if e.archetype == 'player' ][0]

    @classmethod
    def load(cls, filename):
        with open(os.path.join(LEVELS_PATH, filename)) as json_data:
            return Level(json.load(json_data))

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

    def setScreenRect(self, l, t, r, b):
        l -= SCREEN_MARGIN
        t -= SCREEN_MARGIN
        r += SCREEN_MARGIN
        b += SCREEN_MARGIN
        # Rly?
        self.screenEntity = LevelEntity(l, t, 'screen', {'name':'screen','width':(r-l),'height':(b-t)}, scale=1.0)

    def isOffscreen(self, entity):
        return not self.collides(self.screenEntity, entity)

    def screenRelative(self, x, y):
        sx = (x - self.screenEntity.centre) / (self.screenEntity.width  / 2)
        sy = (y - self.screenEntity.middle) / (self.screenEntity.height / 2)
        #print("(%f,%f) --[%f,%f:%f,%f]-> (%f,%f)" % (x,y,self.screenEntity.left,self.screenEntity.top,self.screenEntity.right,self.screenEntity.bottom,sx,sy))
        return (sx, sy)

    # Update all of the entities
    def update(self, dt):
        for s in self.spawners:
            s.update(dt)

        see = self.getSpedEcEntity()

        for le in self.levelEntities:
            # Apply inputs
            if le.vcontact == Level.CONTACT_FLOOR:
                accel = PLAYER_ACCEL
                decel = PLAYER_DECEL
                if le.jump:
                    le.vel_y = self.jump_v
            else:
                accel = PLAYER_ACCEL_AIR
                decel = accel
                if le.jump and le.hcontact != 0:
                    le.vel_y = 0.5 * self.jump_v
                    le.vel_x = self.jump_v * le.hcontact

            speedtarget = 0.0
            if le.go_r:
                speedtarget += self.playerspeed
            if le.go_l:
                speedtarget -= self.playerspeed
            sign_x = numpy.sign(le.vel_x)
            if numpy.sign(speedtarget) != sign_x and sign_x != 0:
                accel = decel
            speeddiff = speedtarget - le.vel_x
            if abs(speeddiff) < accel:
                le.vel_x = speedtarget
            else:
                le.vel_x += numpy.sign(speeddiff) * accel

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
            vx = le.vel_x * BLOCKS_PER_M
            vy = le.vel_y * BLOCKS_PER_M
            dx = vx * dt
            dy = vy * dt

            # Check which gridlines will be crossed
            def findCrossingParams(edge0, edge1, ds, axis):
                if ds == 0:
                    return []
                else:
                    offset = 0 if ds > 0 else -1
                    if ds > 0:
                        s0 = edge1
                        sr = range(math.ceil(s0), math.ceil(s0 + ds))
                    else:
                        s0 = edge0
                        sr = range(math.floor(s0 + ds) + 1, math.floor(s0) + 1)
                    return [ ((s - s0) / ds, s + offset, axis) for s in sr ]
            dtx = findCrossingParams(le.left, le.right, dx, 0)
            dty = findCrossingParams(le.top, le.bottom, dy, 1)

            dps = sorted(dtx + dty, key=lambda e: e[0])

            stop = [0, 0]
            # phys_margin = 0.2
            # xmarg = numpy.sign(dx) * phys_margin
            # ymarg = numpy.sign(dy) * phys_margin
            # le.move(-xmarg, -ymarg)
            pp = 0.0
            for p,s,axis in dps:
                dp = p - pp
                pp = p
                le.move(dp * dx, dp * dy)
                if stop[axis]:
                    continue
                if axis == 0:
                    if self.surfdata.check(SurfData.MASK['block'],
                                            s, math.floor(le.top),
                                            s, math.ceil(le.bottom) - 1):
                        stop[0] = 1
                        le.hcontact = Level.CONTACT_RIGHT if (dx > 0) else Level.CONTACT_LEFT
                        dx = 0
                    else:
                        le.hcontact = 0
                if axis == 1:
                    surfmask = SurfData.MASK['block']
                    if (dy > 0) and not le.go_d:
                        surfmask |= SurfData.MASK['stand']
                    if self.surfdata.check(surfmask,
                                            math.floor(le.left), s,
                                            math.ceil(le.right) - 1, s):
                        stop[1] = 1
                        le.vcontact = Level.CONTACT_FLOOR if (dy > 0) else Level.CONTACT_CEILING
                        dy = 0
                    else:
                        le.vcontact = 0
            # Do the remaining movement
            dp = 1.0 - pp
            le.move(dp * dx, dp * dy)

            # le.move(xmarg, ymarg)

            if stop[0]:
                le.vel_x = 0.0
            if stop[1]:
                le.vel_y = 0.0

            # Do offscreen checks and cull from the level
            if self.isOffscreen(le):
                le.offscreen = 1
                if le.archetype not in ['health','weapon']:
                    self.dropEntity(le)

    def draw(self, rq):
        for lo in self.levelObjects:
            lo.draw(rq)
        for le in self.levelEntities:
            le.draw(rq)

class Spawner:
    """
    Something that spawns entities
    """
    @classmethod
    def init(cls):
        with open('entities.json') as json_data:
            cls.entities = json.load(json_data)

    @classmethod
    def setPlayerEntity(cls, pe):
        cls.playerentity = pe

    def __init__(self, spawnerDefinition, level):
        s = spawnerDefinition
        self.level = level
        self.x = s['x']
        self.y = s['y']
        self.type = s['spawnertype']
        self.rate = s['rate']
        self.entitytype = s['entitytype']
        if 'filter' in s and s['filter'] != '':
            self.filter = s['filter']
        else:
            self.filter = None
        self.timer = 0

    def setTimer(self, r):
        # TODO: Use r to randomize
        self.timer = 1.0 / self.rate

    def update(self, dt):
        if self.active():
            self.timer -= dt
            if(self.timer <= 0):
                self.setTimer(0)
                self.spawn()

    def active(self):
        if self.type == 'oneshot':
            status = (self.rate != -1)
            self.timer = -1
            self.rate  = -1
            return status
        else:
            sx, sy = self.level.screenRelative(self.x + 0.5, self.y + 0.5)
            if   self.type == 'goleft':
                return (sx > 0.5 and sy > -2.0 and sy < 2.0)
            elif self.type == 'goright':
                return (sx < -0.5 and sy > -2.0 and sy < 2.0)
        return False

    def spawn(self):
        if self.entitytype not in Spawner.entities:
            print("Can't spawn entitytype '%s'" % self.entitytype)
            return

        edefs = Spawner.entities[self.entitytype]
        if self.filter is not None:
            edefs = [ e for e in edefs if 'filter' in e and e['filter'] == self.filter ]

        if self.entitytype == 'player':
            entitydata = [ d for d in edefs if d['name'] == get_shared_values().player.name ][0]
        else:
            entitydata = random.choice(edefs)
        width  = entitydata['width']
        height = entitydata['height']
        # Spawn above the bottom of the current block
        b = self.y + 0.99
        m = self.x + 0.5
        x = m - width  / 2.0
        y = b - height
        entity     = LevelEntity(x, y, self.entitytype, entitydata)
        # TODO: Assign a proper controller
        if self.type == 'goright':
            entity.go_r = 1
        elif self.type == 'goleft':
            entity.go_l = 1

        self.level.addEntity(entity)

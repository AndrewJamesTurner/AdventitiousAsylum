
import math
import json
import numpy
import random

from game import *
from constants import *
from LevelObject import *
from SurfData import *

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

        if 'objects' in l:
            self.levelObjects = [ LevelObject(o, self.surfdata) for o in l['objects'] ]
        else:
            print("Warning: Level has no objects")
            self.levelObjects = []
        if 'spawners' in l:
            print("Warning: Level has no spawners")
            self.spawners = [ Spawner(s, self) for s in l['spawners'] ]
        else:
            self.spawners = []
        self.levelEntities = []

        for s in [ s for s in self.spawners if s.type in ['player','oneshot'] ]:
            e = s.update(0)
            if(s.type == 'player'):
                self.playerentity = e

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

    # Update all of the entities
    def update(self, dt):
        for s in self.spawners:
            s.update(dt)

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
        self.timer = 0

    def setTimer(self, r):
        # TODO: Use r to randomize
        self.timer = 1.0 / self.rate

    def update(self, dt):
        if self.active():
            self.timer -= dt
            if(self.timer <= 0):
                self.setTimer(0)
                return self.spawn()

    def active(self):
        if self.type in ['goright','goleft']:
            if abs(Spawner.playerentity.centre - (self.x + 0.5)) > 20:
                return False
            if abs(Spawner.playerentity.middle - (self.y + 0.5)) > 30:
                return False
        elif self.type in ['oneshot','player']:
            status = (self.rate != -1)
            self.rate = -1
            return status
        return True

    def spawn(self):
        edefs = Spawner.entities[self.entitytype]
        if self.type == 'player':
            entitydata = [ d for d in edefs if d['name'] == SharedValues.spedecentity ][0]
        else:
            entitydata = random.choice(edefs)
        width  = entitydata['width']
        height = entitydata['height']
        # Spawn above the bottom of the current block
        b = self.y + 0.99
        m = self.x + 0.5
        x = m - width  / 2.0
        y = b - height
        entity     = LevelEntity(x, y, width, height, entitydata['image'])
        # TODO: Assign a proper controller
        if self.type == 'goright':
            entity.go_r = 1
        elif self.type == 'goleft':
            entity.go_l = 1

        self.level.addEntity(entity)
        return entity

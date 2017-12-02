
import math
import json

from game import *
from constants import *
from numpy import *

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

    def __init__(self, width, height):
        self.ary numpy.zeros((width, height), SurfData.TYPE)

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
            #TODO

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
        self.jump_v = -sqrt( 2 * self.gravity * l['jumpheight'] )

        self.surfdata = SurfData.new(self.width, self.height)

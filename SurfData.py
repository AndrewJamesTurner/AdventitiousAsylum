import numpy
from constants import *
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

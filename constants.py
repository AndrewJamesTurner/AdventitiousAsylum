# Window size, in pixels
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Width and height, in pixels, of a block in the level
BLOCK_SIZE = 32

# Default gravity
GRAVITY = 20.0

# Pixels per meter, converting between box2d world and pygame screen
PPM = 20.0

# Frames per second, for rendering and physics
FPS = 60

# Conversion between ezpygame dt and box2d dt
DT_SCALE = 0.001

# Box2d iteration parameters
VELOCITY_ITERATIONS = 10
POSITION_ITERATIONS = 10


MAX_FUEL = 5000
MAX_HEALTH = 100
MAX_OXYGEN = 1000

# Number of box2d metres for every unit in our shape definition units
SHAPE_UNITS_TO_METRES = 20

# Pygame colour
black = 0, 0, 0, 0
white = 255, 255, 255, 0
red = 255, 0, 0, 0
yellow = 255, 255, 0, 0
grey = 160, 160, 160, 0
green = 0, 255, 0, 0

PLAYER_ACCEL = 0.2
PLAYER_DECEL = 1.0
PLAYER_ACCEL_AIR = 0.1

ASSETS_PATH = 'assets'
LEVELS_PATH = 'levels'

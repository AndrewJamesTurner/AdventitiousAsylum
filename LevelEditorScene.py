
import thorpy
import json
import itertools
from game import *
from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *


DETAILS_AREA_WIDTH = 250
PATTERNS_AREA_WIDTH = 250
SPAWNERS_AREA_WIDTH = 250


class Spawner:
    """
    A representation of spawners that draws an image to the screen - for the level editor.
    """

    def __init__(self, x, y, entity_type, spawner_type, rate):
        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)
        self.entity_type = entity_type
        self.spawner_type = spawner_type
        self.rate = rate
        width = 1
        height = 1
        asset = 'spawn.png'
        rawimage = pygame.image.load(os.path.join(ASSETS_PATH, asset)).convert_alpha()
        self.image = pygame.transform.smoothscale(rawimage, (width * BLOCK_SIZE, height * BLOCK_SIZE))

    def set_draw_position(self, x, y):
        # Snap to block sizes
        x, y = math.floor(x / BLOCK_SIZE), math.floor(y / BLOCK_SIZE)
        self.block_position = (x, y)
        self.draw_position = (x * BLOCK_SIZE, y * BLOCK_SIZE)

    def draw(self, rq):
        rq.add(self.draw_position, self.image, z_index=99)


class LevelEditor(GameScene):

    def __init__(self):
        self.level_objects = []
        self.spawner_objects = []
        self.render_queue = RenderQueue()
        self.dragging_object = None
        self.dragging_spawner = None
        self.selected_object = None
        self.selected_spawner = None
        self.drag_offset = None
        self.zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0

        # Game area
        self.game_area = thorpy.Box.make([], size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_area.set_main_color((220, 255, 220, 0))
        # TODO: Add horizontal and vertical scroller to game area

        # Level details area
        self.level_details_title = thorpy.make_text('Level Details', 18, (0, 0, 0))
        self.level_name_box = thorpy.Inserter.make(name='Name: ', value='new_level')
        load_level_button = thorpy.make_button('Load level', self.load_level)
        self.level_width_box = thorpy.Inserter.make(name='Width: ', value='')
        self.level_height_box = thorpy.Inserter.make(name='Height: ', value='')
        self.gravity_box = thorpy.Inserter.make(name='Gravity: ', value='')
        self.jump_height_box = thorpy.Inserter.make(name='Jump height: ', value='')
        self.player_speed_box = thorpy.Inserter.make(name='Player speed: ', value='')
        save_level_button = thorpy.make_button('Save level', self.save_level)
        self.level_details_area = thorpy.Box.make([self.level_details_title, self.level_name_box, load_level_button, self.level_width_box, self.level_height_box, self.gravity_box, self.jump_height_box, self.player_speed_box, save_level_button])
        self.level_details_area.fit_children()

        # Pattern details area
        pattern_details_title = thorpy.make_text('Pattern Details', 18, (0, 0, 0))
        self.pattern_id_box = thorpy.Inserter.make(name='ID: ', value='')
        self.image_file_box = thorpy.Inserter.make(name='Image file: ', value='')
        self.pattern_width_box = thorpy.Inserter.make(name='Width: ', value='')
        self.pattern_height_box = thorpy.Inserter.make(name='Height: ', value='')
        self.block_data_box = thorpy.Inserter.make(name='Block data: ', value='')
        self.stand_data_box = thorpy.Inserter.make(name='Stand data: ', value='')
        self.climb_data_box = thorpy.Inserter.make(name='Climb data: ', value='')
        self.damage_data_box = thorpy.Inserter.make(name='Damage data: ', value='')
        self.pattern_details_area = thorpy.Box.make([pattern_details_title, self.pattern_id_box, self.image_file_box, self.pattern_width_box, self.pattern_height_box, self.block_data_box, self.stand_data_box, self.climb_data_box, self.damage_data_box])

        # Object details area
        object_details_title = thorpy.make_text('Object Details', 18, (0, 0, 0))
        self.top_box = thorpy.Inserter.make(name='Top: ', value='')
        self.left_box = thorpy.Inserter.make(name='Left: ', value='')
        self.z_box = thorpy.Inserter.make(name='Z index: ', value='')
        self.object_details_area = thorpy.Box.make([object_details_title, self.top_box, self.left_box, self.z_box])

        def change_z_index(event):
            self.selected_object.z_index = str_to_int(event.value)
        z_index_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT, reac_func=change_z_index,
                                               event_args={'id': thorpy.constants.EVENT_INSERT, 'el': self.z_box})
        self.z_box.add_reaction(z_index_reaction)

        self.details_area = thorpy.Box.make([self.level_details_area, self.pattern_details_area, self.object_details_area],
                                            size=(DETAILS_AREA_WIDTH, SCREEN_HEIGHT))
        self.details_area.set_main_color((255, 220, 255, 180))
        self.details_area.set_topleft((SCREEN_WIDTH, 0))

        self.debug_draw = False

        # Patterns area
        patterns_title = thorpy.make_text('Patterns', 18, (0, 0, 0))

        def click_pattern(pattern_id, surfdata):
            position = self.backwardMouseTransform((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            level_object = LevelObject(objectDefinition={
                'type': pattern_id,
                'x': math.floor(position[0] / BLOCK_SIZE),
                'y': math.floor(position[1] / BLOCK_SIZE),
                'z': 0,
            })  # TODO: Do we need to pass in surf data here?
            self.level_objects.append(level_object)

        # Load the already-created patterns
        patterns = []
        pattern_objects = []
        LevelObjectPattern.init()
        with open('patterns.json', 'r') as patterns_file:
            patterns_descriptions = json.load(patterns_file)

        patterns_temp = list(patterns_descriptions.items())
        patterns_temp.sort(key=lambda x: x[0])

        for pattern_id, pattern_definition in patterns_temp:
            pattern = LevelObjectPattern(pattern_definition, pattern_id)
            patterns.append(pattern)
            # TODO: Add a small version of the image to this object
            pattern_object = thorpy.make_button(pattern_id, func=click_pattern, params={'pattern_id': pattern_id, 'surfdata': pattern_definition['surfdata']})
            pattern_objects.append(pattern_object)

        self.patterns_area = thorpy.Box.make([patterns_title, *pattern_objects], size=(PATTERNS_AREA_WIDTH, SCREEN_HEIGHT))
        self.patterns_area.set_main_color((220, 220, 255, 180))
        self.patterns_area.set_topleft((SCREEN_WIDTH + DETAILS_AREA_WIDTH, 0))
        thorpy.store(self.patterns_area, y=0)
        self.patterns_area.refresh_lift()

        # Spawners area
        def click_add_spawner():
            position = self.backwardMouseTransform((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            spawner_object = Spawner(
                x=math.floor(position[0] / BLOCK_SIZE),
                y=math.floor(position[1] / BLOCK_SIZE),
                entity_type='',
                spawner_type='',
                rate=0.3,
            )
            self.spawner_objects.append(spawner_object)

        spawners_title = thorpy.make_text('Spawners', 18, (0, 0, 0))
        add_spawner_button = thorpy.make_button('Add spawner', func=click_add_spawner, params={})

        # Spawner details area
        spawner_details_title = thorpy.make_text('Spawner Details', 18, (0, 0, 0))
        self.spawner_x_box = thorpy.Inserter.make(name='X: ', value='')
        self.spawner_y_box = thorpy.Inserter.make(name='Y: ', value='')
        self.spawner_entity_type_box = thorpy.Inserter.make(name='Entity type: ', value='')
        self.spawner_spawner_type_box = thorpy.Inserter.make(name='Spawner type: ', value='')
        self.spawner_rate_box = thorpy.Inserter.make(name='Rate: ', value='')

        def change_spawner_entity_type(event):
            self.selected_spawner.entity_type = event.value
        def change_spawner_spawner_type(event):
            self.selected_spawner.spawner_type = event.value
        def change_spawner_rate(event):
            self.selected_spawner.rate = str_to_float(event.value)
        entity_type_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                               reac_func=change_spawner_entity_type,
                                               event_args={'id': thorpy.constants.EVENT_INSERT, 'el': self.spawner_entity_type_box})
        spawner_type_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                               reac_func=change_spawner_spawner_type,
                                               event_args={'id': thorpy.constants.EVENT_INSERT, 'el': self.spawner_spawner_type_box})
        rate_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                               reac_func=change_spawner_rate,
                                               event_args={'id': thorpy.constants.EVENT_INSERT,
                                                           'el': self.spawner_rate_box})
        self.spawner_entity_type_box.add_reaction(entity_type_reaction)
        self.spawner_spawner_type_box.add_reaction(spawner_type_reaction)
        self.spawner_rate_box.add_reaction(rate_reaction)

        spawner_details_area = thorpy.Box.make(
            [spawner_details_title, self.spawner_x_box, self.spawner_y_box, self.spawner_entity_type_box,
             self.spawner_spawner_type_box, self.spawner_rate_box, ])

        self.spawners_area = thorpy.Box.make([spawners_title, add_spawner_button, spawner_details_area], size=(SPAWNERS_AREA_WIDTH, SCREEN_HEIGHT))
        self.spawners_area.set_main_color((255, 255, 220, 180))
        self.spawners_area.set_topleft((SCREEN_WIDTH + DETAILS_AREA_WIDTH + PATTERNS_AREA_WIDTH, 0))
        thorpy.store(self.spawners_area, gap=30)

        self.menu = thorpy.Menu([self.game_area, self.patterns_area, self.details_area, self.spawners_area])

    def load_level(self):
        file_name = self.level_name_box.get_value()
        if not file_name.endswith('.json'):
            file_name += '.json'
        with open(os.path.join('levels', file_name), 'r') as level_file:
            level_info = json.load(level_file)
        self.level_width_box.set_value(str(level_info['width']))
        self.level_height_box.set_value(str(level_info['height']))
        self.gravity_box.set_value(str(level_info['gravity']))
        self.jump_height_box.set_value(str(level_info['jumpheight']))
        self.player_speed_box.set_value(str(level_info['playerspeed']))
        self.level_objects = []
        for level_object_info in level_info['objects']:
            self.level_objects.append(LevelObject(objectDefinition=level_object_info))
        if 'spawners' in level_info:
            for spawner_info in level_info['spawners']:
                self.spawner_objects.append(Spawner(x=spawner_info['x'], y=spawner_info['y'],
                                                    entity_type=spawner_info['entitytype'],
                                                    spawner_type=spawner_info['spawnertype'],
                                                    rate=spawner_info['rate']))

    def save_level(self):
        # Move objects to positive positions
        min_x = min(level_object.block_position[0] for level_object in self.level_objects)
        max_x = max(level_object.block_position[0] + level_object.pattern.definition['width'] for level_object in self.level_objects)
        min_y = min(level_object.block_position[1] for level_object in self.level_objects)
        max_y = max(level_object.block_position[1] + level_object.pattern.definition['height'] for level_object in self.level_objects)

        # Collect level details
        level = {
            'width': max_x - min_x,
            'height': max_y - min_y,
            'gravity': str_to_float(self.gravity_box.get_value()),
            'jumpheight': str_to_float(self.jump_height_box.get_value()),
            'playerspeed': str_to_float(self.player_speed_box.get_value()),
            'objects': [],
            'spawners': [],
        }
        # Collect objects
        for level_object in self.level_objects:
            level['objects'].append({
                'type': level_object.type,
                'x': level_object.block_position[0] - min_x,
                'y': level_object.block_position[1] - min_y,
                'z': level_object.z_index,
            })
        # Collect spawners
        for spawner in self.spawner_objects:
            level['spawners'].append({
                'x': spawner.block_position[0] - min_x,
                'y': spawner.block_position[1] - min_y,
                'entitytype': spawner.entity_type,
                'spawnertype': spawner.spawner_type,
                'rate': spawner.rate,
            })

        # Write file
        file_name = self.level_name_box.get_value()
        if not file_name.endswith('.json'):
            file_name += '.json'
        with open(os.path.join('levels', file_name), 'w') as file:
            json.dump(level, file, indent=2)

    def draw(self, screen):
        for level_object in self.level_objects:
            level_object.draw(self.render_queue, self.debug_draw)
        for spawner_object in self.spawner_objects:
            spawner_object.draw(self.render_queue)
        self.render_queue.flush(screen, scale=(self.zoom, self.zoom), camera_position=(self.camera_x, self.camera_y))

        for element in [self.game_area, self.patterns_area, self.details_area, self.spawners_area]:
            element.blit()

    def update(self, dt):
        for element in [self.game_area, self.patterns_area, self.details_area, self.spawners_area]:
            element.update()

    def backwardMouseTransform(self, pos):
        x, y = pos
        x /= self.zoom
        y /= self.zoom
        x += self.camera_x
        y += self.camera_y
        return(x, y)

    def handle_event(self, event):
        self.menu.react(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = self.backwardMouseTransform(event.pos)
            # See if we are clicking on a game element
            for level_object in sorted(self.level_objects, key=lambda lo: lo.z_index):
                if level_object.draw_position[0] < mouse_x < level_object.draw_position[0] + level_object.pattern.image.get_width() \
                        and level_object.draw_position[1] < mouse_y < level_object.draw_position[1] + level_object.pattern.image.get_height():
                    if event.button == 1:
                        # Drag element
                        self.dragging_object = level_object
                        self.selected_object = level_object
                        self.drag_offset = (level_object.draw_position[0] - mouse_x,
                                            level_object.draw_position[1] - mouse_y)
                        self.update_object_details_area(level_object)
                    elif event.button == 3:
                        # Delete element
                        self.level_objects.remove(level_object)
            for spawner_object in self.spawner_objects:
                if spawner_object.draw_position[0] < mouse_x < spawner_object.draw_position[0] + spawner_object.image.get_width() \
                        and spawner_object.draw_position[1] < mouse_y < spawner_object.draw_position[1] + spawner_object.image.get_height():
                    # Replace selected level object with spawner object
                    self.dragging_object = None
                    self.drag_offset = None
                    if event.button == 1:
                        # Drag spawner
                        self.dragging_spawner = spawner_object
                        self.selected_spawner = spawner_object
                        self.drag_offset = (spawner_object.draw_position[0] - mouse_x,
                                            spawner_object.draw_position[1] - mouse_y)
                        self.update_spawner_details_area(spawner_object)
                    elif event.button == 3:
                        # Delete spawner
                        self.spawner_objects.remove(spawner_object)
            if event.button == 4:
                self.doZoom(1.25, *event.pos)
            elif event.button == 5:
                self.doZoom(0.8, *event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.update_object_details_area(self.selected_object)
                self.dragging_object = None
                self.dragging_spawner = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_object is not None:
                mouse_x, mouse_y = self.backwardMouseTransform(event.pos)
                self.dragging_object.set_draw_position(mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1])
            elif self.dragging_spawner is not None:
                mouse_x, mouse_y = self.backwardMouseTransform(event.pos)
                self.dragging_spawner.set_draw_position(mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1])

        elif event.type == pygame.KEYDOWN:
            nudge_size = BLOCK_SIZE * 5 / self.zoom
            if event.key == pygame.K_LEFT:
                self.camera_x -= nudge_size
            elif event.key == pygame.K_RIGHT:
                self.camera_x += nudge_size
            if event.key == pygame.K_UP:
                self.camera_y -= nudge_size
            elif event.key == pygame.K_DOWN:
                self.camera_y += nudge_size
            if event.key == pygame.K_d:
                self.debug_draw = not self.debug_draw

        elif event.type == pygame.QUIT:
            pygame.quit()

    def doZoom(self, factor, cx, cy):
        def nastyZoomTransform(z1, z2, m, c1):
            c2 = (m / z1) - (m / z2) + c1
            return c2
        z1 = self.zoom
        self.zoom *= factor
        z2 = self.zoom
        self.camera_x = nastyZoomTransform(z1, z2, cx, self.camera_x)
        self.camera_y = nastyZoomTransform(z1, z2, cy, self.camera_y)

    def update_object_details_area(self, level_object):
        if level_object is None:
            self.top_box.set_value('')
            self.left_box.set_value('')
            self.z_box.set_value('')
        else:
            self.top_box.set_value(str(level_object.block_position[1]))
            self.left_box.set_value(str(level_object.block_position[0]))
            self.z_box.set_value(str(level_object.z_index))

            self.pattern_id_box.set_value(level_object.type)
            self.image_file_box.set_value(level_object.pattern.definition['image'])
            self.pattern_width_box.set_value(str(level_object.pattern.definition['width']))
            self.pattern_height_box.set_value(str(level_object.pattern.definition['height']))
            self.block_data_box.set_value('')
            self.stand_data_box.set_value('')
            self.climb_data_box.set_value('')
            self.damage_data_box.set_value('')

    def update_spawner_details_area(self, spawner_object):
        if spawner_object is None:
            self.spawner_x_box.set_value('')
            self.spawner_y_box.set_value('')
            self.spawner_entity_type_box.set_value('')
            self.spawner_spawner_type_box.set_value('')
            self.spawner_rate_box.set_value('')
        else:
            self.spawner_x_box.set_value(str(spawner_object.block_position[0]))
            self.spawner_y_box.set_value(str(spawner_object.block_position[1]))
            self.spawner_entity_type_box.set_value(spawner_object.entity_type)
            self.spawner_spawner_type_box.set_value(spawner_object.spawner_type)
            self.spawner_rate_box.set_value(str(spawner_object.rate))


def str_to_float(string):
    if string == '':
        return 0.0
    else:
        return float(string)


def str_to_int(integer):
    if integer == '':
        return 0
    else:
        return int(integer)


def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk


if __name__ == '__main__':
    app = ezpygame.Application(
        title='Level Editor',
        resolution=(SCREEN_WIDTH + DETAILS_AREA_WIDTH + PATTERNS_AREA_WIDTH + SPAWNERS_AREA_WIDTH, SCREEN_HEIGHT),
        update_rate=FPS)
    app.run(LevelEditor())

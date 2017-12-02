
import thorpy
import json
from game import *
from GameScene import GameScene
from RenderQueue import RenderQueue
from LevelObject import *


class LevelEditor(GameScene):

    def __init__(self):
        self.level_objects = []
        self.render_queue = RenderQueue()
        self.dragging_object = None
        self.drag_offset = None

        DETAILS_AREA_WIDTH = SCREEN_WIDTH / 5
        PATTERNS_AREA_HEIGHT = SCREEN_HEIGHT / 5

        # Game area
        self.game_area = thorpy.Box.make([], size=(SCREEN_WIDTH - DETAILS_AREA_WIDTH, SCREEN_HEIGHT - PATTERNS_AREA_HEIGHT))
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

        self.details_area = thorpy.Box.make([self.level_details_area, self.pattern_details_area, self.object_details_area],
                                            size=(DETAILS_AREA_WIDTH, SCREEN_HEIGHT))
        self.details_area.set_main_color((255, 220, 255, 180))
        DETAILS_AREA_LEFT = SCREEN_WIDTH - DETAILS_AREA_WIDTH
        self.details_area.set_topleft((DETAILS_AREA_LEFT, 0))

        # Patterns area
        patterns_title = thorpy.make_text('Patterns', 18, (0, 0, 0))

        def click_pattern(pattern_id, surfdata):
            level_object = LevelObject(objectDefinition={
                'type': pattern_id,
                'x': 0,
                'y': 0,
                'z': 0,
            })  # TODO: Do we need to pass in surf data here?
            self.level_objects.append(level_object)

        # Load the already-created patterns
        patterns = []
        pattern_objects = []
        LevelObjectPattern.init()
        with open('patterns.json', 'r') as patterns_file:
            patterns_descriptions = json.load(patterns_file)
        for pattern_id, pattern_definition in patterns_descriptions.items():
            pattern = LevelObjectPattern(pattern_definition)
            patterns.append(pattern)
            # TODO: Add a small version of the image to this object
            pattern_object = thorpy.make_button(pattern_id, func=click_pattern, params={'pattern_id': pattern_id, 'surfdata': pattern_definition['surfdata']})
            pattern_objects.append(pattern_object)
        # TODO: Add horizontal scroller to patterns section

        self.patterns_area = thorpy.Box.make([patterns_title, *pattern_objects],
                                             size=(SCREEN_WIDTH - DETAILS_AREA_WIDTH, PATTERNS_AREA_HEIGHT))
        self.patterns_area.set_main_color((220, 220, 255, 180))
        PATTERNS_AREA_TOP = SCREEN_HEIGHT - PATTERNS_AREA_HEIGHT
        self.patterns_area.set_topleft((0, PATTERNS_AREA_TOP))
        thorpy.store(self.patterns_area, mode='h', gap=15, x=0, align='top')

        self.menu = thorpy.Menu([self.game_area, self.patterns_area, self.details_area])

    def load_level(self):
        file_name = self.level_name_box.get_value()
        if not file_name.endswith('.json'):
            file_name += '.json'
        with open(os.path.join('levels', file_name), 'r') as level_file:
            level_info = json.load(level_file)
        self.level_width_box.set_value(level_info['width'])
        self.level_height_box.set_value(level_info['height'])
        self.gravity_box.set_value(level_info['gravity'])
        self.jump_height_box.set_value(level_info['jumpheight'])
        self.player_speed_box.set_value(level_info['playerspeed'])
        self.level_objects = []
        for level_object_info in level_info['objects']:
            self.level_objects.append(LevelObject(objectDefinition=level_object_info))

    def save_level(self):
        # Collect level details
        level = {
            'width': self.level_width_box.get_value(),
            'height': self.level_height_box.get_value(),
            'gravity': self.gravity_box.get_value(),
            'jumpheight': self.jump_height_box.get_value(),
            'playerspeed': self.player_speed_box.get_value(),
            'objects': [],
        }
        # Collect objects
        for level_object in self.level_objects:
            level['objects'].append({
                'type': level_object.type,
                'x': level_object.block_position[0],
                'y': level_object.block_position[1],
                'z': level_object.z_index
            })
        # Write file
        file_name = self.level_name_box.get_value()
        if not file_name.endswith('.json'):
            file_name += '.json'
        with open(os.path.join('levels', file_name), 'w') as file:
            json.dump(level, file, indent=2)

    def draw(self, screen):
        for level_object in self.level_objects:
            level_object.draw(self.render_queue)
        self.render_queue.flush(screen)

        for element in [self.game_area, self.patterns_area, self.details_area]:
            element.blit()

    def update(self, dt):
        for element in [self.game_area, self.patterns_area, self.details_area]:
            element.update()

    def handle_event(self, event):
        self.menu.react(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # See if we are clicking on a game element
                for level_object in self.level_objects:
                    mouse_x, mouse_y = event.pos
                    if level_object.draw_position[0] < mouse_x < level_object.draw_position[0] + level_object.pattern.image.get_width() \
                            and level_object.draw_position[1] < mouse_y < level_object.draw_position[1] + level_object.pattern.image.get_height():
                        self.dragging_object = level_object
                        self.drag_offset = (level_object.draw_position[0] - mouse_x, level_object.draw_position[1] - mouse_y)
                        self.update_object_details_area(level_object)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.update_object_details_area(self.dragging_object)
                self.dragging_object = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_object is not None:
                mouse_x, mouse_y = event.pos
                self.dragging_object.set_draw_position(mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1])
                self.update_object_details_area(self.dragging_object)

    def update_object_details_area(self, level_object):
        if level_object is None:
            self.top_box.set_value('')
            self.left_box.set_value('')
            self.z_box.set_value('')
        else:
            self.top_box.set_value(str(level_object.draw_position[1]))
            self.left_box.set_value(str(level_object.draw_position[0]))
            self.z_box.set_value(str(level_object.z_index))

            self.pattern_id_box.set_value(level_object.type)
            self.image_file_box.set_value(level_object.pattern.definition['image'])
            self.pattern_width_box.set_value(str(level_object.pattern.definition['width']))
            self.pattern_height_box.set_value(str(level_object.pattern.definition['height']))
            self.block_data_box.set_value('')
            self.stand_data_box.set_value('')
            self.climb_data_box.set_value('')
            self.damage_data_box.set_value('')


if __name__ == '__main__':
    app = ezpygame.Application(title='Level Editor', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(LevelEditor())

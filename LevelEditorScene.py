
import thorpy
import json
from game import *
from GameScene import GameScene
from LevelObject import *


class LevelEditor(GameScene):

    def __init__(self):
        DETAILS_AREA_WIDTH = SCREEN_WIDTH / 5
        PATTERNS_AREA_HEIGHT = SCREEN_HEIGHT / 5

        # Game area
        self.game_area = thorpy.Box.make([], size=(SCREEN_WIDTH - DETAILS_AREA_WIDTH, SCREEN_HEIGHT - PATTERNS_AREA_HEIGHT))
        self.game_area.set_main_color((220, 255, 220, 180))

        # Level details area
        level_details_title = thorpy.make_text('Level Details', 18, (0, 0, 0))
        level_width_box = thorpy.Inserter.make(name='Width: ', value='')
        level_height_box = thorpy.Inserter.make(name='Height: ', value='')
        gravity_box = thorpy.Inserter.make(name='Gravity: ', value='')
        jump_height_box = thorpy.Inserter.make(name='Jump height: ', value='')
        player_speed_box = thorpy.Inserter.make(name='Player speed: ', value='')
        self.level_details_area = thorpy.Box.make([level_details_title, level_width_box, level_height_box, gravity_box, jump_height_box, player_speed_box])

        # Pattern details area
        pattern_details_title = thorpy.make_text('Pattern Details', 18, (0, 0, 0))
        pattern_id_box = thorpy.Inserter.make(name='ID: ', value='')
        image_file_box = thorpy.Inserter.make(name='Image file: ', value='')
        pattern_width_box = thorpy.Inserter.make(name='Width: ', value='')
        pattern_height_box = thorpy.Inserter.make(name='Height: ', value='')
        block_data_box = thorpy.Inserter.make(name='Block data: ', value='')
        stand_data_box = thorpy.Inserter.make(name='Stand data: ', value='')
        climb_data_box = thorpy.Inserter.make(name='Climb data: ', value='')
        damage_data_box = thorpy.Inserter.make(name='Damage data: ', value='')
        self.pattern_details_area = thorpy.Box.make([pattern_details_title, pattern_id_box, image_file_box, pattern_width_box, pattern_height_box, block_data_box, stand_data_box, climb_data_box, damage_data_box])

        # Object details area
        object_details_title = thorpy.make_text('Object Details', 18, (0, 0, 0))
        top_box = thorpy.Inserter.make(name='Top: ', value='')
        left_box = thorpy.Inserter.make(name='Left: ', value='')
        z_box = thorpy.Inserter.make(name='Z index: ', value='')
        self.object_details_area = thorpy.Box.make([object_details_title, top_box, left_box, z_box])

        self.details_area = thorpy.Box.make([self.level_details_area, self.pattern_details_area, self.object_details_area],
                                            size=(DETAILS_AREA_WIDTH, SCREEN_HEIGHT))
        self.details_area.set_main_color((255, 220, 255, 180))
        DETAILS_AREA_LEFT = SCREEN_WIDTH - DETAILS_AREA_WIDTH
        self.details_area.set_topleft((DETAILS_AREA_LEFT, 0))

        # Patterns area
        patterns_title = thorpy.make_text('Patterns', 18, (0, 0, 0))

        # TODO: Make "Add new pattern" button work
        add_pattern_button = thorpy.make_button('Add pattern')
        # TODO: Put add button under title (new ghost to contain them), with "save patterns file" button

        # Load the already-created patterns
        patterns = []
        pattern_objects = []
        with open('patterns.json', 'r') as patterns_file:
            patterns_descriptions = json.load(patterns_file)
        for pattern_id, pattern_definition in patterns_descriptions.items():
            pattern = LevelObjectPattern(pattern_definition)
            patterns.append(pattern)
            # pattern_image = thorpy.Image.make(os.path.join('assets', pattern_definition['image']))
            # pattern_image.scale_to_title()
            pattern_object = thorpy.Draggable.make(pattern_id) #, [pattern.image]) #[pattern_image])
            pattern_objects.append(pattern_object)

        self.patterns_area = thorpy.Box.make([patterns_title, add_pattern_button, *pattern_objects],
                                             size=(SCREEN_WIDTH - DETAILS_AREA_WIDTH, PATTERNS_AREA_HEIGHT))
        self.patterns_area.set_main_color((220, 220, 255, 180))
        PATTERNS_AREA_TOP = SCREEN_HEIGHT - PATTERNS_AREA_HEIGHT
        self.patterns_area.set_topleft((0, PATTERNS_AREA_TOP))
        thorpy.store(self.patterns_area, mode='h', gap=15, x=0, align='top')

        # Click actions
        def click(event):
            # TODO: Switch out the details areas, to only show one at once
            if event.pos[0] > DETAILS_AREA_LEFT:
                print('details area')
                # self.pattern_details_area.set_visible(False)
            elif event.pos[1] > PATTERNS_AREA_TOP:
                print('patterns area')
            else:
                print('level area')
        reac_click = thorpy.Reaction(pygame.MOUSEBUTTONDOWN, click, {"button": thorpy.parameters.LEFT_CLICK_BUTTON})
        self.patterns_area.add_reaction(reac_click)

        self.menu = thorpy.Menu([self.game_area, self.patterns_area, self.details_area])

    def draw(self, screen):
        for element in [self.game_area, self.patterns_area, self.details_area]:
            element.blit()

    def update(self, dt):
        for element in [self.game_area, self.patterns_area, self.details_area]:
            element.update()

    def handle_event(self, event):
        self.menu.react(event)


if __name__ == '__main__':
    app = ezpygame.Application(title='Level Editor', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(LevelEditor())

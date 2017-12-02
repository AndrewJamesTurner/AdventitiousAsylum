from game import pygame, SCREEN_WIDTH, SCREEN_HEIGHT, ezpygame, FPS, get_shared_values
from GameScene import GameScene
from RenderQueue import RenderQueue
from enemy import Enemy
from items import physical_type, mental_type, chemical_type
from items import ItemGenerator
from items import ItemEffectiveness
from random import randint

player_move_select_state = "player_move_select_state"
player_attack_animation_state = "player_attack_animation_state"
player_message_state = "player_message_state"
enemy_move_select_state = "enemy_move_select_state"
enemy_attack_animation_state = "enemy_attack_animation_state"
enemy_message_state = "enemy_message_state"


def draw_health_bar(render_queue, x, y, health_percentage):

    length = 150
    height = 22

    back = pygame.Surface((length, height))
    back.fill((255, 0, 0))

    front = pygame.Surface((length, height))
    front.fill((0, 255, 0))

    render_queue.add((x, y), back, z_index=20)
    render_queue.add((x, y), front, scale=(health_percentage, 1), z_index=21)


def get_multiplier(attack_type, defence_type):

    multiplier = 1

    beat_multiplier = 2
    lose_multiplier = 0.5

    if attack_type == chemical_type and defence_type == mental_type:
        multiplier = beat_multiplier

    if attack_type == mental_type and defence_type == physical_type:
        multiplier = beat_multiplier

    if attack_type == physical_type and defence_type == chemical_type:
        multiplier = beat_multiplier

    if attack_type == mental_type and defence_type == chemical_type:
        multiplier = lose_multiplier

    if attack_type == physical_type and defence_type == mental_type:
        multiplier = lose_multiplier

    if attack_type == chemical_type and defence_type == physical_type:
        multiplier = lose_multiplier

    return multiplier


class BattleScene(GameScene):

    def leave_scene(self):

        get_shared_values().health = self.health
        get_shared_values().enemy = None

        self.application.change_scene(self.previous_scene)

    def on_enter(self, previous_scene):

        super(BattleScene, self).on_enter(previous_scene)

        self.previous_scene = previous_scene
        self.state = player_move_select_state
        self.items = get_shared_values().items
        self.health = get_shared_values().health
        self.max_health = get_shared_values().max_health
        self.type = get_shared_values().type
        self.enemy = get_shared_values().enemy
        self.image = get_shared_values().image
        self.currently_selected_item = 0
        self.enemy_selected_item = 0

        self.message = ""

        self.player_image = pygame.image.load("assets/astronaut_small.png")
        self.enemy_image = pygame.image.load("assets/astronaut_small.png")

        self.blue_move = pygame.image.load("assets/battle-background-images/blue-rect.png")
        self.black_move = pygame.image.load("assets/battle-background-images/black-rect.png")

        self.render_queue = RenderQueue()

        # remove this
        self.enemy = Enemy("Bob", 1000, physical_type, [ItemGenerator().getItemByName("pillow"), ItemGenerator().getItemByName("spaceship"), ItemGenerator().getItemByName("tugboat")])

        self.move_font = pygame.font.Font("assets/Courgette-Regular.ttf", 24)

    def draw(self, screen):

        self.render_queue.flush(screen)

    def update(self, dt):

        if self.health <= 0 or self.enemy.health <= 0:
            self.leave_scene()

        draw_health_bar(self.render_queue, 218, 342, self.health / self.max_health)

        draw_health_bar(self.render_queue, 605, 82, self.enemy.health / self.enemy.max_health)

        enemy_pos_x = 765
        enemy_pos_y = 50
        self.render_queue.add((enemy_pos_x, enemy_pos_y), self.enemy.image, z_index=1)

        player_pos_x = 95
        player_pos_y = 111
        self.render_queue.add((player_pos_x, player_pos_y), self.image, z_index=1)

        if self.state == player_move_select_state:

            move_x_left = 90
            move_x_right = 510

            move_y_top = 410
            move_y_bottom = 480

            text_y_offset = 10
            move_name_x_offset = 20
            move_power_x_offset = 150
            move_type_x_offset = 250

            font_colour = (0, 0, 0)

            if len(self.items) > 0:

                name_text = self.move_font.render(str(self.items[0].name), True, font_colour)
                damage_text = self.move_font.render(str(self.items[0].damage), True, font_colour)
                type_text = self.move_font.render(self.items[0].type, True, font_colour)

                self.render_queue.add((move_x_left, move_y_top), self.black_move, z_index=1)
                self.render_queue.add((move_x_left + move_name_x_offset, move_y_top + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_left + move_power_x_offset, move_y_top + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_left + move_type_x_offset, move_y_top + text_y_offset), type_text, z_index=2)

            if len(self.items) > 1:

                name_text = self.move_font.render(str(self.items[1].name), True, font_colour)
                damage_text = self.move_font.render(str(self.items[1].damage), True, font_colour)
                type_text = self.move_font.render(str(self.items[1].type), True, font_colour)

                self.render_queue.add((move_x_right, move_y_top), self.black_move)
                self.render_queue.add((move_x_right + move_name_x_offset, move_y_top + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_right + move_power_x_offset, move_y_top + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_right + move_type_x_offset, move_y_top + text_y_offset), type_text, z_index=2)

            if len(self.items) > 2:

                name_text = self.move_font.render(str(self.items[2].name), True, font_colour)
                damage_text = self.move_font.render(str(self.items[2].damage), True, font_colour)
                type_text = self.move_font.render(str(self.items[2].type), True, font_colour)

                self.render_queue.add((move_x_left, move_y_bottom), self.black_move)
                self.render_queue.add((move_x_left + move_name_x_offset, move_y_bottom + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_left + move_power_x_offset, move_y_bottom + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_left + move_type_x_offset, move_y_bottom + text_y_offset), type_text, z_index=2)

            if len(self.items) > 3:
                self.render_queue.add((move_x_right, move_y_bottom), self.black_move)

            if self.currently_selected_item == 0:
                self.render_queue.add((move_x_left, move_y_top), self.blue_move)
            if self.currently_selected_item == 1:
                self.render_queue.add((move_x_right, move_y_top), self.blue_move)
            if self.currently_selected_item == 2:
                self.render_queue.add((move_x_left, move_y_bottom), self.blue_move)
            if self.currently_selected_item == 3:
                self.render_queue.add((move_x_right, move_y_bottom), self.blue_move)

        elif self.state == player_attack_animation_state:

            attack_type = self.items[self.currently_selected_item].type
            defence_type = self.enemy.type
            damage = self.items[self.currently_selected_item].damage

            damage = damage * get_multiplier(attack_type, defence_type)

            self.enemy.health -= damage

            self.state = player_message_state

            item_name = self.items[self.currently_selected_item].name

            attack_type = self.items[self.currently_selected_item].type
            defence_type = self.enemy.type

            if get_multiplier(attack_type, defence_type) > 1:
                effectiveness = ItemEffectiveness().get_rand_high_effective()
            if get_multiplier(attack_type, defence_type) < 1:
                effectiveness = ItemEffectiveness().get_rand_neutral_effective()
            if get_multiplier(attack_type, defence_type) == 1:
                effectiveness = ItemEffectiveness().get_rand_low_effective()

            self.message = "Player attacked {0} with {1}. It was {2}!".format(self.enemy.name, item_name, effectiveness)

        elif self.state == player_message_state:

            font_colour = (0, 0, 0)
            text = self.move_font.render(self.message, True, font_colour)

            self.render_queue.add((100, 100), text, z_index=1)

        elif self.state == enemy_move_select_state:

            self.enemy_selected_item = randint(0, len(self.enemy.items) - 1)
            self.state = enemy_attack_animation_state

        elif self.state == enemy_attack_animation_state:

            attack_type = self.enemy.items[self.enemy_selected_item].type
            defence_type = self.type
            damage = self.items[self.currently_selected_item].damage
            damage = damage * get_multiplier(attack_type, defence_type)

            self.health -= damage

            self.state = enemy_message_state

            item_name = self.enemy.items[self.enemy_selected_item].name

            attack_type = self.enemy.items[self.enemy_selected_item].type
            defence_type = self.type

            if get_multiplier(attack_type, defence_type) > 1:
                effectiveness = ItemEffectiveness().get_rand_high_effective()
            if get_multiplier(attack_type, defence_type) < 1:
                effectiveness = ItemEffectiveness().get_rand_neutral_effective()
            if get_multiplier(attack_type, defence_type) == 1:
                effectiveness = ItemEffectiveness().get_rand_low_effective()

            self.message = "{0} attacked Player with {1}. It was {2}!".format(self.enemy.name, item_name, effectiveness)

        elif self.state == enemy_message_state:

            font_colour = (0, 0, 0)
            text = self.move_font.render(self.message, True, font_colour)

            self.render_queue.add((100, 100), text, z_index=1)

    def handle_event(self, event):

        if self.state == player_move_select_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.currently_selected_item += 1

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.currently_selected_item += 2

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.currently_selected_item -= 1

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.currently_selected_item -= 2

                self.currently_selected_item = self.currently_selected_item % len(self.items)

                if event.key == pygame.K_RETURN:
                    self.state = player_attack_animation_state

        elif self.state == player_message_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    self.state = enemy_move_select_state

        elif self.state == enemy_message_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    self.state = player_move_select_state


if __name__ == '__main__':

    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)

    app.run(BattleScene())

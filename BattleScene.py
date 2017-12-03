from game import pygame, SCREEN_WIDTH, SCREEN_HEIGHT, ezpygame, FPS
from sharedValues import get_shared_values
from GameScene import GameScene
from RenderQueue import RenderQueue
from movement_path import MovementPath
from orderly import Orderly
from player import Player
from items import physical_type, mental_type, chemical_type
# from items import ItemGenerator
from items import ItemEffectiveness, ItemDescriptor
from random import randint

player_move_select_state = "player_move_select_state"
player_attack_animation_state = "player_attack_animation_state"
player_message_state = "player_message_state"
enemy_move_select_state = "enemy_move_select_state"
enemy_attack_animation_state = "enemy_attack_animation_state"
enemy_message_state = "enemy_message_state"


def draw_health_bar(render_queue, x, y, health_percentage, length, height):

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

        get_shared_values().health = self.player.health
        get_shared_values().enemy = None

        self.application.change_scene(self.previous_scene)

    def get_select_box(self, type):

        if type == physical_type:
            return self.red_move

        if type == mental_type:
            return self.blue_move

        if type == chemical_type:
            return self.green_move

    def on_enter(self, previous_scene):

        super(BattleScene, self).on_enter(previous_scene)

        self.player = get_shared_values().player
        self.enemy = get_shared_values().orderly

        self.previous_scene = previous_scene
        self.state = player_move_select_state

        self.player_selected_item = 0
        self.enemy_selected_item = 0

        self.message = ""

        # self.player.items = get_shared_values().items
        # self.player.health = get_shared_values().health
        # self.max_health = get_shared_values().max_health
        # self.player.type = get_shared_values().type
        # self.image = get_shared_values().image

        # self.player_image = pygame.image.load("assets/characters/astronaut_small2.png")
        # self.enemy_image = pygame.image.load("assets/characters/doctor_woman.png")

        self.blue_move = pygame.image.load("assets/battle-background-images/blue-rect.png")
        self.red_move = pygame.image.load("assets/battle-background-images/red-rect.png")
        self.green_move = pygame.image.load("assets/battle-background-images/green-rect.png")
        self.black_move = pygame.image.load("assets/battle-background-images/black-rect.png")
        self.message_box = pygame.image.load("assets/battle-background-images/message-box.png")
        self.border = pygame.image.load("assets/battle-background-images/border.png")

        self.render_queue = RenderQueue()

        # remove this
        # enemy_items = [
        #     ItemGenerator().getItem(),
        #     ItemGenerator().getItem(),
        #     ItemGenerator().getItem(),
        #     ItemGenerator().getItem(),
        # ]

        # enemy_items = ItemGenerator().getItems(4)

        # self.enemy = Orderly("Bob", "assets/characters/doctor_woman.png", 1000, physical_type, enemy_items)

        self.move_font = pygame.font.Font("assets/Courgette-Regular.ttf", 24)
        self.movement_path = None

    def draw(self, screen):

        self.render_queue.flush(screen)

    def update(self, dt):

        message_box_x = 54
        message_box_y = 420

        message_text_offset_x = 10
        message_text_offset_y = 10

        player_pos_x = 95
        player_pos_y = 111

        enemy_pos_x = 900
        enemy_pos_y = 85

        health_bar_height = 25
        health_bar_width = 200
        health_bar_padding = 15

        if self.player.health <= 0 or self.enemy.health <= 0:
            self.leave_scene()

        player_mid_x = player_pos_x + max(self.player.image_width, health_bar_width) / 2
        enemy_mid_x = enemy_pos_x - max(self.enemy.image_width, health_bar_width) / 2

        draw_health_bar(self.render_queue, player_mid_x - (health_bar_width / 2), player_pos_y + self.player.desired_height + health_bar_padding, self.player.health / self.player.max_health, health_bar_width, health_bar_height)
        draw_health_bar(self.render_queue, enemy_mid_x - (health_bar_width / 2), enemy_pos_y - (health_bar_height + health_bar_padding), self.enemy.health / self.enemy.max_health, health_bar_width, health_bar_height)

        self.render_queue.add((0, 0), self.border, z_index=0)

        self.render_queue.add((enemy_mid_x - self.enemy.image_width/2, enemy_pos_y), self.enemy.image, z_index=1)

        self.render_queue.add((player_mid_x - self.player.image_width/2, player_pos_y), self.player.image, scale=(self.player.image_width_scaler, self.player.image_height_scaler), z_index=1)
        # self.render_queue.add((player_pos_x, player_pos_y), self.player.image, z_index=1)

        if self.state == player_move_select_state:

            move_x_left = 90
            move_x_right = 510

            move_y_top = 410
            move_y_bottom = 480

            text_y_offset = 10
            move_name_x_offset = 20
            move_power_x_offset = 200
            move_type_x_offset = 250

            font_colour = (0, 0, 0)

            if len(self.player.items) > 0:

                name_text = self.move_font.render(str(self.player.items[0].name), True, font_colour)
                damage_text = self.move_font.render(str(self.player.items[0].damage), True, font_colour)
                type_text = self.move_font.render(self.player.items[0].type, True, font_colour)

                self.render_queue.add((move_x_left, move_y_top), self.black_move, z_index=1)
                self.render_queue.add((move_x_left + move_name_x_offset, move_y_top + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_left + move_power_x_offset, move_y_top + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_left + move_type_x_offset, move_y_top + text_y_offset), type_text, z_index=2)

            if len(self.player.items) > 1:

                move_type = self.player.items[1].type

                name_text = self.move_font.render(str(self.player.items[1].name), True, font_colour)
                damage_text = self.move_font.render(str(self.player.items[1].damage), True, font_colour)
                type_text = self.move_font.render(self.player.items[1].type, True, font_colour)

                self.render_queue.add((move_x_right, move_y_top), self.black_move)
                self.render_queue.add((move_x_right + move_name_x_offset, move_y_top + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_right + move_power_x_offset, move_y_top + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_right + move_type_x_offset, move_y_top + text_y_offset), type_text, z_index=2)

            if len(self.player.items) > 2:

                name_text = self.move_font.render(str(self.player.items[2].name), True, font_colour)
                damage_text = self.move_font.render(str(self.player.items[2].damage), True, font_colour)
                type_text = self.move_font.render(self.player.items[2].type, True, font_colour)

                self.render_queue.add((move_x_left, move_y_bottom), self.black_move)
                self.render_queue.add((move_x_left + move_name_x_offset, move_y_bottom + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_left + move_power_x_offset, move_y_bottom + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_left + move_type_x_offset, move_y_bottom + text_y_offset), type_text, z_index=2)

            if len(self.player.items) > 3:

                name_text = self.move_font.render(str(self.player.items[3].name), True, font_colour)
                damage_text = self.move_font.render(str(self.player.items[3].damage), True, font_colour)
                type_text = self.move_font.render(self.player.items[3].type, True, font_colour)

                self.render_queue.add((move_x_right, move_y_bottom), self.black_move)
                self.render_queue.add((move_x_right + move_name_x_offset, move_y_bottom + text_y_offset), name_text, z_index=2)
                self.render_queue.add((move_x_right + move_power_x_offset, move_y_bottom + text_y_offset), damage_text, z_index=2)
                self.render_queue.add((move_x_right + move_type_x_offset, move_y_bottom + text_y_offset), type_text, z_index=2)

            move_type = self.player.items[self.player_selected_item].type

            if self.player_selected_item == 0:
                self.render_queue.add((move_x_left, move_y_top), self.get_select_box(move_type))
            if self.player_selected_item == 1:
                self.render_queue.add((move_x_right, move_y_top), self.get_select_box(move_type))
            if self.player_selected_item == 2:
                self.render_queue.add((move_x_left, move_y_bottom), self.get_select_box(move_type))
            if self.player_selected_item == 3:
                self.render_queue.add((move_x_right, move_y_bottom), self.get_select_box(move_type))

        elif self.state == player_attack_animation_state:

            attack_type = self.player.items[self.player_selected_item].type

            if self.movement_path is None:
                self.movement_path = MovementPath(player_pos_x + self.player.image_width, player_pos_y + 50, 1000, [(0, 0), (SCREEN_WIDTH*0.27, -SCREEN_HEIGHT * 0.4), (SCREEN_WIDTH*0.5, -SCREEN_HEIGHT * 0.1)])
            else:
                if self.movement_path.is_done():
                    self.state = player_message_state
                    self.movement_path = None

                    defence_type = self.enemy.type
                    damage = self.player.items[self.player_selected_item].damage

                    damage = damage * get_multiplier(attack_type, defence_type)

                    self.enemy.health -= damage

                else:
                    self.movement_path.step(dt)

                    item_image = self.player.items[self.player_selected_item].image
                    self.render_queue.add(self.movement_path.get_position(), item_image, z_index=100)

            item_name = self.player.items[self.player_selected_item].name

            attack_type = self.player.items[self.player_selected_item].type
            defence_type = self.enemy.type

            if get_multiplier(attack_type, defence_type) > 1:
                effectiveness = ItemEffectiveness().get_rand_high_effective()
            elif get_multiplier(attack_type, defence_type) < 1:
                effectiveness = ItemEffectiveness().get_rand_neutral_effective()
            else:  # get_multiplier(attack_type, defence_type) == 1:
                effectiveness = ItemEffectiveness().get_rand_low_effective()

            item_descripter = ItemDescriptor().getDescriptor()

            self.message = "Player attacked {0} with {3} {1} and it was {2}!".format(self.enemy.name, item_name, effectiveness, item_descripter)

        elif self.state == player_message_state:

            font_colour = (0, 0, 0)
            text = self.move_font.render(self.message, True, font_colour)

            self.render_queue.add((message_box_x, message_box_y), self.message_box, z_index=0)
            self.render_queue.add((message_box_x + message_text_offset_x, message_box_y + message_text_offset_y), text, z_index=1)

        elif self.state == enemy_move_select_state:

            self.enemy_selected_item = randint(0, len(self.enemy.items) - 1)
            self.state = enemy_attack_animation_state

        elif self.state == enemy_attack_animation_state:

            if self.movement_path is None:
                self.movement_path = MovementPath(enemy_pos_x - 2*self.enemy.items[self.enemy_selected_item].image.get_width(), enemy_pos_y + 100, 1000, [(0, 0), (-SCREEN_WIDTH*0.27, -SCREEN_HEIGHT * 0.4), (-SCREEN_WIDTH*0.5, -SCREEN_HEIGHT * 0.1)])

            else:
                if self.movement_path.is_done():

                    self.state = enemy_message_state
                    self.movement_path = None

                    attack_type = self.enemy.items[self.enemy_selected_item].type
                    defence_type = self.player.type
                    damage = self.enemy.items[self.enemy_selected_item].damage
                    damage = damage * get_multiplier(attack_type, defence_type)

                    self.player.health -= damage
                else:
                    self.movement_path.step(dt)

                    item_image = self.enemy.items[self.enemy_selected_item].image
                    self.render_queue.add(self.movement_path.get_position(), item_image, z_index=100)

            item_name = self.enemy.items[self.enemy_selected_item].name

            attack_type = self.enemy.items[self.enemy_selected_item].type
            defence_type = self.player.type

            if get_multiplier(attack_type, defence_type) > 1:
                effectiveness = ItemEffectiveness().get_rand_high_effective()
            if get_multiplier(attack_type, defence_type) < 1:
                effectiveness = ItemEffectiveness().get_rand_neutral_effective()
            if get_multiplier(attack_type, defence_type) == 1:
                effectiveness = ItemEffectiveness().get_rand_low_effective()

            item_descripter = ItemDescriptor().getDescriptor()

            self.message = "{0} attacked Player with {3} {1} and it was {2}!".format(self.enemy.name, item_name, effectiveness, item_descripter)

        elif self.state == enemy_message_state:

            font_colour = (0, 0, 0)
            text = self.move_font.render(self.message, True, font_colour)

            self.render_queue.add((message_box_x, message_box_y), self.message_box, z_index=0)
            self.render_queue.add((message_box_x + message_text_offset_x, message_box_y + message_text_offset_y), text, z_index=1)

    def handle_event(self, event):

        if self.state == player_move_select_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player_selected_item += 1

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player_selected_item += 2

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player_selected_item -= 1

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player_selected_item -= 2

                self.player_selected_item = self.player_selected_item % len(self.player.items)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.state = player_attack_animation_state

        elif self.state == player_message_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.state = enemy_move_select_state

        elif self.state == enemy_message_state:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.state = player_move_select_state


if __name__ == '__main__':

    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)

    get_shared_values().orderly = Orderly("doctor woman")
    get_shared_values().player = Player("spedecWoman")


    app.run(BattleScene())

from game import pygame, SCREEN_WIDTH, SCREEN_HEIGHT, ezpygame, FPS, get_shared_values
from GameScene import GameScene
from RenderQueue import RenderQueue
from enemy import Enemy
from items import physical_type, mental_type, chemical_type
from items import ItemGenerator
from random import randint

player_move_select_state = "player_move_select_state"
player_attack_animation_state = "player_attack_animation_state"
player_message_state = "player_message_state"
enemy_move_select_state = "enemy_move_select_state"
enemy_attack_animation_state = "enemy_attack_animation_state"
enemy_message_state = "enemy_message_state"


def draw_health_bar(render_queue, x, y, health_percentage):

    back = pygame.Surface((200, 20))
    back.fill((255, 0, 0))

    front = pygame.Surface((200, 20))
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
        self.currently_selected_item = 0
        self.enemy_selected_item = 0

        self.player_image = pygame.image.load("assets/astronaut_small.png")
        self.enemy_image = pygame.image.load("assets/astronaut_small.png")

        self.blue_move = pygame.image.load("assets/battle-background-images/blue-rect.png")
        self.black_move = pygame.image.load("assets/battle-background-images/black-rect.png")

        self.render_queue = RenderQueue()

        # remove this
        self.enemy = Enemy(1000, physical_type, [ItemGenerator().getItemByName("pillow"), ItemGenerator().getItemByName("spaceship"), ItemGenerator().getItemByName("tug boat")])

        self.move_font = pygame.font.Font("assets/Courgette-Regular.ttf", 24)

    def draw(self, screen):

        self.render_queue.flush(screen)

    def update(self, dt):

        if self.health <= 0 or self.enemy.health <= 0:
            self.leave_scene()

        draw_health_bar(self.render_queue, 50, 50, self.health / self.max_health)
        draw_health_bar(self.render_queue, 500, 50, self.enemy.health / self.enemy.max_health)

        if self.state == player_move_select_state:

            move_x_left = 88
            move_x_right = 509

            move_y_top = 200
            move_y_bottom = 400

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
                self.render_queue.add((88, 200), self.blue_move)
            if self.currently_selected_item == 1:
                self.render_queue.add((509, 200), self.blue_move)
            if self.currently_selected_item == 2:
                self.render_queue.add((88, 400), self.blue_move)
            if self.currently_selected_item == 3:
                self.render_queue.add((509, 400), self.blue_move)

        elif self.state == player_attack_animation_state:

            attack_type = self.items[self.currently_selected_item].type
            defence_type = self.enemy.type
            damage = self.items[self.currently_selected_item].damage

            damage = damage * get_multiplier(attack_type, defence_type)

            self.enemy.health -= damage

            self.state = player_message_state

        elif self.state == player_message_state:
            self.state = enemy_move_select_state

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

        elif self.state == enemy_message_state:
            self.state = player_move_select_state

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

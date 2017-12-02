from game import pygame, SCREEN_WIDTH, SCREEN_HEIGHT, ezpygame, FPS, get_shared_values
from GameScene import GameScene
from RenderQueue import RenderQueue
# from enemy import Enemy

player_move_select_state = "player_move_select_state"
player_attack_animation_state = "player_attack_animation_state"
player_message_state = "player_message_state"
enemy_move_select_state = "enemy_move_select_state"
enemy_attack_animation_state = "enemy_attack_animation_state"
enemy_message_state = "enemy_message_state"


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
        self.enemy = get_shared_values().enemy
        self.currently_selected_item = 0

        self.player_image = pygame.image.load("assets/astronaut_small.png")
        self.enemy_image = pygame.image.load("assets/astronaut_small.png")

        self.blue_move = pygame.image.load("assets/battle-background-images/blue-rect.png")
        self.black_move = pygame.image.load("assets/battle-background-images/black-rect.png")

        self.render_queue = RenderQueue()

    def draw(self, screen):

        self.render_queue.flush(screen)

    def update(self, dt):

        if self.state == player_move_select_state:

            self.render_queue.add((88, 200), self.black_move)
            self.render_queue.add((509, 200), self.black_move)
            self.render_queue.add((88, 400), self.black_move)
            self.render_queue.add((509, 400), self.black_move)

            if self.currently_selected_item == 0:
                self.render_queue.add((88, 200), self.blue_move)
            if self.currently_selected_item == 1:
                self.render_queue.add((509, 200), self.blue_move)
            if self.currently_selected_item == 2:
                self.render_queue.add((88, 400), self.blue_move)
            if self.currently_selected_item == 3:
                self.render_queue.add((509, 400), self.blue_move)

        elif self.state == player_attack_animation_state:
            self.state = player_message_state

        elif self.state == player_message_state:
            self.state = enemy_move_select_state

        elif self.state == enemy_move_select_state:
            self.state = enemy_attack_animation_state

        elif self.state == enemy_attack_animation_state:
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

                self.currently_selected_item = self.currently_selected_item % 4  # len(self.items)

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

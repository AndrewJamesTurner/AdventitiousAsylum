from game import pygame, SCREEN_WIDTH, SCREEN_HEIGHT, ezpygame, FPS
from GameScene import GameScene
from RenderQueue import RenderQueue


class BattleScene(GameScene):

    def on_enter(self, previous_scene):

        super(BattleScene, self).on_enter(previous_scene)

        self.pos_x = 0
        self.pos_y = 0

        self.player = pygame.image.load("assets/astronaut_small.png")
        self.enemy = pygame.image.load("assets/astronaut_small.png")
        self.moves = pygame.image.load("assets/display.png")


        self.render_queue = RenderQueue()

    def draw(self, screen):

        # screen.fill((50, 100, 255))

        self.render_queue.flush(screen)



    def update(self, dt):

        self.render_queue.add((self.pos_x * SCREEN_WIDTH, self.pos_y * SCREEN_HEIGHT), self.player, z_index=1000)
        # self.render_queue.add((0.7 * SCREEN_WIDTH, 0.05 * SCREEN_HEIGHT), self.enemy)
        self.render_queue.add((0.7 * SCREEN_WIDTH, 0.05 * SCREEN_HEIGHT), self.enemy)
        self.render_queue.add((0.01 * SCREEN_WIDTH, 0.6 * SCREEN_HEIGHT), self.moves)




        # screen.blit(self.player, (0.1 * SCREEN_WIDTH, 0.3 * SCREEN_HEIGHT))
        # # screen.blit(self.player, (self.pos_x * SCREEN_WIDTH, self.pos_y * SCREEN_HEIGHT))
        # screen.blit(self.enemy, (0.7 * SCREEN_WIDTH, 0.05 * SCREEN_HEIGHT))
        # screen.blit(self.moves, (0.01 * SCREEN_WIDTH, 0.6 * SCREEN_HEIGHT))

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.pos_x += 0.01
                self.pos_y += 0.01


if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(BattleScene())

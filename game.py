#!/usr/bin/env python3
import os

import ezpygame
import pygame

from constants import *
from items import ItemGenerator, none_type

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

pygame.init()

CAMERA_POSITION = (0, 0)


def set_camera_position(x,y):
    global CAMERA_POSITION
    CAMERA_POSITION = (x, y)


def world_to_screen_coordinates(world_coords):
    window_coords = (   world_coords[0] - CAMERA_POSITION[0],
                        world_coords[1] - CAMERA_POSITION[1] )
    screen_coords = (   SCREEN_WIDTH  / 2 + window_coords[0] * PPM,
                        SCREEN_HEIGHT / 2 - window_coords[1] * PPM )
    return screen_coords

def screen_to_world_coordinates(screen_coords):
    window_coords = (   (screen_coords[0] - SCREEN_WIDTH / 2) / PPM,
                        (SCREEN_HEIGHT / 2 - screen_coords[1]) / PPM )
    world_coords  = (   window_coords[0] + CAMERA_POSITION[0],
                        window_coords[1] + CAMERA_POSITION[1] )
    return world_coords

# Scenes
menu_scene = None
message_scene = None
platformer_scene = None
battle_scene = None
game_over_scene = None
win_scene = None

def get_menu_scene():
    global menu_scene
    if menu_scene is None:
        from StartMenuScene import StartMenuScene
        menu_scene = StartMenuScene()
    return menu_scene

def get_message_scene():
    global message_scene
    if message_scene is None:
        from MessageScreenScene import MessageScene
        message_scene = MessageScene()
    return message_scene

def get_platformer_scene():
    global platformer_scene
    if platformer_scene is None:
        from PlatformerScene import PlatformerScene
        platformer_scene = PlatformerScene()
    return platformer_scene

def get_battle_scene():
    global battle_scene
    if battle_scene is None:
        from BattleScene import BattleScene
        battle_scene = BattleScene()
    return battle_scene

def get_game_over_scene():
    global game_over_scene
    if game_over_scene is None:
        from GameOverScene import GameOverScene
        game_over_scene = GameOverScene()
    return game_over_scene

def get_win_scene():
    global win_scene
    if win_scene is None:
        from WinScene import WinScene
        win_scene = WinScene()
    return win_scene

# Values shared by every scene
shared_values = None


class SharedValues:

    import constants

    # items = [
    #     ItemGenerator().getItemByName("pillow"),
    # ]

    items = ItemGenerator().getItems(4)

    playerentity = 'spedecWoman' # Which entity do we use for the player

    health = 1000
    max_health = health
    enemy = None
    image = pygame.image.load("assets/characters/spedec.png")
    type = none_type

    def reset(self):

        import constants
        self.items = [create_pillow()]
        self.health = 100
        self.enemy = None

def get_shared_values():

    global shared_values
    if shared_values is None:
        shared_values = SharedValues()
    return shared_values

if __name__ == '__main__':
    app = ezpygame.Application(title="Metal Ass", resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(get_menu_scene())

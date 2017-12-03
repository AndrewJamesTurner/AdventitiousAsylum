from items import ItemGenerator, none_type
import json
from game import pygame
from animation import Animation


class Player:

    def __init__(self, name):

        self.items = [ItemGenerator().getItemByName("pillow")]
        self.name = name
        self.health = 1000
        self.max_health = 1000
        self.type = none_type

        for thing in json.load(open('entities.json'))["player"]:
            if thing["name"] == name:

                self.anim = Animation(True,
                                      pygame.image.load('assets/characters/spedec-2/spedec-man-walk-2-sheet.png'), 180)

                image_width = self.anim.get_current_frame().get_width()
                image_height = self.anim.get_current_frame().get_height()

                self.desired_height = 250
                ratio = self.desired_height / image_height

                self.image_width_scaler = ratio
                self.image_height_scaler = ratio

                self.image_width = image_width * ratio
                self.image_height = self.desired_height


    def add_item(self, item):

        self.items.append(item)

        if len(self.items) == 5:
            return self.items.pop(0)
        else:
            return None

    def adjust_health(self, change):
        self.health += change
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0
        return self.health > 0

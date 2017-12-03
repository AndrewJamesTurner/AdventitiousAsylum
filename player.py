from items import ItemGenerator, none_type
import json
from game import pygame


class Player:

    def __init__(self, name):

        self.items = [ItemGenerator().getItemByName("pillow")]
        self.name = name
        self.health = 1000
        self.max_health = 1000
        self.type = none_type

        for thing in json.load(open('entities.json'))["player"]:
            if thing["name"] == name:

                self.image_path = thing["image"]
                self.image = pygame.image.load("assets/" + self.image_path)

                image_width = self.image.get_width()
                image_height = self.image.get_height()

                desired_height = 280
                ratio = desired_height / image_height

                self.image_width_scaler = ratio
                self.image_height_scaler = ratio

                self.image_width = image_width * ratio
                self.image_height = desired_height

    def add_item(self, item):

        self.items.append(item)

        if len(self.items) == 5:
            return self.items.pop(0)
        else:
            return None

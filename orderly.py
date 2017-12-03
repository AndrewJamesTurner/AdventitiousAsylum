# from items import physical_type, mental_type, chemical_type
# from game import pygame
import json
# from random import shuffle
# import random
from items import ItemGenerator
from game import pygame


class Orderly:

    def __init__(self, name):

        _json = json.load(open('entities.json'))

        for thing in _json["orderly"]:
            if thing["name"] == name:
                orderly_json = thing

        self.name = name
        self.health = 1000
        self.max_health = 1000
        self.type = orderly_json["type"]
        self.items = [ItemGenerator().getItemByName("pillow")]
        # self.image = orderly_json["image"]

        self.image_path = orderly_json["image"]
        self.image = pygame.image.load("assets/" + self.image_path)

        image_width = self.image.get_width()
        image_height = self.image.get_height()

        desired_height = 300
        ratio = desired_height / image_height

        self.image_width_scaler = ratio
        self.image_height_scaler = ratio


# class OrderlyGenerator:

#     def __init__(self):

#         orderlys = json.load(open('entities.json'))["orderly"]

#         self.orderlys = []

#         for ordd in orderlys:

#             xxx = Orderly(ordd["name"], ordd["image"], ordd["type"], [])
#             self.orderlys.append(xxx)

#     def getOrderly(self):

#         ordd = self.orderlys[random.randint(0, len(self.orderlys)-1)]
#         return ordd

#     def getOrderlys(self, num=4):

#         shuffle(self.orderlys)

#         return self.orderlys[0:num]

#     def getOrderlyByName(self, name):

#         itemFound = False

#         for xxx in self.orderlys:

#             if xxx.name == name:
#                 itemFound = True
#                 return xxx

#         if not itemFound:
#             return None

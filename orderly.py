# from items import physical_type, mental_type, chemical_type
from game import pygame
import json
from random import shuffle
import random


class Orderly:

    def __init__(self, name, image, health, _type, items):

        self.health = health
        self.max_health = health
        self.type = _type
        self.items = items
        self.name = name

        self.image = pygame.image.load(image)


class OrderlyGenerator:

    def __init__(self):

        orderlys = json.load(open('entities.json'))["orderly"]

        self.orderlys = []

        for ordd in orderlys:

            xxx = Orderly(ordd["name"], ordd["image"], ordd["type"], [])
            self.orderlys.append(xxx)

    def getOrderly(self):

        ordd = self.orderlys[random.randint(0, len(self.orderlys)-1)]
        return ordd

    def getOrderlys(self, num=4):

        shuffle(self.orderlys)

        return self.orderlys[0:num]

    def getOrderlyByName(self, name):

        itemFound = False

        for xxx in self.orderlys:

            if xxx.name == name:
                itemFound = True
                return xxx

        if not itemFound:
            return None

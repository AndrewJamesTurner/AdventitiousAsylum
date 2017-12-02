import pygame
import random

#health max 1000
#sanity max 10, min 0

class Item:

    def __init__(self, name, image, damage, sanity, _type):

        self.name = name
        self.image = image
        self.damage = damage
        self.sanity = sanity
        self.type = _type

    @staticmethod
    def create_pillow():

        name = 'pillow'
        image = pygame.image.load("assets/astronaut_small.png")
        damage = 10
        sanity = 10
        _type = "physical"

        return Item(name, image, damage, sanity, _type)


class ItemGenerator:

    def __init__(self, image, damage, _type):

        self.items = [Item('pillow', 'assets/astronaut_small.png', 7, 10, 'physical'),
                      Item('spaceship', 'assets/astronaut_small.png', 300, 0, 'mental'),
                      Item('tug boat', 'assets/astronaut_small.png', 100, 2, 'mental')]

    def getItem(self):

        item = random.randint(0, len(self.items))
        return item

class ItemDescriptor:

    def __init__(self):

        self.descriptors = ['sparkly', 'singing', 'wet', 'slimy', 'fluffy', 'peppered', 'noisy', 'foiled', 'upsidedown',
                        'pert', 'loose', 'wobbly', 'troubling', 'wavy', 'erotic', 'alarming', 'dangerous', 'meddling',
                        'runny', 'wearisome', 'hopeful', 'sharp', 'whimsical']

    def getDescriptor(self):
        descriptor = random.randint(0, len(self.descriptors))
        return descriptor
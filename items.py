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

    def __init__(self):

        imagePath = 'assets/weapon-images'

        self.items = [Item('pillow', imagePath + '/astronaut_small.png', 7, 10, 'physical'),
                      Item('spaceship', imagePath + '/spaceship-side.png', 300, 0, 'mental'),
                      Item('tugboat', imagePath + '/astronaut_small.png', 100, 2, 'mental'),
                      Item('elephant', imagePath + '/astronaut_small.png', 150, 2, 'physical')]

    def getItem(self):

        item = random.randint(0, len(self.items))
        return item

    def getItemByName(self, name):

        itemFound = False

        for item in self.items:

            if item.name == name:
                itemFound = True
                return item

        if not itemFound:
            return None



class ItemDescriptor:

    def __init__(self):

        self.descriptors = ['sparkly', 'singing', 'wet', 'slimy', 'fluffy', 'peppered', 'noisy', 'foiled', 'upsidedown',
                        'pert', 'loose', 'wobbly', 'troubling', 'wavy', 'erotic', 'alarming', 'dangerous', 'meddling',
                        'runny', 'wearisome', 'hopeful', 'sharp', 'whimsical']

    def getDescriptor(self):
        descriptor = random.randint(0, len(self.descriptors))
        return descriptor
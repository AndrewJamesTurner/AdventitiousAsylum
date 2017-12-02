import pygame
import random

#health max 1000
#sanity max 10, min 0

physical_type = "physical"
mental_type = "mental"
chemical_type = "chemical"
none_type = "none"

class Item:

    def __init__(self, name, image, damage, sanity, _type):

        self.name = name
        self.image = image
        self.damage = damage
        self.sanity = sanity
        self.type = _type

class ItemGenerator:

    def __init__(self):

        imagePath = 'assets/items/weapons'

        self.items = [Item('pillow', imagePath + '/astronaut_small.png', 7, 10, physical_type),
                      Item('spaceship', imagePath + '/spaceship-side.png', 300, 0, mental_type),
                      Item('tugboat', imagePath + '/astronaut_small.png', 100, 2, mental_type),
                      Item('elephant', imagePath + '/astronaut_small.png', 150, 2, physical_type)]

    def getItem(self):

        item = random.randint(0, len(self.items)-1)
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
        descriptor = random.randint(0, len(self.descriptors)-1)
        return descriptor

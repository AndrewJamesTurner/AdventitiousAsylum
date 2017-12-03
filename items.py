import pygame
import random
from random import shuffle
import json
# health max 1000
# sanity max 10, min 0

physical_type = "physical"
mental_type = "mental"
chemical_type = "chemical"
none_type = "none"


class Item:

    def __init__(self, name, image, damage, sanity, _type):

        self.name = name
        self.image = pygame.image.load(image)
        self.damage = damage
        self.sanity = sanity
        self.type = _type


class ItemGenerator:

    def __init__(self):

        weapons = json.load(open('entities.json'))["weapon"]

        self.items = []

        for weapon in weapons:

            item = Item(weapon["name"], weapon["image"], weapon["damage"], weapon["sanity"], weapon["type"])
            self.items.append(item)


    def getItem(self):

        item = self.items[random.randint(0, len(self.items)-1)]
        return item

    def getItems(self, num=4):

        shuffle(self.items)

        return self.items[0:num]

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
                        'runny', 'wearisome', 'hopeful', 'sharp', 'whimsical', 'sassy', 'floral']

    def getDescriptor(self):

        descriptor = self.descriptors[random.randint(0, len(self.descriptors)-1)]

        if descriptor[0].lower() in ['a', 'e', 'i', 'o', 'u']:
            thing = 'an'
        else:
            thing = 'a'

        full_descriptor = thing + ' ' + descriptor

        return full_descriptor


class ItemEffectiveness():

    def __init__(self):

        self.high = ['effective', 'very effective', 'painful', 'super effective', 'exquisite', 'phenomenal',
                     'spectacular', 'a spectacle', 'fabulous', 'overwhelming', 'horrific', 'Brian Blessedesque']
        self.neutral = ['neutral', 'confusing', 'disturbing', 'unsettling', 'quite', 'whelming', 'hilarious', 'rather',
                        'amicable']
        self.low = ['not very effective', 'erotic', 'pitiful', 'pathetic', 'underwhelming', 'horrific']

    def get_rand_high_effective(self):
        effectiveness = self.high[random.randint(0, len(self.high)-1)]
        return effectiveness

    def get_rand_neutral_effective(self):
        effectiveness = self.neutral[random.randint(0, len(self.neutral)-1)]
        return effectiveness

    def get_rand_low_effective(self):
        effectiveness = self.low[random.randint(0, len(self.low)-1)]
        return effectiveness

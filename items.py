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
        self.image = pygame.image.load("assets/" + image)
        self.damage = damage
        self.sanity = sanity
        self.type = _type


class ItemGenerator:

    def __init__(self):

        weapons = json.load(open('entities.json'))["weapon"]

        self.items = []

        for weapon in weapons:

            item = Item(weapon["name"], weapon["image"], weapon["damage"], weapon["sanity"], weapon["type"])

            image_width = item.image.get_width()
            image_height = item.image.get_height()

            max_size = 80.0

            width_scale = max_size/image_width
            height_scale = max_size/image_height

            if width_scale < height_scale:
                item.image = pygame.transform.smoothscale(item.image, (int(width_scale * image_width), int(width_scale * image_height)))
            else:
                item.image = pygame.transform.smoothscale(item.image, (int(height_scale * image_width), int(height_scale * image_height)))

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

        self.descriptors = [
            'sparkly',
            'singing',
            'wet',
            'slimy',
            'fluffy',
            'peppered',
            'noisy',
            'foiled',
            'upsidedown',
            'pert',
            'loose',
            'wobbly',
            'troubling',
            'freshly shaven',
            'wavy',
            'erotic',
            'alarming',
            'dangerous',
            'meddling',
            'runny',
            'wearisome',
            'hopeful',
            'sharp',
            'whimsical',
            'sassy',
            'floral',
            'homoeroctic',
            'indifferent',
            'succulent',
            'subservient',
            'childish',
            'long-haired',
            'syphilis-ridden',
            'hopeful',
            'relaxed',
            'happy',
            'barbaric',
            'prehistoric',
            'soiled',
            'shitty',
            'warm',
            'moist',
            'old old',
            'fresh',
        ]

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

        self.high = [
            'effective',
            'very effective',
            'painful',
            'super effective',
            'exquisite',
            'phenomenal',
            'spectacular',
            'a spectacle',
            'fabulous',
            'overwhelming',
            'horrific',
            'Brian Blessedesque',
            'devastating',
            'limp educing',
            'violating',
            'traumatic',
            'distressing',
            'diarrhea inducing',
            'something to be remembered',
            'tear educing',
        ]

        self.neutral = [
            'neutral',
            'confusing',
            'disturbing',
            'unsettling',
            'quite',
            'whelming',
            'hilarious',
            'rather',
            'amicable',
            'fine',
            'OK',
            'passable',
            'a bit funny',
        ]

        self.low = [
            'not very effective',
            'erotic',
            'pitiful',
            'pathetic',
            'underwhelming',
            'horrific',
            'a poor move',
            'pretty dull',
            'tedious',
        ]

    def get_rand_high_effective(self):
        effectiveness = self.high[random.randint(0, len(self.high)-1)]
        return effectiveness

    def get_rand_neutral_effective(self):
        effectiveness = self.neutral[random.randint(0, len(self.neutral)-1)]
        return effectiveness

    def get_rand_low_effective(self):
        effectiveness = self.low[random.randint(0, len(self.low)-1)]
        return effectiveness

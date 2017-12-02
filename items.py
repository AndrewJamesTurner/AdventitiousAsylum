import pygame

class Item:

    def __init__(self, image, damage, _type):

        self.image = image
        self.damage = damage
        self.type = _type

    @staticmethod
    def create_pillow():

        image = pygame.image.load("assets/astronaut_small.png")
        damage = 9007
        _type = "???"

        return Item(image, damage, _type)

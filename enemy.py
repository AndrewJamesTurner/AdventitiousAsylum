from items import physical_type, mental_type, chemical_type
from game import pygame


class Enemy:

    def __init__(self, name, health, _type, items):

        self.health = health
        self.max_health = health
        self.type = _type
        self.items = items
        self.name = name

        self.image = pygame.image.load("assets/characters/spedec.png")

        if _type == physical_type:
            self.image = pygame.image.load("assets/characters/physical-orderly.png")

        if _type == mental_type:
            self.image = pygame.image.load("assets/characters/mental-orderly.png")

        if _type == chemical_type:
            self.image = pygame.image.load("assets/characters/chemical-orderly.png")

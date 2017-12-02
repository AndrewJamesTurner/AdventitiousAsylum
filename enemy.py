
class Enemy:

    def __init__(self, health, _type, items):

        self.health = health
        self.max_health = health
        self.type = _type
        self.items = items
        self.name = "enemy"

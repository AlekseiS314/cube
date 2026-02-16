

class ShieldSpell:
    def __init__(self,health_shield,count):
        self.health_shield = health_shield
        self.count = count

    def calc_hitbox(self):
        ...

    def draw_spell(self):
        ...

    def start(self):
        if self.calc_hitbox():
            self.draw_spell()
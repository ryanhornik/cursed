import random

from engine.models.entities import Entity


class Creature(Entity):
    def __init__(self, strength=1, constitution=1, dexterity=1, intelligence=1, perception=1, luck=1, level=1):
        self.strength = strength
        self.constitution = constitution
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.perception = perception
        self.luck = luck

        self.level = level
        self.health = constitution * 3

    @property
    def vision(self):
        """
        Returns the distance the creature is capable of seeing
        A creature with 0 perception is considered to be blind
        """
        if self.perception == 0:
            return 0
        return self.perception // 10 + 1

    @property
    def hearing_threshold(self):
        """
        Returns the minimum decibels the creature is capable of hearing
        A creature with 0 perception is considered to be deaf, sound degrades over distance as a square root
        """
        if self.perception == 0:
            return 0
        return self.perception // 5 + 1

    @property
    def attack_power(self):
        return self.strength // 3 + 1

    def receive_damage(self, attacker):
        """
        Determines how much damage the creature will receive from the attacker

        :type attacker: Creature
        :return: The amount of damage the creature received
        """
        attack = attacker.attack_power

        dealt = attack - (self.constitution // 3)
        self.health -= dealt
        return dealt

    def attack_dodged(self, attacker):
        """
        Determines if the Creature will dodge the attacker

        :type attacker: Creature
        :return: bool: Whether the creature dodged the attack
        """
        net_luck = self.luck - attacker.luck
        accuracy = attacker.dexterity * 0.1
        evasion = self.dexterity * 0.05
        dodge_chance = ((accuracy - evasion)/accuracy) * 1000

        return dodge_chance >= 0 and not random.randint(1000 - net_luck) > dodge_chance

import random

from engine.models.entities import Entity


class Creature(Entity):
    def __init__(self, strength=1, constitution=1, dexterity=1, intelligence=1, perception=1, luck=1, level=1):
        """
        Initializes a creature with the specified stats

        :param strength: The creatures strength
        :param constitution: The creatures constitution
        :param dexterity: The creatures dexterity
        :param intelligence: The creatures intelligence
        :param perception: The creatures perception
        :param luck: The creatures luck
        :param level: The creatures level
        :type strength: int
        :type constitution: int
        :type dexterity: int
        :type intelligence: int
        :type perception: int
        :type luck: int
        :type level: int

        :return: returns nothing
        """
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
        The distance the creature is capable of seeing
        A creature with 0 perception is considered to be blind

        :return: returns the distance the creature is capable of seeing
        :rtype: int
        """
        if self.perception == 0:
            return 0
        return self.perception // 10 + 1

    @property
    def hearing_threshold(self):
        """
        The minimum decibels the creature is capable of hearing
        A creature with 0 perception is considered to be deaf, sound degrades over distance as a square root

        :return: returns the minimum decibels the creature is capable of hearing
        :rtype: int
        """
        if self.perception == 0:
            return 0
        return self.perception // 5 + 1

    @property
    def attack_power(self):
        """
        The amount of damage the creature will do

        :return: returns the amount of damage the creature will do
        :rtype: int
        """
        return self.strength // 3 + 1

    def receive_damage(self, attacker):
        """
        Determines how much damage the creature will receive from the attacker

        :param attacker: the creature that is attacking this creature
        :type attacker: Creature
        :return: The amount of damage the creature received
        :rtype: int
        """
        attack = attacker.attack_power

        dealt = attack - (self.constitution // 3)
        self.health -= dealt
        return dealt

    def attack_dodged(self, attacker):
        """
        Determines if the Creature will dodge the attacker

        :param attacker: the creature that is attacking this creature
        :type attacker: Creature
        :return: Whether the creature dodged the attack
        :rtype: bool
        """
        net_luck = self.luck - attacker.luck
        accuracy = attacker.dexterity * 0.1
        evasion = self.dexterity * 0.05
        dodge_chance = ((accuracy - evasion)/accuracy) * 1000

        return dodge_chance >= 0 and not random.randint(1000 - net_luck) > dodge_chance

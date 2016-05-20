from functools import partial

from engine.models import World
from engine.models.entities import Creature

from engine.scenes import OptionsScene
from engine.scenes.components import NumericOption, SelectionOption


class CharacterCreationScene(OptionsScene):
    def draw_elements(self):
        super().draw_elements()
        self.show_instructions(['↑↓ - change option',
                                '←→ - change value      Remaining Points {}'.format(self.available_points)])
        self.show_options()

    def __init__(self, controller):
        super().__init__(controller=controller,
                         title="Choose Stats",
                         options=(
                             NumericOption('strength'),
                             NumericOption('constitution'),
                             NumericOption('dexterity'),
                             NumericOption('intelligence'),
                             NumericOption('perception'),
                             NumericOption('luck'),
                             SelectionOption("Confirm", action=self.confirm_character)
                         ))

    def loop(self):
        self.show_instructions(['↑↓ - change option',
                                '←→ - change value      Remaining Points {}'.format(self.available_points)])
        super().loop()

    @property
    def available_points(self):
        remaining = 21
        for opt in self.options:
            if isinstance(opt, NumericOption):
                remaining -= opt.value
        return remaining

    def validator(self, change):
        return (self.available_points - change) >= 0

    def confirm_character(self):
        from game.scenes import WorldScene
        if self.available_points == 0:
            player_char = Creature()

            for option in self.options:
                if isinstance(option, NumericOption):
                    setattr(player_char, option.name, option.value)

            world = World(5, 5)
            self.replace(partial(WorldScene, world=world, player=player_char))


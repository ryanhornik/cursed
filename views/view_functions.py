import curses
from functools import partial

from models import World
from models.entities import Creature
from views import OptionsView, BaseView
from views.options_view import SelectionOption, NumericOption


class SettingsView(OptionsView):
    def __init__(self, *args, **kwargs):
        super().__init__('Settings',
                         options=(
                             SelectionOption('Do Nothing', lambda: None),
                             SelectionOption('Back', self.pop),
                         ), *args, **kwargs)


class MainMenuView(OptionsView):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Main Menu",
                         options=(
                             SelectionOption('New Game', action=partial(self.push, CharacterCreationView)),
                             SelectionOption('Load Game', action=self.flash_and_beep),
                             SelectionOption('Settings', action=partial(self.push, SettingsView)),
                             SelectionOption('Exit', action=self.pop)
                         ), *args, **kwargs)


class GameView(BaseView):
    def show(self):
        super().show()
        curses.nonl()
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        self.clear_input()

    def clear_input(self):
        self.show_instructions([' ' * (self.screen_width - 2), ' ' * (self.screen_width - 2)])
        self.main_input.move(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(title="Dungeon", *args, **kwargs)
        self.world = kwargs['world']
        self.player = kwargs['player']

    def loop(self):
        self.get_command()

    def get_command(self):
        line = self.main_input.getstr().decode('utf-8').lower()
        self.clear_input()

        if line == 'exit':
            self.pop()


class CharacterCreationView(OptionsView):
    def show(self):
        super().show()
        self.show_instructions(['↑↓ - change option',
                                '←→ - change value      Remaining Points {}'.format(self.available_points)])
        self.show_options()

    def __init__(self, *args, **kwargs):
        super().__init__(title="Choose Stats",
                         options=(
                             NumericOption('strength'),
                             NumericOption('constitution'),
                             NumericOption('dexterity'),
                             NumericOption('intelligence'),
                             NumericOption('perception'),
                             NumericOption('luck'),
                             SelectionOption("Confirm", action=self.confirm_character)
                         ), *args, **kwargs)

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
        if self.available_points == 0:
            player_char = Creature()

            for option in self.options:
                if isinstance(option, NumericOption):
                    setattr(player_char, option.name, option.value)

            world = World(5, 5)
            self.replace(partial(GameView, world=world, player=player_char))


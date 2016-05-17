from functools import partial

from views import OptionsView
from views.options_view import Option, SelectionOption, NumericOption


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
            self.controller.pop()


from functools import partial

from views import OptionsView
from views.options_view import Option


class SettingsView(OptionsView):
    def __init__(self, *args, **kwargs):
        super().__init__('Settings',
                         options=(
                             Option('Do Nothing', lambda: None),
                             Option('Back', self.pop),
                         ), *args, **kwargs)


class MainMenuView(OptionsView):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Main Menu",
                         options=(
                             Option('New Game', action=self.flash_and_beep),
                             Option('Load Game', action=self.flash_and_beep),
                             Option('Settings', action=partial(self.push, SettingsView)),
                             Option('Exit', action=self.pop)
                         ), *args, **kwargs)

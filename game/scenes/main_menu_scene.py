from functools import partial

from engine.scenes import OptionsScene
from engine.scenes.components import SelectionOption


class MainMenuScene(OptionsScene):
    def __init__(self, *args, **kwargs):
        from game.scenes import CharacterCreationScene, SettingsScene
        super().__init__(title="Main Menu",
                         options=(
                             SelectionOption('New Game', action=partial(self.push, CharacterCreationScene)),
                             SelectionOption('Load Game', action=self.flash_and_beep),
                             SelectionOption('Settings', action=partial(self.push, SettingsScene)),
                             SelectionOption('Exit', action=self.pop)
                         ), *args, **kwargs)

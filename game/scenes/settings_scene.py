from engine.scenes import OptionsScene
from engine.scenes.components import SelectionOption


class SettingsScene(OptionsScene):
    def __init__(self, *args, **kwargs):
        super().__init__('Settings',
                         options=(
                             SelectionOption('Do Nothing', lambda: None),
                             SelectionOption('Back', self.pop),
                         ), *args, **kwargs)

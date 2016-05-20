from engine.scenes import OptionsScene
from engine.scenes.components import SelectionOption


class SettingsScene(OptionsScene):
    def __init__(self, controller):
        super().__init__(controller=controller,
                         title='Settings',
                         options=(
                             SelectionOption('Do Nothing', lambda: None),
                             SelectionOption('Back', self.pop),
                         ))

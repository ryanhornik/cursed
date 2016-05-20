import curses

from engine.scenes import BaseScene


class WorldScene(BaseScene):
    def __init__(self, controller, world, player):
        super().__init__(controller=controller, title="Dungeon")
        self.world = world
        self.player = player

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

    def loop(self):
        super().loop()
        self.get_command()

    def get_command(self):
        line = self.main_input.getstr().decode('utf-8').lower()
        self.clear_input()

        if line == 'exit':
            self.pop()

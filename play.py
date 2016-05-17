from time import sleep

from models import World
from models.entities import Creature
import curses
from functools import partial
from random import randrange


class View(object):
    def __init__(self):
        self.screen = curses.initscr()

        curses.noecho()  # don't echo the keys on the screen
        curses.cbreak()
        curses.curs_set(0)  # don't show cursor.

        curses.start_color()
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.screen.keypad(True)

        self.screen.erase()
        self.screen_height, self.screen_width = self.screen.getmaxyx()

        self.title_bar = self.screen.subwin(3, self.screen_width, 0, 0)

        self.main_output = self.screen.subwin(self.screen_height - 7, self.screen_width, 3, 0)
        self.main_input = self.screen.subwin(4, self.screen_width, self.screen_height - 4, 0)

        self.options = []
        self.selected = None

    def set_title(self, title):
        self.title_bar.erase()
        self.title_bar.box()
        self.title_bar.addstr(1, 0, title.center(self.screen_width, ' '))
        self.refresh()

    def refresh(self):
        self.screen.refresh()
        self.title_bar.refresh()
        self.main_output.refresh()
        self.main_input.refresh()

    def show_options(self, options):
        self.main_output.erase()

        self.options = []
        for i, opt in enumerate(options):
            self.options.append(opt[0])
            self.main_output.addstr(i + 1, 4, opt[1])
        self.set_selected(0)
        self.refresh()

    def set_selected(self, idx):
        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, 0, "--> " if i == idx else "    ")
        self.selected = idx
        self.refresh()

    def show_instructions(self, instructions):
        self.main_input.erase()
        self.main_input.box()
        for i, inst in enumerate(instructions):
            self.main_input.addstr(i + 1, 2, inst)
        self.refresh()

    def cleanup(self):
        curses.endwin()

    def update_selection(self):
        key = self.screen.getch()

        new_selection = self.selected
        if key == curses.KEY_UP:
            new_selection -= 1
            if new_selection <= -1:
                new_selection = len(self.options) - 1
        elif key == curses.KEY_DOWN:
            new_selection += 1
            if new_selection >= len(self.options):
                new_selection = 0
        elif key == curses.KEY_ENTER or key == 10:
            self.options[self.selected]()

        if new_selection != self.selected:
            self.set_selected(new_selection)

    def flash_and_beep(self):
        original = self.screen.getbkgd()
        self.screen.bkgd(curses.color_pair(2) | curses.A_NORMAL)
        self.refresh()
        sleep(0.15)
        self.screen.bkgd(original)
        self.refresh()


def cleanup_and_exit(view):
    view.cleanup()
    exit()


def main():
    view = View()
    view.set_title("Main Menu")
    view.show_options([(view.flash_and_beep, 'Fuck'), (partial(cleanup_and_exit, view), 'Exit')])
    view.show_instructions(['↑↓ - change option', 'Enter↵ - confirm'])

    try:
        while True:
            view.update_selection()
    finally:
        view.cleanup()

if __name__ == "__main__":
    main()

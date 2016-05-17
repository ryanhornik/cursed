import curses
import threading
from time import sleep


class BaseView(object):
    def show(self):
        self.screen = curses.initscr()

        curses.noecho()  # don't echo the keys on the screen
        curses.cbreak()
        curses.curs_set(0)  # don't show cursor.

        self.screen.keypad(True)

        self.screen.erase()
        self.screen_height, self.screen_width = self.screen.getmaxyx()

        self.title_bar = self.screen.subwin(3, self.screen_width, 0, 0)

        self.main_output = self.screen.subwin(self.screen_height - 7, self.screen_width, 3, 0)
        self.main_input = self.screen.subwin(4, self.screen_width, self.screen_height - 4, 0)

        if self.title:
            self.set_title(self.title)

    def __init__(self, title=None, *args, **kwargs):
        self.title = title
        self.threads = []

    def set_title(self, title):
        self.title = title
        self.title_bar.erase()
        self.title_bar.box()
        self.title_bar.addstr(1, 0, title.center(self.screen_width, ' '))
        self.refresh()

    def refresh(self):
        self.screen.refresh()
        self.title_bar.refresh()
        self.main_output.refresh()
        self.main_input.refresh()

    def show_instructions(self, instructions):
        self.main_input.erase()
        self.main_input.box()
        for i, inst in enumerate(instructions):
            self.main_input.addstr(i + 1, 2, inst)
        self.refresh()

    def cleanup(self):
        for t in self.threads:
            t.join()
        curses.endwin()

    def flash_and_beep(self):
        old_title = self.title
        self.set_title("FFFFFFFUUUUUUUUUUUUCK")
        reset_title = threading.Timer(3, self.set_title, args=(old_title,))
        self.threads.append(reset_title)
        reset_title.start()

    def loop(self):
        sleep(0.1)

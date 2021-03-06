import curses
import threading
from engine.controllers import SceneControllerDelegate


class BaseScene(SceneControllerDelegate):
    def show(self):
        """
        Creates the screen and draws elements

        :return: returns nothing
        """
        self.screen = curses.initscr()

        curses.noecho()  # don't echo the keys on the screen
        curses.cbreak()
        curses.curs_set(0)  # don't show cursor.

        self.draw_elements()

    def draw_elements(self):
        """
        Draws all the elements on the screen
        Should be overridden by subclasses, and subclasses should make a call to super().draw_elements()

        :return: returns nothing
        """
        self.screen.keypad(True)

        self.screen.erase()
        self.screen_height, self.screen_width = self.screen.getmaxyx()

        self.title_bar = self.screen.subwin(3, self.screen_width, 0, 0)

        self.main_output = self.screen.subwin(self.screen_height - 7, self.screen_width, 3, 0)
        self.main_input = self.screen.subwin(4, self.screen_width, self.screen_height - 4, 0)

        if self.title:
            self.set_title(self.title)

    def __init__(self, controller, title):
        """
        Creates a new scene object

        :param title: the title to be displayed at the top of the screen
        :type title: str
        :param controller: the scene controller that instantiated this object
        :type controller: SceneController

        :return: returns nothing
        """
        self.screen = None
        self.screen_height = None
        self.screen_width = None
        self.title_bar = None

        self.main_output = None
        self.main_input = None

        self.controller = controller
        self.title = title
        self.nonvolatile_threads = []

    def set_title(self, title):
        """
        Sets the title displayed at the top of the screen, and displays it

        :param title: the title to be displayed at the top of the screen
        :type title: str
        :return: returns nothing
        """
        self.title = title
        self.title_bar.erase()
        self.title_bar.box()
        self.title_bar.addstr(1, 0, title.center(self.screen_width, ' '))
        self.refresh()

    def refresh(self):
        """
        Refreshes the screen and each sub-window
        Should be overridden and extended by subclasses that add new windows

        :return: returns nothing
        """
        self.screen.refresh()
        self.title_bar.refresh()
        self.main_output.refresh()
        self.main_input.refresh()

    def show_instructions(self, instructions):
        """
        Sets the instructions displayed at the bottom of the screen, and displays them

        :param instructions: The instructions to display, one list entry per line
        :type instructions: list[str]
        :return: returns nothing
        """
        self.main_input.erase()
        self.main_input.box()
        for i, inst in enumerate(instructions):
            self.main_input.addstr(i + 1, 2, inst)
        self.refresh()

    def cleanup(self):
        """
        Removes all this instance's information from the screen, and cleans up resources
        Should be called anytime this Scene will be replaced

        :return: returns nothing
        """
        for t in self.nonvolatile_threads:
            t.cancel()
            t.join()
        self.screen.erase()
        self.main_output.erase()
        self.title_bar.erase()
        self.main_input.erase()
        curses.endwin()

    def flash_and_beep(self):
        old_title = self.title
        self.set_title("I'm afraid I can't let you do that...")
        reset_title = threading.Timer(3, self.set_title, args=(old_title,))
        self.nonvolatile_threads.append(reset_title)
        reset_title.start()

    def resize(self):
        """
        Updates the screen to handle a resizing of the terminal window
        May cause an error if the window becomes too small

        :return: returns nothing
        """
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        self.screen.erase()
        curses.resizeterm(self.screen_height, self.screen_width)
        self.draw_elements()
        self.screen.refresh()

    def loop(self):
        """
        Receives input from the user then responds
        Should be extended by subclasses to handle different input types

        :return: returns nothing
        """
        if curses.is_term_resized(self.screen_height, self.screen_width):
            self.resize()

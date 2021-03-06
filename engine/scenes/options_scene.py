import curses

from engine.scenes import BaseScene


class OptionsScene(BaseScene):
    def validator(self, val):
        return True

    def draw_elements(self):
        super().draw_elements()
        self.show_instructions(['↑↓ - change option', 'Enter↵ - confirm'])
        self.show_options()

    def __init__(self, controller, title, options=None):
        """
        Creates a new options scene object

        :param controller: the scene controller that instantiated this object
        :type controller: SceneController
        :param title: the title to be displayed at the top of the screen
        :type title: str
        :param options: the options to be used shown in the scene
        :type options: list(options)

        :return: returns nothing
        """
        super().__init__(controller, title)

        self.options = []
        self.selected = None
        if options:
            self.set_options(options)

    def set_options(self, options):
        """
        Sets the options for the scene

        :param options: the options to be used shown in the scene
        :type options: list(options)

        :return: returns nothing
        """

        self.options = []
        for opt in options:
            self.options.append(opt)
        self.selected = 0

    def show_options(self):
        """
        Displays the options for the scene

        :return: returns nothing
        """
        self.main_output.erase()
        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, len(opt.selected_text), opt.name)
        self.show_selected()
        self.refresh()

    def show_selected(self, idx=None):
        """
        Displays the appropriate symbols near the selected and unselected options

        :param idx: the index of the selected option if any
        :type idx: int
        :return: returns nothing
        """
        self.selected = self.selected if idx is None else idx

        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, 0, opt.selected_text if i == self.selected else opt.unselected_text)

        self.refresh()

    def update_selection(self):
        """
        Updates which option is selected based on a keypress
        Also forwards non up/down arrow keys to the currently selected option

        :return: returns nothing
        """
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
        else:
            self.options[self.selected].process_keypress(self, key)

        if new_selection != self.selected:
            self.show_selected(new_selection)

    def loop(self):
        super().loop()
        self.update_selection()

import curses

from engine.scenes import BaseScene

curses.is_enter = lambda key: key == curses.KEY_ENTER or key == 10 or key == 13


class OptionsScene(BaseScene):
    def validator(self, val):
        return True

    def show(self):
        super().show()
        self.show_instructions(['↑↓ - change option', 'Enter↵ - confirm'])
        self.show_options()

    def __init__(self, title=None, options=None, *args, **kwargs):
        super().__init__(title, *args, **kwargs)

        self.options = []
        self.selected = None
        if options:
            self.set_options(options)

    def set_options(self, options):
        self.options = []
        for opt in options:
            self.options.append(opt)
        self.selected = 0

    def show_options(self):
        self.main_output.erase()
        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, len(opt.selected_text), opt.name)
        self.show_selected()
        self.refresh()

    def show_selected(self, idx=None):
        self.selected = self.selected if idx is None else idx

        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, 0, opt.selected_text if i == self.selected else opt.unselected_text)

        self.refresh()

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
        else:
            self.options[self.selected].process_key(self, key)

        if new_selection != self.selected:
            self.show_selected(new_selection)

    def loop(self):
        self.update_selection()

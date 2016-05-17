import curses
from views import BaseView


class Option(object):
    ACTION_TYPE = 0
    TRANSITION_TYPE = 1

    def __init__(self, name, action=None, transition=None):
        self.name = name
        if action:
            self.option_type = Option.ACTION_TYPE
            self.action = action
        elif transition:
            self.option_type = Option.TRANSITION_TYPE
            self.transition = transition
        else:
            raise ValueError("Option requires an action or a transition")

    def do(self, source_view):
        if self.option_type == Option.ACTION_TYPE:
            self.action()
        elif self.option_type == Option.TRANSITION_TYPE:
            source_view.transition(self.transition)


class OptionsView(BaseView):
    ARROW = "--> "

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
            self.main_output.addstr(i + 1, len(OptionsView.ARROW), opt.name)
        self.show_selected()
        self.refresh()

    def show_selected(self, idx=None):
        self.selected = self.selected if idx is None else idx

        for i, opt in enumerate(self.options):
            self.main_output.addstr(i + 1, 0, OptionsView.ARROW if i == self.selected else ' ' * len(OptionsView.ARROW))

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
        elif key == curses.KEY_ENTER or key == 10:
            self.options[self.selected].do(source_view=self)

        if new_selection != self.selected:
            self.show_selected(new_selection)

    def loop(self):
        self.update_selection()

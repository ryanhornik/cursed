import curses
from views import BaseView


curses.is_enter = lambda key: key == curses.KEY_ENTER or key == 10 or key == 13


class Option(object):
    @property
    def selected_text(self):
        return " --> "

    @property
    def unselected_text(self):
        return ' ' * len(self.selected_text)

    def __init__(self, name):
        self.name = name

    def process_key(self, source_view, key):
        raise NotImplementedError("Use a concrete subclass of Option")


class NumericOption(Option):
    @property
    def selected_text(self):
        return ">{}<".format(self.value).center(6)

    @property
    def unselected_text(self):
        return " {} ".format(self.value).center(6)

    def __init__(self, name, initial=1, min_value=1, max_value=999):
        super().__init__(name)
        assert min_value <= initial <= max_value

        self.min_value = min_value
        self.max_value = max_value
        self.value = initial

    def process_key(self, source_view, key):
        if key == curses.KEY_LEFT:
            if self.value > self.min_value and source_view.validator(-1):
                self.value -= 1
                source_view.show_selected()
                source_view.refresh()
        elif key == curses.KEY_RIGHT:
            if self.value < self.max_value and source_view.validator(1):
                self.value += 1
                source_view.show_selected()
                source_view.refresh()


class SelectionOption(Option):
    ACTION_TYPE = 0
    TRANSITION_TYPE = 1

    def __init__(self, name, action=None, transition=None):
        super().__init__(name)

        if action:
            self.option_type = SelectionOption.ACTION_TYPE
            self.action = action
        elif transition:
            self.option_type = SelectionOption.TRANSITION_TYPE
            self.transition = transition
        else:
            raise ValueError("Option requires an action or a transition")

    def process_key(self, source_view, key):
        if curses.is_enter(key):
            self.do(source_view)

    def do(self, source_view):
        if self.option_type == SelectionOption.ACTION_TYPE:
            self.action()
        elif self.option_type == SelectionOption.TRANSITION_TYPE:
            source_view.transition(self.transition)


class OptionsView(BaseView):
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

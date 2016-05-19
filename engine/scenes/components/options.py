import curses


class Option(object):
    @property
    def selected_text(self):
        return " --> "

    @property
    def unselected_text(self):
        return ' ' * len(self.selected_text)

    def __init__(self, name):
        self.name = name

    def process_key(self, source_scene, key):
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

    def process_key(self, source_scene, key):
        if key == curses.KEY_LEFT:
            if self.value > self.min_value and source_scene.validator(-1):
                self.value -= 1
                source_scene.show_selected()
                source_scene.refresh()
        elif key == curses.KEY_RIGHT:
            if self.value < self.max_value and source_scene.validator(1):
                self.value += 1
                source_scene.show_selected()
                source_scene.refresh()


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

    def process_key(self, source_scene, key):
        if curses.is_enter(key):
            self.do(source_scene)

    def do(self, source_scene):
        if self.option_type == SelectionOption.ACTION_TYPE:
            self.action()
        elif self.option_type == SelectionOption.TRANSITION_TYPE:
            source_scene.transition(self.transition)
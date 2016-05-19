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

    def __init__(self, name, action=None):
        super().__init__(name)
        self.action = action

    def process_key(self, source_scene, key):
        if curses.is_enter(key):
            self.action()


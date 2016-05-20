import curses


class Option(object):
    """
    Represents o single option for a OptionScene
    """

    @property
    def selected_text(self):
        """
        The text to display when the options is currently selected
        :return: returns the text to display when the options is currently selected
        :rtype: str
        """
        return " --> "

    @property
    def unselected_text(self):
        """
        The text to display when the options is not selected
        :return: returns the text to display when the options is not selected
        :rtype: str
        """
        return ' ' * len(self.selected_text)

    def __init__(self, name):
        """
        Creates a new option object

        :param name: the text to display to represent the option
        :type name: str
        :return: returns nothing
        """
        self.name = name

    def process_keypress(self, source_scene, key):
        """
        Performs an action based on a keypress
        Must be overridden by subclasses

        :param source_scene: the scene containing the option
        :type source_scene: BaseScene
        :param key: the value of the key that was pressed (cannot be KEY_UP or KEY_DOWN)
        :type key: int
        :return: returns nothing
        """
        raise NotImplementedError("Use a concrete subclass of Option")


class NumericOption(Option):
    """
    Represents o single option for a OptionScene
    This allows a number to be set
    """

    @property
    def selected_text(self):
        return ">{}<".format(self.value).center(6)

    @property
    def unselected_text(self):
        return " {} ".format(self.value).center(6)

    def __init__(self, name, initial=1, min_value=1, max_value=999):
        """
        Creates a new numeric option object

        :param name: the text to display to represent the option
        :type name: str
        :param initial: the initial numeric value of the option
        :type initial: int
        :param min_value: the minimum numeric value of the option
        :type min_value: int
        :param max_value: the maximum numeric value of the option
        :type max_value: int
        :return: returns nothing
        """
        super().__init__(name)
        assert min_value <= initial <= max_value

        self.min_value = min_value
        self.max_value = max_value
        self.value = initial

    def process_keypress(self, source_scene, key):
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
    """
    Represents o single option for a OptionScene
    This allows an action to be performed on selection
    """
    ACTION_TYPE = 0
    TRANSITION_TYPE = 1

    def __init__(self, name, action=None):
        """
        Creates a new selection option object

        :param name: the text to display to represent the option
        :type name: str
        :param action: the action to be performed if the option is selected
        :type action: callable
        :return: returns nothing
        """
        super().__init__(name)
        self.action = action

    def process_keypress(self, source_scene, key):
        if curses.is_enter(key):
            self.action()


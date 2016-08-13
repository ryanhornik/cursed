import traceback


class SceneController(object):
    """
    Handles transitions between classes, and dictates the main loop
    """

    def __init__(self, initial=None):
        """
        Constructs a new SceneController object

        :param initial: The first scene for the controller
        :type initial: a class subclassing BaseScene
        :return: returns nothing
        """
        self.current_scene = None
        self.scene_stack = []
        if initial:
            self.push(initial)

    @property
    def top(self):
        """
        Retrieves the current top of the scene stack

        :return: returns the current top of the scene stack
        :rtype: a class subclassing BaseScene
        """
        return self.scene_stack[-1]

    def push(self, scene):
        """
        Adds a new scene to the stack and displays it

        :param scene: The scene to show next
        :type scene: a class subclassing BaseScene
        :return: returns nothing
        """
        if len(self.scene_stack) > 0:
            self.current_scene.cleanup()

        self.scene_stack.append(scene)

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

    def pop(self):
        """
        Removes the scene from the top of the stack, and displays the one below it

        :return: returns the item removed from the stack
        :rtype: a class subclassing BaseScene
        """
        popped = self.scene_stack.pop()
        self.current_scene.cleanup()

        if len(self.scene_stack) == 0:
            self.exit()
            return

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

        return popped

    def replace(self, scene):
        """
        Replaces the scene at the top of the stack with a new scene. Hides the previous top, and shows the new one

        :param scene: The scene to show next
        :type scene: a class subclassing BaseScene
        :return: returns the item removed from the stack
        :rtype: a class subclassing BaseScene
        """
        if len(self.scene_stack) > 0:
            self.current_scene.cleanup()

        popped = self.scene_stack.pop()
        self.scene_stack.append(scene)

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

        return popped

    def cleanup(self):
        """
        Removes all remaining items from the stack

        :return: returns nothing
        """
        while len(self.scene_stack) > 0:
            self.pop()

    def loop(self):
        """
        Performs the next step in the loop, relative to the current scene

        :return: returns nothing
        """
        self.current_scene.loop()

    def start(self):
        """
        Starts and manages the main game loop
        :return: returns nothing
        """
        try:
            while True:
                self.loop()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
        finally:
            self.cleanup()

    def exit(self, *args, **kwargs):
        """
        Ends the program execution when the bottom of the stack is reached
        Simply forwards to builtin exit command (makes it testing this functionality simple)
        :return: returns nothing
        """
        exit(args, kwargs)

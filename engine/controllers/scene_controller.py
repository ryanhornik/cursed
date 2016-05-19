import traceback
from typing import Callable, Optional, List
import engine.scenes


class SceneController(object):
    """
    Handles transitions between classes, and dictates the main loop

    :cvar current_scene: An instance of the scene type at the top of the stack
    :cvar scene_stack: The current stack of scenes
    """

    current_scene = None  # type: Optional['engine.scenes.BaseScene']
    scene_stack = None  # type: List[Callable[..., 'engine.scenes.BaseScene']]

    def __init__(self, initial: Optional[Callable[..., 'engine.scenes.BaseScene']]=None) -> None:
        """
        Constructs a new SceneController object

        :param initial: The first scene for the controller
        :return: nothing
        """

        self.scene_stack = []

        if initial:
            self.push(initial)

    @property
    def top(self):
        return self.scene_stack[-1]

    def push(self, scene):
        if len(self.scene_stack) > 0:
            self.current_scene.cleanup()

        self.scene_stack.append(scene)

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

    def pop(self):
        popped = self.scene_stack.pop()
        self.current_scene.cleanup()

        if len(self.scene_stack) == 0:
            exit()

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

        return popped

    def replace(self, scene):
        if len(self.scene_stack) > 0:
            self.current_scene.cleanup()

        popped = self.scene_stack.pop()
        self.scene_stack.append(scene)

        self.current_scene = self.top(controller=self)
        self.current_scene.show()

        return popped

    def cleanup(self):
        while len(self.scene_stack) > 0:
            self.pop()

    def loop(self):
        self.current_scene.loop()

    def start(self):
        try:
            while True:
                self.loop()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
        finally:
            self.cleanup()


class SceneControllerDelegate(object):
    def pop(self):
        self.controller.pop()

    def push(self, scene):
        self.controller.push(scene)

    def replace(self, scene):
        self.controller.replace(scene)

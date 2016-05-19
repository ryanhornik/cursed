import traceback


class SceneController(object):
    def __init__(self, initial=None):
        self.scene_stack = []
        if initial:
            self.push(initial)

    current = None

    @property
    def top(self):
        return self.scene_stack[-1]

    def push(self, scene):
        if len(self.scene_stack) > 0:
            self.current.cleanup()

        self.scene_stack.append(scene)

        self.current = self.top(controller=self)
        self.current.show()

    def pop(self):
        popped = self.scene_stack.pop()
        self.current.cleanup()

        if len(self.scene_stack) == 0:
            exit()

        self.current = self.top(controller=self)
        self.current.show()

        return popped

    def replace(self, scene):
        if len(self.scene_stack) > 0:
            self.current.cleanup()

        popped = self.scene_stack.pop()
        self.scene_stack.append(scene)

        self.current = self.top(controller=self)
        self.current.show()

        return popped

    def cleanup(self):
        while len(self.scene_stack) > 0:
            self.pop()

    def loop(self):
        self.current.loop()

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

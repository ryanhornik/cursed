from engine.controllers import SceneController


class SceneControllerDelegate(object):
    """
    Delegates the transition functions of SceneController to SceneControllerDelegate's subclasses
    The subclassses must define controller
    """

    def pop(self):
        return self.controller.pop()
    pop.__doc__ = SceneController.pop.__doc__

    def push(self, scene):
        self.controller.push(scene)
    push.__doc__ = SceneController.push.__doc__

    def replace(self, scene):
        self.controller.replace(scene)
    replace.__doc__ = SceneController.replace.__doc__

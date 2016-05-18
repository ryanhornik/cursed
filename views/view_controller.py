from time import time


class ViewController(object):
    def __init__(self, initial=None):
        self.view_stack = []
        if initial:
            self.push(initial)

    current = None

    @property
    def top(self):
        return self.view_stack[-1]

    def push(self, view):
        if len(self.view_stack) > 0:
            self.current.cleanup()

        self.view_stack.append(view)

        self.current = self.top(controller=self)
        self.current.show()

    def pop(self):
        popped = self.view_stack.pop()
        self.current.cleanup()

        if len(self.view_stack) == 0:
            exit()

        self.current = self.top(controller=self)
        self.current.show()

        return popped

    def replace(self, view):
        if len(self.view_stack) > 0:
            self.current.cleanup()

        popped = self.view_stack.pop()
        self.view_stack.append(view)

        self.current = self.top(controller=self)
        self.current.show()

        return popped

    def cleanup(self):
        while len(self.view_stack) > 0:
            self.pop()


class ViewController(object):
    def __init__(self, initial=None):
        self.view_stack = []
        if initial:
            self.push(initial)

    @property
    def current(self):
        return self.view_stack[-1]

    def push(self, view):
        if len(self.view_stack) > 0:
            self.current.cleanup()
        self.view_stack.append(view)
        self.current.show()

    def pop(self):
        popped = self.view_stack.pop()
        popped.cleanup()
        if len(self.view_stack) == 0:
            return popped
        self.current.show()
        return popped

    def cleanup(self):
        while len(self.view_stack) > 0:
            self.pop()

import argparse

command_controller = None


class CommandController(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(*args, **kwargs)

    def register_command(self, command, action):
        self.parser.add_subparsers()

    def set_program_name(self, name):
        self.parser.prog = name



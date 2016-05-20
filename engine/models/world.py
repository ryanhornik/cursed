from random import random

from engine.models.entities import Entity


class World(object):
    __grid = None

    class AlreadyOccupiedException(BaseException):
        def __init__(self, room, key):
            super().__init__("The selected cell ({},{}) is already occupied by {}".format(key[0], key[1], room[key]))

    class FullRoomException(BaseException):
        def __init__(self):
            super().__init__("The room is full, can't add anything")

    def __init__(self, width, height):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__length = width * height
        self.__grid = [[None] * width] * height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def place_random(self, entity):
        empty = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self[x, y] is None:
                    empty.append((x, y))
        if len(empty) == 0:
            raise World.FullRoomException()
        self[random.choice(empty)] = entity

    def __getitem__(self, key):
        return self.__grid[key[0]][key[1]]

    def __setitem__(self, key, value):
        if value is None:
            self.__grid[key[0]][key[1]] = value
            return

        if self[key]:
            raise World.AlreadyOccupiedException(self, key)

        if not isinstance(value, Entity):
            raise TypeError("Value must be an Entity or None")

        self.__grid[key[0]][key[1]] = value

    def __len__(self):
        return self.__length

    def __iter__(self):
        for row in self.__grid:
            for item in row:
                yield item

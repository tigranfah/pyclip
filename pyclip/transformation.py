import copy


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, _pos):
        pos = copy.deepcopy(self)
        pos.x = self.x + _pos.x
        pos.y = self.y + _pos.y
        return pos

    def __sub__(self, _pos):
        pos = copy.deepcopy(self)
        pos.x = self.x - _pos.x
        pos.y = self.y - _pos.y
        return pos

    def __str__(self):
        return "Position({}, {})".format(self.x, self.y)
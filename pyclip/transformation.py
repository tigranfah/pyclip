import copy

import error_handler


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


class Rotation(Position):

    def __str__(self):
        return "Rotation({}, {})".format(self.x, self.y)


class Scale(Position):

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __add__(self, _scale):
        scale = copy.deepcopy(self)
        scale.w = self.w + _scale.w
        scale.h = self.h + _scale.h
        return scale

    def __sub__(self, _scale):
        scale = copy.deepcopy(self)
        scale.w = self.w - _scale.w
        scale.h = self.h - _scale.h
        return scale

    def __str__(self):
        return "Scale({}, {})".format(self.w, self.h)


class Transformation:

    def __init__(self, pos, scale, rot):
        for value in [pos, scale, rot]:
            if not error_handler.is_of_type(value, tuple):
                raise error_handler.ValueError("{} must of type {}, not of type {}".format(value, tuple, type(value)))
        
        self._pos = Position(pos[0], pos[1])
        self._scale = Scale(scale[0], scale[1])
        self._rot = Rotation(rot[0], rot[1])

    @property
    def pos(self):
        return self._pos

    @property
    def scale(self):
        return self._scale

    @property
    def rot(self):
        return self._rot

    @pos.setter
    def pos(self, pos):
        self._pos.x = pos[0]
        self._pos.y = pos[1]

    @scale.setter
    def scale(self, scale):
        self._scale.w = scale[0]
        self._scale.h = scale[1]

    @rot.setter
    def rot(self, rot):
        self._rot.x = rot[0]
        self._rot.y = rot[1]
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


class Scale:

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


class Rotation:

    def __init__(self, angle):
        self.angle = angle

    def __add__(self, _rot):
        rot = copy.deepcopy(self)
        rot.angle = self.angle + _rot.angle
        return rot

    def __sub__(self, _rot):
        rot = copy.deepcopy(self)
        rot.angle = self.angle - _rot.angle
        return rot

    def __str__(self):
        return "Rotation({})".format(self.angle)

 
class Transformation:

    def __init__(self, pos, scale, rot):
        for value in [pos, scale]:
            if not error_handler.is_of_type(value, tuple):
                raise error_handler.ValueError("{} must of type {}, not of type {}".format(value, tuple, type(value)))
        
        self._pos = Position(pos[0], pos[1])
        self._scale = Scale(scale[0], scale[1])
        self._rot = Rotation(rot)

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
    def rot(self, angle):
        self._rot.angle = angle
import cv2
import numpy as np

from clip import Position


class MovieBase:

    def __init__(self, title, width, height, fps):
        self._title = title
        self._width = width
        self._height = height
        self._fps = fps

    @property
    def title(self):
        return self._title

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps


class Movie(MovieBase):

    def __init__(self, title, width, height, fps):
        MovieBase.__init__(self, title, width, height, fps)
        self._clip_sequence = []

    def __get_position_by_pos_type(self, clip):
        if clip.info.position:
            return clip.info.position
        return {
            "" : Position(0, 0),
            "center" : Position(
                (self._width - clip.info.width) / 2,
                (self._height - clip.info.height) / 2
            ),
            "left" : Position(0, (self._height - clip.info.height) / 2),
            "top" : Position((self._width - clip.info.width) / 2, 0),
            "right" : Position(
                self._width - clip.info.width,
                (self._height - clip.info.height) / 2
            ),
            "bottom" : Position(
                (self._width - clip.info.width) / 2,
                self._height - clip.info.height
            ),
            "top-left" : Position(0, 0),
            "top-right" : Position(self._width - clip.info.width, 0),
            "bottom-left" : Position(0, self._height - clip.info.height),
            "bottom-right" : Position(self._width - clip.info.width, self._height - clip.info.height)
        }[clip.info.position_type]

    def get_next_clip(self):
        for clip in self._clip_sequence:

            clip.position = self.__get_position_by_pos_type(clip)

            yield clip

    def append_clip(self, clip):
        self._clip_sequence.append(clip)

    @property
    def frame_count(self):
        return sum([clip.info.frame_count for clip in self.clip_sequence])

    @property
    def clip_sequence(self):
        return self._clip_sequence
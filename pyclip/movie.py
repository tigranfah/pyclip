import cv2
import numpy as np

from clip import Position


class MovieBase:

    def __init__(self, name, width, height, fps):
        self._name = name
        self._width = width
        self._height = height
        self._fps = fps
        self._background_color = (0, 0, 0)

    @property
    def name(self):
        return self._name

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, width):
        self._width = width

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def fps(self):
        return self._fps

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, color):
        self._background_color = color


class Movie(MovieBase):

    def __init__(self, name, width, height, fps):
        MovieBase.__init__(self, name, width, height, fps)
        self._clip_sequence = {}
        self._audio_sequence = {}

    def __get_position_by_pos_type(self, clip):
        return {
            "" : (0, 0),
            "center" : (
                (1 - clip.info.trans.scale.w) / 2,
                (1 - clip.info.trans.scale.h) / 2
            ),
            "left" : (0, (1 - clip.info.trans.scale.h) / 2),
            "top" : ((1 - clip.info.trans.scale.w) / 2, 0),
            "right" : (
                1 - clip.info.trans.scale.w,
                (1 - clip.info.trans.scale.h) / 2
            ),
            "bottom" : (
                (1 - clip.info.trans.scale.w) / 2,
                1 - clip.info.trans.scale.h
            ),
            "top-left" : (0, 0),
            "top-right" : (1 - clip.info.trans.scale.w, 0),
            "bottom-left" : (0, 1 - clip.info.trans.scale.h),
            "bottom-right" : (1 - clip.info.trans.scale.w, 1 - clip.info.trans.scale.h)
        }[clip.info.position_type]

    def append_clip(self, clip):
        if not self._clip_sequence:
            clip.info.pos_in_movie = (0, clip.info.frame_count)
        else:
            clip.info.pos_in_movie = (self.frame_count, self.frame_count + clip.info.frame_count)
        if clip.info.position_type:
            clip.info.trans.pos = self.__get_position_by_pos_type(clip)
        self._clip_sequence[len(self._clip_sequence) + 1] = clip

    def put_clip(self, clip, frame_number):
        clip.info.pos_in_movie = (frame_number, frame_number + clip.info.frame_count)
        if clip.info.position_type:
            clip.info.trans.pos = self.__get_position_by_pos_type(clip)
        self._clip_sequence[len(self._clip_sequence) + 1] = clip

    def process_running_clips(self, index):
        for i, clip in self._clip_sequence.items():
            if clip.info.pos_in_movie[0] <= index < clip.info.pos_in_movie[1]:
                yield i, clip
            elif clip.clip_source.current_frame_index != 0:
                clip.restore_source()

    @property
    def frame_count(self):
        largest_frame = 0
        for clip in self.clip_sequence.values():
            if clip.info.pos_in_movie[1] > largest_frame:
                largest_frame = clip.info.pos_in_movie[1]
        return largest_frame

    @property
    def clip_sequence(self):
        return self._clip_sequence

    # @width.setter
    # def width(self, width):
    #     MovieBase.width(self, width)
    #
    #
    # @height.setter
    # def height(self, height):
    #     MovieBase.height(self, height)

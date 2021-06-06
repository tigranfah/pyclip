import cv2
import numpy as np
import pygame

from pathlib import Path
import os
import sys

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


class ClipManager:

    @staticmethod
    def load_from_file(file_path):
        if not error_handler.path_is_valid(file_path):
            raise error_handler.PathIsNotValid("{} is not a valid file directory.".format(file_path))

        new_clip = Clip()

        # cap = cv2.VideoCapture(file_path)

        new_clip.clip_source = VideoCaptureSource(file_path)
        new_clip.info = ClipInfo("Movie1", new_clip.clip_source.width, new_clip.clip_source.height, 
                      new_clip.clip_source.frame_count, new_clip.clip_source.fps, position_type="center")

        return new_clip


class ClipInfo:
    
    def __init__(self, title, width, height, frame_count, fps, position=None, position_type=""):

        self.title = title
        self.width = width
        self.height = height
        self.frame_count = frame_count
        self.fps = fps

        self._frame_indices = (0, frame_count)

        self.position = position
        self.position_type = position_type

        self.pos_in_movie = ()

    @property
    def frame_indices(self):
        return self._frame_indices

    @frame_indices.setter
    def frame_indices(self, frame_ind):
        self.frame_count = frame_ind[1] - frame_ind[0]
        self._frame_indices = frame_ind


class ClipSource:
    
    def read_next_frame(self):
        pass

    def restore_source(self):
        pass


class VideoCaptureSource(ClipSource):
    
    def __init__(self, file_path):
        self._file_path = file_path
        self._capture = None
        self.__init_capture()

    def __init_capture(self):
        self._capture = cv2.VideoCapture(self._file_path)

    def read_next_frame(self):
        # print(self.current_frame_index)
        if self._capture.isOpened():
            ret, frame = self._capture.read()
            
            return ret, frame

    def restore_source(self):
        self.__init_capture()

    def set_read_frame(self, frame_number):
        self._capture.set(1, frame_number)

    @property
    def width(self):
        return int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        return int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame_count(self):
        return int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def fps(self):
        return int(self._capture.get(cv2.CAP_PROP_FPS))

    @property
    def current_frame_index(self):
        return int(self._capture.get(cv2.CAP_PROP_POS_FRAMES))


class Clip:

    def __init__(self):
        self._info = None
        self._clip_source = None

    def initialize(self):
        self._clip_source.restore_source()
        self._clip_source.set_read_frame(self._info.frame_indices[0])

    def get_next_frame(self):

        while self._clip_source.current_frame_index <= self._info.frame_indices[1]:
            ret, frame = self._clip_source.read_next_frame()

            if not ret: break

            resized_frame = cv2.resize(frame, (self._info.width, self._info.height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

            yield resized_frame

    def cut_from_left(self, frame_number):
        self._info.frame_indices = (self._info.frame_indices[0] + frame_number, self._info.frame_indices[1])
        
    def cut_from_right(self, frame_number):
        self._info.frame_indices = (self._info.frame_indices[0], self._info.frame_indices[1] - frame_number)
        
    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, inf):
        self._info = inf

    @property
    def clip_source(self):
        return self._clip_source

    @clip_source.setter
    def clip_source(self, source):
        self._clip_source = source
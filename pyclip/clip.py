import cv2
import numpy as np
import pygame

from pathlib import Path
import os
import sys
import logging

import error_handler
from transformation import Transformation, Position


class ClipInfo:

    def __init__(self, name, pos, scale, rot, frame_count, fps, position_type=""):

        self.name = name
        self.trans = Transformation(pos, scale, rot)
        self.frame_count = frame_count
        self.fps = fps

        self._frame_indices = (0, frame_count)

        self.position_type = position_type

        self.pos_in_movie = ()

    @property
    def frame_indices(self):
        return self._frame_indices

    @property
    def duration_in_seconds(self):
        return self.frame_count / self.fps

    @frame_indices.setter
    def frame_indices(self, frame_ind):
        self.frame_count = frame_ind[1] - frame_ind[0]
        self._frame_indices = frame_ind


class ClipSource:

    def read_next_frame(self):
        pass

    def release(self):
        pass


class VideoCaptureSource(ClipSource):

    def __init__(self, file_path):
        print("here")
        self._file_path = file_path
        self._capture = None
        self.init_clip()

    def init_clip(self):
        self._capture = cv2.VideoCapture(self._file_path)

    def release(self):
        self._capture.release()

    def read_next_frame(self):
        if self._capture.isOpened():
            ret, frame = self._capture.read()

            return ret, frame

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

    def __init__(self, file_path):

        if not error_handler.path_is_valid(file_path):
            raise error_handler.PathIsNotValid("{} is not a valid file directory.".format(file_path))

        self._clip_source = None
        self._info = None

        self.acquire_source(file_path)

    def acquire_source(self, path):
        self._clip_source = VideoCaptureSource(path)
        self._info = ClipInfo(os.path.split(path)[-1], (0, 0), (self._clip_source.width, self._clip_source.height), 0,
                      self._clip_source.frame_count, self._clip_source.fps, position_type="center")

        self._clip_source.set_read_frame(self._info.frame_indices[0])
        logging.info("Clip {} is acquired.".format(self._info.name))

    def restore_source(self):
        self._clip_source.set_read_frame(self._info.frame_indices[0])

    def release_source(self):
        self._clip_source.release()
        logging.info("Clip {} is released.".format(clip.name))

    def get_next_frame(self):

        while self._clip_source.current_frame_index <= self._info.frame_indices[1]:
            ret, frame = self._clip_source.read_next_frame()

            if not ret: break

            yield frame

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

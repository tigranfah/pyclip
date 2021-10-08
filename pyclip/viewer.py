import cv2
import numpy as np
import pygame
import pygame_gui
import sounddevice as sd

import time
import logging

from movie import MovieBase
from renderer import Renderer, Converter
from transformation import Scale


class MovieViewer(MovieBase):

    __instance = None
    _width = int(720/1.5)
    _height = int(480/1.5)

    def __init__(self):

        if MovieViewer.__instance != None:
            raise Exception(__class__.__name__ + " is a singleton class.")

        MovieBase.__init__(self, None, None, None, None)

        self._display = None

        self._clock = pygame.time.Clock()

        self._renderer = None

        MovieViewer.__instance = self

    def init_display(self, movie):
        self._fps = movie.fps

        self._display = pygame.display.set_mode((MovieViewer._width, MovieViewer._height), flags=pygame.SHOWN)
        pygame.display.set_caption("Viewer window.")

        self._manager = pygame_gui.UIManager((MovieViewer._width, MovieViewer._height))

        self._button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MovieViewer._width/2 - 25, MovieViewer._height-100+20), (50, 50)), text="hello", manager=self._manager)

        self._slider_bar = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, MovieViewer._height-100), (MovieViewer._width, 20)), start_value=0, value_range=(0, movie.frame_count), manager=self._manager)

        self._renderer = Renderer(self._display)

    @staticmethod
    def get_instance():
        return MovieViewer.__instance

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


MovieViewer()


def play(movie):

    logging.info("Playing movie {}.".format(movie.name))

    movie_viewer = MovieViewer.get_instance()

    time_delta = movie_viewer._clock.tick(60)/1000.0

    movie_viewer.init_display(movie)

    slide_bar = movie_viewer._slider_bar

    is_playing = True

    is_moving = False
    has_been_moved = False

    current_clips = []

    while slide_bar.get_current_value() != movie.frame_count:

        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:

                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == movie_viewer._slider_bar:
                        is_moving = True
                else:
                    if is_moving:
                        has_been_moved = True
                    is_moving = False

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == movie_viewer._button:
                        is_playing = False if is_playing else True

            movie_viewer._manager.process_events(event)

            if event.type == pygame.QUIT:
                return

        prev_current_clips = current_clips

        current_clips = [clip for i, clip in movie.get_clip_by_frame_index(slide_bar.get_current_value())]

        for clip in prev_current_clips:
            if not clip in current_clips:
                clip.restore_source()

        if has_been_moved:
            for clip in current_clips:
                clip.clip_source.set_read_frame(slide_bar.get_current_value() - clip.info.pos_in_movie[0] + clip.info.frame_indices[0])
            has_been_moved = False

        if is_playing and not is_moving:
            current_frames = []
            for clip in current_clips:
                next_frame = next(clip.get_next_frame(), np.empty(0))
                current_frames.append(next_frame)
            slide_bar.set_current_value(slide_bar.get_current_value() + 1)

        movie_viewer._manager.update(time_delta)

        movie_viewer._renderer.clear(movie.background_color)

        for clip, frame in zip(current_clips, current_frames):
            movie_viewer._renderer.render_frame(MovieViewer._width, MovieViewer._height-100, frame, clip.info.trans)

        movie_viewer._clock.tick(movie_viewer._fps)

        movie_viewer._manager.draw_ui(movie_viewer._display)

        pygame.display.update()

        movie_viewer._clock.tick(60)

    pygame.display.quit()

    logging.info("Played movie {}.".format(movie.name))

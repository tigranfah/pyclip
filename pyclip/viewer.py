import cv2
import numpy as np
import pygame
import pygame_gui

import time
import logging

from movie import MovieBase
from renderer import Renderer, Converter
from transformation import Scale
import error_handler
import gui
import logger
import time


class MovieViewer(MovieBase):

    __instance = None

    def __init__(self, name="Viewer window.", width=int(720/1.5), height=int(480/1.5), fps=60):

        if MovieViewer.__instance != None:
            raise error_handler.SingletonClass(f"{__class__.__name__} is a singleton class.")

        MovieBase.__init__(self, name, width, height, fps)

        self._display = None
        self._renderer = None
        self._is_playing = False
        self._is_rendering_frames = False
        self._viewing_movie = None

        self._moving_update_time = 0

        self._clock = pygame.time.Clock()

        MovieViewer.__instance = self

    def init_viewer(self, movie):
        self._is_playing = True
        self._is_rendering_frames = True
        self._viewing_movie = movie

        self._display = pygame.display.set_mode((self._width, self._height), flags=pygame.SHOWN)
        pygame.display.set_caption(self._name)
        self._renderer = Renderer(self._display)

        self._gui_manager = pygame_gui.UIManager((self._width, self._height))
        self._ss_button = gui.Button(relative_rect=pygame.Rect((self._width/2 - 25, self._height-100+20), (50, 50)), text="", manager=self._gui_manager)
        self._timeline_slider = gui.HorizontalSlider(relative_rect=pygame.Rect((0, self._height-100), (self._width, 20)), start_value=0, value_range=(0, movie.frame_count), manager=self._gui_manager)

    def render_clip_frames(self):
        for i, clip in self._viewing_movie.process_running_clips(self._timeline_slider.get_current_value()):
            frame = next(clip.get_next_frame())
            self._renderer.render_frame(self._width, self._height-100, frame, clip.info.trans)
        if not self._viewing_movie.frame_count == self._timeline_slider.get_current_value():
            self._timeline_slider.set_current_value(self._timeline_slider.get_current_value() + 1)
        # self._renderer._rendering_surface = pygame.display.get_surface()

    def pull_events(self):
        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:
                self.timeline_slider.on_moved(event, self)
                self.start_stop_button.on_clicked(event, self)

            self._gui_manager.process_events(event)

            if event.type == pygame.QUIT:
                self.is_playing = False

    @property
    def viewing_movie(self):
        return self._viewing_movie

    @property
    def timeline_slider(self):
        return self._timeline_slider

    @property
    def start_stop_button(self):
        return self._ss_button

    @property
    def is_playing(self):
        return self._is_playing

    @is_playing.setter
    def is_playing(self, is_pl):
        self._is_playing = is_pl

    @staticmethod
    def get_instance():
        return MovieViewer.__instance


MovieViewer()


@logger.movie_view_log
def play(movie):

    movie_viewer = MovieViewer.get_instance()
    movie_viewer.init_viewer(movie)

    time_delta = movie_viewer._clock.tick(60)/1000.0

    while movie_viewer.is_playing:

        movie_viewer.pull_events()

        movie_viewer._renderer.clear(movie.background_color)

        if movie_viewer._timeline_slider.is_moving:
            current_time = time.time()
            if not movie_viewer._moving_update_time or current_time - movie_viewer._moving_update_time >= 0.3:
                movie_viewer._moving_update_time = current_time
                for i, clip in movie_viewer._viewing_movie.process_running_clips(movie_viewer._timeline_slider.get_current_value()):
                    clip.clip_source.set_read_frame(movie_viewer._timeline_slider.get_current_value() - clip.info.pos_in_movie[0] + clip.info.frame_indices[0])

        if movie_viewer._is_rendering_frames:
            movie_viewer.render_clip_frames()
        # else:
        #     movie_viewer._renderer.render_current_surface()


        movie_viewer._clock.tick(movie_viewer._fps)

        movie_viewer._gui_manager.update(time_delta)
        movie_viewer._gui_manager.draw_ui(movie_viewer._display)

        pygame.display.update()

        movie_viewer._clock.tick(60)

    for clip in movie.clip_sequence:
        clip.release_source()

    pygame.display.quit()

    return movie.frame_count == movie_viewer._timeline_slider.get_current_value()

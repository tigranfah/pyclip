import cv2
import numpy as np
import pygame
import pygame_gui

import time

from movie import MovieBase
from renderer import Renderer, Converter


class MovieViewer(MovieBase):

    __instance = None

    def __init__(self):

        if MovieViewer.__instance != None:
            raise Exception(__class__.__name__ + " is a singleton class.")

        MovieBase.__init__(self, None, None, None, None)

        self._display = None

        self._clock = pygame.time.Clock()

        self._renderer = None

        self._mouse_event = None

        self._movie_width = None
        self._movie_height = None

        MovieViewer.__instance = self

    def init_display(self, movie):

        self._width = movie.width
        self._height = movie.height + 100
        self._fps = movie.fps

        self._movie_width = movie.width
        self._movie_height = movie.height

        self._display = pygame.display.set_mode((self._width, self._height), flags=pygame.SHOWN)
        pygame.display.set_caption("Viewer window.")

        self._manager = pygame_gui.UIManager((self._width, self._height))

        self._button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((movie.width/2 - 25, movie.height+20), (50, 50)), text="hello", manager=self._manager)

        self._slider_bar = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, movie.height), (self._width, 20)), start_value=0, value_range=(0, movie.frame_count), manager=self._manager)

        self._renderer = Renderer(self._display)

    def poll_events(self):
        pass

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

    movie_viewer = MovieViewer.get_instance()

    time_delta = movie_viewer._clock.tick(60)/1000.0

    movie_viewer.init_display(movie)

    slide_bar = movie_viewer._slider_bar
        
    is_playing = True

    is_moving = False
    has_been_moved = False

    current_clips = []

    while True:

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
                clip.initialize()

        if has_been_moved:
            for clip in current_clips:
                clip.clip_source.set_read_frame(slide_bar.get_current_value() - clip.info.pos_in_movie[0] + clip.info.frame_indices[0])
                # print("moved to", clip)
            has_been_moved = False

        if is_playing and not is_moving:
            current_frames = []
            for clip in current_clips:
                current_frames.append(next(clip.get_next_frame(), np.empty(0)))
            slide_bar.set_current_value(slide_bar.get_current_value() + 1)
            
        if not current_clips:
            break
                
        mouse = movie_viewer._mouse_event

        movie_viewer._manager.update(time_delta)

        movie_viewer._renderer.clear()

        for clip, frame in zip(current_clips, current_frames):
            movie_viewer._renderer.render_frame(clip.info.trans.pos, frame)

        movie_viewer._clock.tick(movie_viewer._fps)

        movie_viewer._manager.draw_ui(movie_viewer._display)

        pygame.display.update()

        movie_viewer._clock.tick(60)

    pygame.display.quit()
import cv2
import numpy as np
import pygame
import pygame_gui

import time

from clip import Position
from movie import MovieBase
from renderer import Renderer, Converter
from event_handler import MouseEvent


class MovieWriter(MovieBase):

    __instance = None

    def __init__(self):

        if MovieWriter.__instance != None:
            raise Exception(__class__.__name__ + " is a singleton class.")

        MovieBase.__init__(self, None, None, None, None)

        self._display = None

        self._renderer = None

        self._clock = pygame.time.Clock()
        self._video_writer = None

        MovieWriter.__instance = self

    def __init_display(self, width, height, fps):
        self._width = width
        self._height = height
        self._fps = fps

        self._display = pygame.display.set_mode((width, height), flags=pygame.HIDDEN)
        pygame.display.set_caption("Writer window.")

        self._renderer = Renderer(self._display)

    @staticmethod
    def export(movie_name, movie):

        time1 = time.time()

        MovieWriter.__instance.__init_display(movie.width, movie.height, movie.fps)

        MovieWriter.__instance._video_writer = cv2.VideoWriter("{}.mp4".format(movie_name), cv2.VideoWriter_fourcc(*"mp4v"), 30, (movie.width, movie.height))

        clip_index = 1

        while True:
            
            current_clip = movie.clip_sequence.get(clip_index)

            if not current_clip:
                break

            clip_index = clip_index + 1

            for frame in current_clip.get_next_frame():

                MovieWriter.__instance._renderer.clear()

                MovieWriter.__instance._renderer.render_frame(current_clip.position, frame)
                
                dsiplay_frame = Converter.surface_to_frame(pygame.display.get_surface())
                
                MovieWriter.__instance._video_writer.write(dsiplay_frame)

        # print(time.time() - time1)

        pygame.display.quit()

    @staticmethod
    def get_instance():
        return Viewer.__instance

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


MovieWriter()


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

    def __init_display(self, movie):

        self._width = movie.width
        self._height = movie.height + 100
        self._fps = movie.fps

        self._movie_width = movie.width
        self._movie_height = movie.height

        self._manager = pygame_gui.UIManager((self._width, self._height))

        self._slider_bar = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((0, movie.height), (self._width, 20)), start_value=0, value_range=(0, movie.frame_count), manager=self._manager)

        self._button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((movie.width/2 - 25, movie.height+20), (50, 50)), text="hello", manager=self._manager)

        self._display = pygame.display.set_mode((self._width, self._height), flags=pygame.SHOWN)
        pygame.display.set_caption("Viewer window.")

        self._renderer = Renderer(self._display)

        self._mouse_event = MouseEvent()

    def poll_events(self):
        pass

    @staticmethod
    def play(movie):

        time_delta = MovieViewer.__instance._clock.tick(60)/1000.0

        MovieViewer.__instance.__init_display(movie)

        slide_bar = MovieViewer.__instance._slider_bar

        frame_index = 0

        for i, clip in movie.clip_sequence.items():
            print(i, clip)

        clip_index = 0

        is_playing = True

        # print(MovieViewer.__instance._slider_bar._focus_set)

        is_moving = False
        has_been_moved = False

        while True:

            clip_index = clip_index + 1
            
            current_clip = movie.clip_sequence.get(clip_index)

            if not current_clip:
                break

            current_clip.initialize()

            # print(dir(pygame_gui))

            while True:

                for event in pygame.event.get():

                    MovieViewer.__instance._mouse_event.update(event)
                    if event.type == pygame.USEREVENT:
                        # print("thread")
                        if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                            if event.ui_element == MovieViewer.__instance._slider_bar:
                                is_moving = True
                        else:
                            if is_moving:
                                has_been_moved = True
                            is_moving = False

                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == MovieViewer.__instance._button:
                                is_playing = False if is_playing else True


                    MovieViewer.__instance._manager.process_events(event)

                    if event.type == pygame.QUIT:
                        return

                if is_playing and not is_moving:
                    current_frame = next(current_clip.get_next_frame(), np.empty(0))
                    slide_bar.set_current_value(slide_bar.get_current_value() + 1)
                    if current_frame.shape[0] == 0:
                        break

                mouse = MovieViewer.__instance._mouse_event

                MovieViewer.__instance._manager.update(time_delta)

                if has_been_moved:
                    ind, _clip = movie.get_clip_by_frame_index(slide_bar.get_current_value())
                    _clip.clip_source.set_read_frame(slide_bar.get_current_value() - _clip.info.pos_in_movie[0] + _clip.info.frame_indices[0])
                    frame_index = slide_bar.get_current_value()
                    clip_index = ind
                    print("moved to", clip_index)
                    current_clip = _clip
                    has_been_moved = False

                MovieViewer.__instance._renderer.clear()

                MovieViewer.__instance._renderer.render_frame(current_clip.position, current_frame)

                MovieViewer.__instance._clock.tick(MovieViewer.__instance._fps)

                MovieViewer.__instance._manager.draw_ui(MovieViewer.__instance._display)

                pygame.display.update()

                MovieViewer.__instance._clock.tick(60)

        # print(time.time() - time1)

        pygame.display.quit()

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
import cv2
import numpy as np
import pygame
import pygame_gui

import time

from clip import Position
from movie import MovieBase
from gui import ControlBar
from renderer import Renderer, Converter
from event_handler import MouseEvent


class MovieWriter(MovieBase):

    __instance = None

    def __init__(self):

        if MovieWriter.__instance != None:
            raise Exception(__class__.__name__ + " is a singleton class.")

        MovieBase.__init__(self, None, None, None, None)

        self._display = None

        self._clock = pygame.time.Clock()
        self._video_writer = None

        MovieWriter.__instance = self

    def __init_display(self, width, height, fps):
        self._width = width
        self._height = height
        self._fps = fps

        self._display = pygame.display.set_mode((width, height), flags=pygame.HIDDEN)
        pygame.display.set_caption("Writer window.")

    @staticmethod
    def export(movie_name, movie):

        time1 = time.time()

        MovieWriter.__instance.__init_display(movie.width, movie.height, movie.fps)

        MovieWriter.__instance._video_writer = cv2.VideoWriter("{}.mp4".format(movie_name), cv2.VideoWriter_fourcc(*"mp4v"), 30, (movie.width, movie.height))

        for clip in movie.get_next_clip():
            for frame in clip.get_next_frame():

                surface = Converter.frame_to_surface(frame)

                MovieWriter.__instance._display.blit(surface, (clip.position.x, clip.position.y))

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

        print(dir(self._slider_bar))

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

        for current_clip in movie.get_next_clip():

            for current_frame in current_clip.get_next_frame():

                mouse = MovieViewer.__instance._mouse_event

                for event in pygame.event.get():

                    MovieViewer.__instance._mouse_event.update(event)

                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == MovieViewer.__instance._button:
                                print("Pressed!")

                    MovieViewer.__instance._manager.process_events(event)

                    if event.type == pygame.QUIT:
                        return

                # if sr_button.is_on:
                #     continue

                # if MovieViewer.__instance._mouse_event.is_pressed:
                #     print(MovieViewer.__instance._mouse_event.event_type)

                MovieViewer.__instance._manager.update(time_delta)

                # current_frame = next(current_clip.get_next_frame(), np.empty(0))
                # if current_frame.shape[0] == 0:
                #     break

                slide_bar.set_current_value(slide_bar.get_current_value() + 1)

                MovieViewer.__instance._renderer.clear()

                MovieViewer.__instance._renderer.render_frame(current_clip.position, current_frame)

                MovieViewer.__instance._clock.tick(MovieViewer.__instance._fps)

                MovieViewer.__instance._manager.draw_ui(MovieViewer.__instance._display)

                pygame.display.update()

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
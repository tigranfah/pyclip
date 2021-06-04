import cv2
import numpy as np
import pygame

import time

from clip import Position
from movie import MovieBase
from gui import StopResumeButton
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
        self._stop_resume_button = None

        self._clock = pygame.time.Clock()

        self._renderer = None

        self._mouse_event = None

        self._movie_width = None
        self._movie_height = None

        self._control_bar_width = None
        self._control_bar_height = 100

        MovieViewer.__instance = self

    def __init_display(self, width, height, fps):

        self._movie_width = width
        self._movie_height = height

        self._control_bar_width = width

        self._width = width
        self._height = height + self._control_bar_height
        self._fps = fps

        self._display = pygame.display.set_mode((self._width, self._height), flags=pygame.SHOWN)
        pygame.display.set_caption("Viewer window.")

        self._renderer = Renderer(self._display)

        self._mouse_event = MouseEvent()

        self._stop_resume_button = StopResumeButton(Position(self._width / 2 - 25, self._height - 50), 50, 50)

    def poll_events(self):
        pass

    @staticmethod
    def play(movie):

        time1 = time.time()

        MovieViewer.__instance.__init_display(movie.width, movie.height, movie.fps)

        for current_clip in movie.get_next_clip():

            while True:

                sr_button = MovieViewer.__instance._stop_resume_button

                mouse = MovieViewer.__instance._mouse_event

                for event in pygame.event.get():

                    MovieViewer.__instance._mouse_event.update(event)
                    
                    if mouse.event_type.get_event("LEFT"):
                        if sr_button.is_clicked(mouse.position[0], mouse.position[1]):
                            sr_button.on_click()


                    if event.type == pygame.QUIT:
                        return

                if sr_button.is_on:
                    continue

                # if MovieViewer.__instance._mouse_event.is_pressed:
                #     print(MovieViewer.__instance._mouse_event.event_type)

                current_frame = next(current_clip.get_next_frame(), np.empty(0))
                if current_frame.shape[0] == 0:
                    break

                MovieViewer.__instance._renderer.render_frame(current_clip.position, current_frame)

                MovieViewer.__instance._renderer.render_gui_component(sr_button)
                
                MovieViewer.__instance._clock.tick(MovieViewer.__instance._fps)

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
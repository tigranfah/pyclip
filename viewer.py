import cv2
import numpy as np
import pygame

import time

from clip import Position
from movie import MovieBase
from gui import StopResumeButton

pygame.init()


class Converter:

    @staticmethod
    def surface_to_frame(surface):
        frame = pygame.surfarray.pixels3d(pygame.transform.rotate(pygame.transform.flip(surface, True, False), 90))
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return bgr_frame

    @staticmethod
    def frame_to_surface(frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        numpy_frame_surf = pygame.surfarray.make_surface(rgb_frame)
        frame_surf = pygame.transform.rotate(pygame.transform.flip(numpy_frame_surf, False, True), -90)
        return frame_surf


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

        self._stop_resume_button = StopResumeButton(Position(self._width / 2 - 25, self._height - 50), 50, 50)

    @staticmethod
    def play(movie):

        time1 = time.time()

        MovieViewer.__instance.__init_display(movie.width, movie.height, movie.fps)

        for current_clip in movie.get_next_clip():

            while True:

                sr_button = MovieViewer.__instance._stop_resume_button

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            clicked_pos = pygame.mouse.get_pos()

                            if sr_button.is_clicked(clicked_pos[0], clicked_pos[1]):
                                sr_button.on_click()

                    if event.type == pygame.QUIT:
                        return

                if sr_button.is_on:
                    continue

                current_frame = next(current_clip.get_next_frame(), np.empty(0))
                if current_frame.shape[0] == 0:
                    break

                surface = Converter.frame_to_surface(current_frame)

                MovieViewer.__instance._display.blit(surface, (current_clip.position.x, current_clip.position.y))

                pygame.draw.rect(MovieViewer.__instance._display, (255, 255, 0), (sr_button.position.x, sr_button.position.y, sr_button.width, sr_button.height))

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
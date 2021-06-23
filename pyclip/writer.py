import cv2
import pygame
import numpy as np

import time

from movie import MovieBase
from renderer import Renderer, Converter


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

    def init_display(self, width, height, fps):
        self._width = width
        self._height = height
        self._fps = fps

        self._display = pygame.display.set_mode((width, height), flags=pygame.HIDDEN)
        pygame.display.set_caption("Writer window.")

        self._renderer = Renderer(self._display)

    @staticmethod
    def get_instance():
        return MovieWriter.__instance

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


MovieWriter()


def export(movie_name, movie):

    time1 = time.time()

    movie_writer = MovieWriter.get_instance()

    movie_writer.init_display(movie.width, movie.height, movie.fps)

    movie_writer._video_writer = cv2.VideoWriter("{}.mp4".format(movie_name), cv2.VideoWriter_fourcc(*"mp4v"), 30, (movie.width, movie.height))

    # while True:

    #     if not current_clip:
    #         break

    #     clip_index = clip_index + 1

    #     for frame in current_clip.get_next_frame():

    #         movie_writer._renderer.clear()

    #         movie_writer._renderer.render_frame(current_clip.position, frame)
                
    #         dsiplay_frame = Converter.surface_to_frame(pygame.display.get_surface())
                
    #         movie_writer._video_writer.write(dsiplay_frame)

    # print(time.time() - time1)

    # pygame.display.quit()

    for frame_index in range(1, movie.frame_count + 1):
            
        current_clips = [clip for i, clip in movie.get_clip_by_frame_index(frame_index)]

        if not current_clips:
            break

        movie_writer._renderer.clear()

        current_frames = []
        for clip in current_clips:
            current_frames.append(next(clip.get_next_frame(), np.empty(0)))

        for clip, frame in zip(current_clips, current_frames):
            movie_writer._renderer.render_frame(clip.info.position, frame)

        display_frame = Converter.surface_to_frame(pygame.display.get_surface())
                
        movie_writer._video_writer.write(display_frame)

    # print(time.time() - time1)

    pygame.display.quit()
import numpy as np
import cv2
import pygame

import time
import os
import copy

import clip
import movie
from viewer import MovieViewer, MovieWriter

pygame.init()

W = 600
H = 700

my_clip = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))
my_nature = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))

my_clip.info.position_type = "center"

my_clip.info.width = 600
my_clip.info.height = 700


movie = movie.Movie("hellodear", W, H, 30)
movie.append_clip(my_clip)
movie.append_clip(my_nature)

MovieViewer.play(movie)
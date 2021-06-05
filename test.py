import os

import pygame

import clip
import movie
from viewer import MovieViewer, MovieWriter

pygame.init()

nat = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))
dol = clip.ClipManager.load_from_file(os.path.join("res", "dolphins.mov"))
view = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))

# nat.info.position_type = "left"

nat.info.width = 1020
nat.info.height = 720

dol.info.width = 1020
dol.info.height = 720

movie = movie.Movie("Name", 1020, 720, 60)
movie.append_clip(nat)
movie.append_clip(dol)
movie.append_clip(view)

MovieViewer.play(movie)
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
W, H = 1020, 720
# nat.info.width = W
# nat.info.height = H

# dol.info.width = W
# dol.info.height = H

movie = movie.Movie("Name", W, H, 60)
movie.append_clip(nat)
movie.append_clip(dol)
movie.append_clip(view)

# MovieWriter.export("movie", movie)
MovieViewer.play(movie)
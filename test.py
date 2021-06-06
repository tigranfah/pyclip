import os
import copy

import pygame

import clip
import movie
from viewer import MovieViewer, MovieWriter

pygame.init()

nat = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))
dol = clip.ClipManager.load_from_file(os.path.join("res", "dolphins.mov"))
view = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))

# a = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))
# b = clip.ClipManager.load_from_file(os.path.join("res", "dolphins.mov"))
# c = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))


# nat.info.position_type = "left"
W, H = 720, 480
nat.info.width = W
nat.info.height = H

dol.info.width = W
dol.info.height = H

view.info.width = W
view.info.height = H

view.cut_from_right(100)
view.cut_from_right(150)

movie = movie.Movie("Name", W, H, 60)
movie.append_clip(view)
movie.append_clip(dol)
# movie.append_clip(view)
# a = nat
# b = dol
# c = view
# movie.append_clip(a)
# movie.append_clip(b)
# movie.append_clip(c)

# MovieWriter.export("movie", movie)
MovieViewer.play(movie)
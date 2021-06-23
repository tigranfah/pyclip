import os
import copy

import pygame
import cv2

import clip
import movie
from viewer import MovieViewer
from writer import MovieWriter

pygame.init()

nat = clip.Clip(os.path.join("res", "nature.mp4"))
dol = clip.Clip(os.path.join("res", "dolphins.mov"))
view = clip.Clip(os.path.join("res", "view.mp4"))

# a = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))
# b = clip.ClipManager.load_from_file(os.path.join("res", "dolphins.mov"))
# c = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))


# nat.info.position_type = "left"
W, H = 720, 480
nat.info.width = W
nat.info.height = H

view.info.position_type = "top-left"
dol.info.position_type = "bottom-right"

dol.info.width = 500
dol.info.height = 350

view.info.width = 500
view.info.height = 350

# view.cut_from_right(50)
# view.cut_from_right(150)

movie = movie.Movie("Name", W, H, 60)
movie.put_clip(view, 0)
movie.put_clip(dol, 100)
# movie.append_clip(view)
# a = nat
# b = dol
# c = view
# movie.append_clip(view)
# movie.append_clip(dol)
# movie.append_clip(c)

# MovieWriter.export("movie", movie)
MovieViewer.play(movie)
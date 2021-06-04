import numpy as np
import cv2

import time
import os
import copy

import clip
import movie
from viewer import MovieViewer, MovieWriter

W = 600
H = 700

my_clip = clip.ClipManager.load_from_file(os.path.join("res", "view.mp4"))
my_nature = clip.ClipManager.load_from_file(os.path.join("res", "nature.mp4"))

my_clip.info.position_type = "center"

my_clip.info.width = 600
my_clip.info.height = 700

# print(my_clip.info.width, my_clip.info.height)

# my_nature.info.width = 1500
# my_nature.info.height = 1200

movie = movie.Movie("hellodear", W, H, 30)
movie.append_clip(my_clip)
movie.append_clip(my_nature)

MovieViewer.play(movie)
# MovieWriter.export("New Movie", movie)
# movie.export("helpme.avi")
# movie.add_clip(my_clip)
# for frame in my_clip.frames:
#     cv2.imshow("frames", frame)

# print(my_clip.clip_source.get_frame())

# for frame in my_clip.clip_source.get_frame():
# print(my_clip.info.frame_count)
# while True:
    
#     frame = my_clip.content_file.get_next_frame()
    
#     cv2.imshow("Frame", frame)

#     if cv2.waitKey(2) & 0xFF == ord("q"):
#         break

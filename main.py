import os

import pyclip


clip = pyclip.Clip(os.path.join("res", "nature.mp4"))
movie = pyclip.Movie("Frames", 960, 480, 60)
movie.append_clip(clip)

pyclip.play(movie)
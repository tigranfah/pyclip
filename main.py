import os

import pyclip


nat = pyclip.Clip(os.path.join("res", "nature.mp4"))
dol = pyclip.Clip(os.path.join("res", "dolphins.mov"))
view = pyclip.Clip(os.path.join("res", "view.mp4"))

W, H = 720, 480

view.info.position_type = "top-left"
nat.info.position_type = "center"
dol.info.position_type = "bottom-right"

dol.info.trans.scale.w = 500
dol.info.trans.scale.h = 350

nat.info.trans.scale.w = 500
nat.info.trans.scale.h = 350

view.info.trans.scale.w = 500
view.info.trans.scale.h = 350
# view.info.trans.rot.angle = 90

movie = pyclip.Movie("Name", W, H, 60)
movie.background_color = (255, 0, 0)
movie.put_clip(nat, 100)
movie.put_clip(dol, 150)
movie.put_clip(view, 200)
# print(movie.clip_sequence)

pyclip.export("movie", movie)
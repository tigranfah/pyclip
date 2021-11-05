import os

import pyclip


nat = pyclip.Clip(os.path.join("res", "nature.mp4"))
dol = pyclip.Clip(os.path.join("res", "dolphins.mov"))
view = pyclip.Clip(os.path.join("res", "view.mp4"))

W, H = 1080, 720

view.info.position_type = "top-left"
nat.info.position_type = "center"
dol.info.position_type = "bottom-right"

dol.info.trans.scale.w = 0.5
dol.info.trans.scale.h = 0.5

nat.info.trans.scale.w = 0.4
nat.info.trans.scale.h = 0.4
nat.info.trans.rot.angle = 45

view.info.trans.scale.w = 0.2
view.info.trans.scale.h = 0.5
view.info.trans.rot.angle = 90

movie = pyclip.Movie("Name", W, H, 60)
# movie.background_color = (255, 0, 0)
movie.put_clip(nat, 0)
movie.put_clip(dol, 150)
movie.put_clip(view, 0)

pyclip.play(movie)
# pyclip.export("move", movie)

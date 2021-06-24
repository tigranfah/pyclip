import os

import pyclip


nat = pyclip.Clip(os.path.join("res", "nature.mp4"))
dol = pyclip.Clip(os.path.join("res", "dolphins.mov"))
view = pyclip.Clip(os.path.join("res", "view.mp4"))

# clip.info.trans.scale.w = 200
# clip.info.trans.scale.h = 100
# clip.info.trans.pos = 
# clip.info.position_type = ""

W, H = 720, 480

view.info.position_type = "top-left"
dol.info.position_type = "bottom-right"

dol.info.trans.scale.w = 500
dol.info.trans.scale.h = 350

view.info.trans.scale.w = 500
view.info.trans.scale.h = 350

view.info.trans.rot.angle = 30

movie = pyclip.Movie("Name", W, H, 60)
movie.put_clip(view, 0)
movie.put_clip(dol, 100)

pyclip.play(movie)
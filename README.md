# PyClips

**Pyclip** is a very simple, but flexible video processing library written in Python3.

```python
import pyclip


nat = pyclip.Clip("res/nature.mp4")
dol = pyclip.Clip("res/dolphins.mov")
view = pyclip.Clip("res/view.mp4")

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
movie.put_clip(nat, 0)
movie.put_clip(dol, 150)
movie.put_clip(view, 0)


# play or export movie
pyclip.play(movie)
pyclip.export(movie)

```

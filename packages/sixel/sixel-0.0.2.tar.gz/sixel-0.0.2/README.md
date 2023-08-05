made by [mat](https://repl.it/@mat1)

here's an example on how to do a rainbow
```py
import sixel
img = sixel.Image(width=6, height=6)
colors = [
	sixel.Color(148, 0, 211),
	sixel.Color(75, 0, 130),
	sixel.Color(0, 0, 255),
	sixel.Color(0, 255, 0),
	sixel.Color(255, 255, 0),
	sixel.Color(255, 127, 0),
	sixel.Color(255, 0, 0)
]

for i, c in enumerate(colors):
	img.fill(1, i, 6, 1, c)
img.draw()
```
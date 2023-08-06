import math
import time

class sixel():
	def __init__(self):
		self.colors = []
		self.data = []


		self.set_color(0, 0, 0)
		self.data.append('~~~~~~')

	def set_color(self, r, g, b, newblock=False, newline=False):
		if not newblock:
			self.data.append('$')
		elif newline:
			self.data.append('-')
		r, g, b = int(r / 2.55), int(g / 2.55), int(b / 2.55)
		try:
			colorid = self.colors.index((r, g, b))
			assert colorid != -1
		except:
			self.colors.append((r, g, b))
			colorid = len(self.colors) - 1
		self.data.append(f'#{colorid}')


	def compress(self,data):
		output = []
		repeated = 0
		before = ''
		output_append = output.append
		for i in data:
			if i != before:
				output_append(f'!{repeated}{before}' if repeated > 3 else before * repeated)
				repeated = 0
				before = i
			repeated += 1
		output_append(f'!{repeated}{before}' if repeated > 3 else before * repeated)
		return ''.join(output)

	def render(self):
		output = ''
		self.coldata = [(f'#{i};2;{col[0]};{col[1]};{col[2]}') for i, col in enumerate(self.colors)]
		output = ''.join(self.coldata + self.data)
		output = self.compress(output)
		return output


class Image():
	def __init__(self, width=6, height=6, bgcolor=None):
		if bgcolor is None:
			bgcolor = (0, 0, 0)
		self.width = width
		self.height = height
		self.pixels = [[bgcolor] * height] * width

	def set_pixel(self, x, y, color):
		self[x, y] = color

	def fill(self, x, y, x2, y2, color):
		for x3 in range(x2):
			for y3 in range(y2):
				self[x + x3, y + y3] = color

	def __setitem__(self, coords, color):
		x, y = coords
		xpixels = list(self.pixels[x])
		xpixels[y] = color
		self.pixels[x] = xpixels

	def __getitem__(self, coords):
		x, y = coords
		return self.pixels[x][y]

	def draw_line(self, y, chars = '?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'):
		selectedpixels = [i[y * 6:(y + 1) * 6] for i in self.pixels]
		allcolors = set()
		allcolors_update = allcolors.update
		[allcolors_update(i) for i in selectedpixels]
		set_color = self.s.set_color
		data_extend = self.s.data.extend
		for c in allcolors:
			set_color(c[0], c[1], c[2])
			data_extend([(
				chars[(1 if c == i[0] else 0) + (2 if c == i[1] else 0) + (4 if c == i[2] else 0) + (8 if c == i[3] else 0) + (16 if c == i[4] else 0) + (32 if c == i[5] else 0)]
			) for i in selectedpixels])


	def render(self):
		self.s = sixel()
		dataappend = self.s.data.append
		draw_line = self.draw_line
		for y in range(math.ceil(self.height / 6)):
			draw_line(y)
			dataappend('-')
		self.output = self.s.render()
		self.output = '\033Pq' + self.output + '\033\\'
	def draw(self):
		print(self.output)
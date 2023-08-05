import time
import math

class sixel():
	def __init__(self):
		self.colors = []
		self.data = ''

		self.set_color(0, 0, 0)
		self.draw_column('111111')
		self.draw_column('111111')
		self.draw_column('111111')
		self.draw_column('111111')
		self.draw_column('111111')
		self.draw_column('111111')

	def set_color(self, r, g, b, newblock=False, newline=False):
		if not newblock:
			self.data += '$'
		if newline:
			self.data += '-'
		r, g, b = int(r / 2.55), int(g / 2.55), int(b / 2.55)
		if (r, g, b) in self.colors:
			colorid = self.colors.index((r, g, b))
		else:
			self.colors.append((r, g, b))
			colorid = len(self.colors) - 1
		self.data += f'#{colorid}'

	def draw_column(self, *data):
		if len(data) == 6 and type(data) in (list, tuple):
			(a, b, c, d, e, *f) = data
			binchar = '1' if a else '0'
			binchar += '1' if b else '0'
			binchar += '1' if c else '0'
			binchar += '1' if d else '0'
			binchar += '1' if e else '0'
			binchar += '1' if f else '0'
		elif len(data) == 1:
			try:
				assert len(data[0]) == 6
				data = data[0].replace(' ', '0')
				int(data, 2)
				binchar = ''.join(data)
			except AssertionError:
				raise Exception(f'oof {len(data[0])}')
		else:
			raise Exception('idk ' + str(len(data)) + str(type(data)) + str(data))

		intchar = int(binchar, 2)
		asciichar = chr(intchar + 63)
		self.data += asciichar

	def draw_row(self):
		pass

	def render(self):
		output = ''
		self.coldata = ''
		for i, col in enumerate(self.colors):
			self.coldata += f'#{i};2;{col[0]};{col[1]};{col[2]}'
		output = self.coldata + self.data
		output = output.rstrip('-')
		print('\033Pq' + output + '\033\\')
		return output


class Image():
	def __init__(self, width=6, height=6, bgcolor=None):
		if bgcolor is None:
			bgcolor = Color(0, 0, 0)
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
		x -= 1
		y -= 1
		xpixels = list(self.pixels[x])
		xpixels[y] = color
		self.pixels[x] = xpixels

	def __getitem__(self, coords):
		x, y = coords
		return self.pixels[x][y]

	def draw_line(self, y):
		selectedpixels = []
		for i in self.pixels:
			selectedpixels.append(i[y * 6:(y + 1) * 6])
		allcolors = set()
		for i in selectedpixels:
			for c in i:
				if c not in allcolors:
					allcolors.add(c)

		for c in allcolors:
			self.s.set_color(c.r, c.g, c.b)
			for i in selectedpixels:
				linetmp = []
				for i2 in i:
					linetmp.append(c == i2)
				linechunks = []
				for i in range(0, len(linetmp), 6):
					linechunks.append(linetmp[i:i + 6])
				for linetmp2 in linechunks:
					column_bin = (str(int(l)) for l in linetmp2)
					binary = ''.join(column_bin)
					self.s.draw_column(''.join(binary))

	def draw(self):
		self.s = sixel()
		for y in range(math.ceil(self.height / 6)):
			self.draw_line(y)
			self.s.data += '-'
		output = self.s.render()
		print('>', output, '<')


class Color():
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

	def __repr__(self):
		return str(f'{self.r, self.g, self.b}')
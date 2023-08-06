from PIL import Image, ImageDraw
from math import ceil, sqrt

def color_vis(digits):
	''' @params a sequence of digits in an iterator
		@return an Image object that looks like a mosaic of digits.'''
	digmap = {
		'1': (255, 0, 0, 255),
		'2': (255, 255, 0, 255),
		'3': (0, 255, 255, 255),
		'4': (0, 255, 0, 255),
		'5': (50, 100, 255, 255),
		'6': (255, 0, 255, 255),
		'7': (0, 0, 255, 255),
		'8': (100, 50, 150, 255),
		'9': (100, 200, 100, 255),
	}
	colors = (digmap.get(d, 'white') for d in digits)
	n = sum([1 for _ in digits])

	w, h, pd = n, n, ceil(sqrt(n)) 
	blank_img = Image.new('RGBA', (w, h), 'white')
	img = ImageDraw.Draw(blank_img)

	for y in range(0, h, pd):
		for x in range(0, w, pd): 
			try:
				c = next(colors)
			except StopIteration:
				c = 'black'
			img.rectangle((x, y, x + pd, y + pd), outline='black', fill=c)
	return blank_img

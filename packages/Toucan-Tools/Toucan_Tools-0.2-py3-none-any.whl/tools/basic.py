from PIL import Image, ImageFilter
from os import path

def cycle(a, right=True):
	a.append(a.pop(0))
	if not right:
		a.append(a.pop(0))
	return a

def shift(img, right=True):
	''' @params an Image object, and a 'right' kwarg to specify which direction
			to shift the RGB values of each pixel.
		@return the transformed Image object, with the applied Color Shift.'''
	pix = img.load()
	width, height = img.size
	for x in range(width):
		for y in range(height):
			pix[x, y] = tuple(cycle(list(pix[x, y]), right=right))
	return img

def blur(img, radius=3):
	''' @params an Image object, and an optional radius kwarg for the Guassian Blur.
		@return the transformed Image object, with the applied Gaussian Blur.'''
	return img.filter(ImageFilter.GaussianBlur(radius=radius))

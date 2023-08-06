#!python
'''
Programmer: Miles Boswell
main.py

Take user input from cli (image file, tool to apply on image)
Display original image and transformed image side by side in window
Optional: overwrite image file with transformation
'''
import sys
from matplotlib import pyplot as plt
from PIL import Image
from tools.utils import error, transform, visualize_text

def user_input():
	''' @return: dictionary with Image object as 'img',
				 file of Image as 'file', and optional tool
				 to apply '''
	if len(sys.argv) > 1:
		sys.argv.pop(0)
		data = {}
		image_file = ''
		if '-t' in sys.argv:
			tool_index = sys.argv.index('-t') + 1
			tool = sys.argv.pop(tool_index)
			data['tool'] = tool
			sys.argv.pop(tool_index - 1)
		elif '-ts' in sys.argv:
			tool_index = sys.argv.index('-ts') + 1
			tool = sys.argv.pop(tool_index)
			data['tool'] = tool
			sys.argv.pop(tool_index - 1)
			data['save'] = sys.argv[0] 

		if '-s' in sys.argv:
			loc_index = sys.argv.index('-s') + 1
			loc = sys.argv.pop(loc_index)
			data['save'] = loc 

		image_file = sys.argv[0]
		if image_file.endswith('.txt'):
			img = visualize_text(image_file)
			img.show()
			sys.exit()

		try:
			img = Image.open(image_file)
		except:
			error('Could not find file: {}'.format(image_file))
		else:
			data['img'], data['file'] = img, image_file
		return data
	else:
		error('You must specify an image file.')

if __name__ == '__main__':
	data = user_input()
	# if a tool is specified, apply it to the Image and display
	img, tool = data.get('img'), data.get('tool', None)
	fileloc = data.get('file')
	save = data.get('save', False)
	if tool:
		trans = transform(tool)
		newimg = trans(img)
		newimg.show()
		if save:
			newimg.save(save)
	else:
		img.show()

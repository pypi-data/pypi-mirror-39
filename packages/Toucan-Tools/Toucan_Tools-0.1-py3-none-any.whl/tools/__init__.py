from . import Polytools
from os import path
from .basic import shift, blur 
from .vis import color_vis

def poly(img):
    if(img.size[0]*img.size[1]) > 10000:
        while(True):
            inp = input("Large images can take long to process. Continue? (y/n)")
            if inp == 'y':
                print("Continuing.")
                break
            elif inp == 'n':
                print("Exiting tool.")
                return
            else:
                print('y or n')
    Polytools.runTracker(img)
    Polytools.alter(img)
    return Polytools.polyImage(img)

def gray(img):
    #convert('LA') puts it in black and white, but for use in some other functions there must be three bands
    return img.convert('LA')

def testPoly():
	from PIL import Image 
	folder = path.dirname(__file__)
	filepath = path.join(folder, 'bin/test.jpg')
	img = gray(Image.open(filepath))
	img.show()
	poly(img)

if __name__ == '__main':
	testPoly()

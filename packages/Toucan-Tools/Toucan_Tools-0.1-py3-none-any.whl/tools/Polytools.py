"""Tools for grouping the image into pixel groups
methods:
pixelSet(numpy array of pil image) -- returns an array of pixels 
avgColor(array of pixel objects) -- finds the average color 
getPanels() -- returns panels
"""
from PIL import Image 
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
threshold=0#Threshold relative to the seed by color (brighntess blind)
marginalthreshold=0.3#Multiplicative threshold relative to neighbor (r1/r2)+(g1/g2)+(b1/b2)
marginalcap=3#How far from the seed the marginal threshold can go
linearthreshold=50#Flat amount threshold from seed (r1+g1+b1)-(r2+g2+c2) 
def pixelSet(arr):#Generates a list of pixel objects from rgb array
    pixels=[]
    for row in range(len(arr)):
        pixels+=[Pixel(arr[row][column],(row,column)) for column in range(len(arr[row]))]
    return pixels
def sum(arr):
    s=0
    for a in arr:
        s+=a
    return s    
def avgColor(pixset):   
    return [average([v.value[i] for v in pixset]) for i in range(len(pixset[0].value))]
def average(arr):#faster than the numpy one
    return sum(arr)/len(arr)
class Pixel(object):#Object to keep track of rgb values and positions
    def __init__(self,value,pos):
        self.value=value#RGB(A)
        self.pos=pos#XY
        self.neighbors=set()
    def similarity(self,compare):#returns the linear difference inthe rgb values. Takes another pixel
        return sum([(int(self.value[i])-int(compare.value[i]))**2 for i in range(len(self.value))])**0.5
    def compareColor(self,compare):#returns the multiplicative similarity between the colors. Takes another pixel
        return sum([abs(1-int(self.value[i]+1)/int(compare.value[i]+1))for i in range(len(self.value))])
    def borders(self,compare):#returns weather this pixel borders another pixel
        return abs(self.pos[0]-compare.pos[0])+abs(self.pos[1]-compare.pos[1])<2
    def __str__(self):
        return ("{"+str(self.value)+"-"+str(self.pos)+"}")
    __repr__=__str__
    #Whether two pixel objects are the same
    def eq(self,compare):
        for i in range(2):
            if not self.pos[i]==compare.pos[i]:
                return False
        return True
class Panel(object):#A class for keeping track of a group of pixels. Takes the list of pixels and a seed pixel
    #and gathers all pixels bordering the seed of a similar color
    def __init__(self,data,seed):
        #"magic wand" algorithm
        self.color=seed.value
        self.pixels=[]
        self.options={}
        self.margins={}
        for candidate in data:
            comp=candidate.compareColor(seed)
            if comp<threshold or seed.similarity(candidate)<linearthreshold and not candidate.eq(seed):
                self.options[str(candidate.pos)]=candidate
            elif comp<threshold+marginalcap and not candidate.eq(seed):
                self.margins[str(candidate.pos)]=candidate
        self.seed=seed
        self.gather(seed,0)
    def gather(self,p,depth):
        #recursive algorithm for gathering all bordering pixels similar in color, and all their borders, ect
        self.pixels.append(p)
        i=0
        if(depth<990):
            #arbitrary number to fit on stack.

            #step 1: find all neighbors.
            offset=((0,1),(0,-1),(1,0),(-1,0))
            for o in offset:
                npos=p.pos[0]+o[0],p.pos[1]+o[1]
                if str(npos) in self.options:
                    p.neighbors.add(self.options.pop(str(npos)))
                elif str(npos) in self.margins:
                    cand=self.margins[str(npos)]
                    if cand.compareColor(p)<marginalthreshold:
                        p.neighbors.add(self.margins.pop(str(npos)))
            #Step 2: Find all neighbors neighbors
            for p2 in p.neighbors:
                self.gather(p2,depth+1)
    #Runs the process with a live-updating GUI from Matplot
panels=[]
oldimg=None
def runTracker(img=None):
    global panels
    if img.__eq__(oldimg):
        print("Cached data used")
        return
    arr=numpy.array(img)
    plt.ion()
    implot=plt.imshow(arr)
    plt.show()
    plt.pause(0.1)
    data=pixelSet(arr)
    while len(data)>0:
        panel=Panel(data,data[0])
        panels.append(panel)
        for p in panel.pixels:
            data.remove(p)
        col=panel.color
        if len(panel.pixels)<20000:
            col=avgColor(panel.pixels)
            panel.color=col
        for i in panel.pixels:
            for ind in range(len(i.value)):
                arr[i.pos[0]][i.pos[1]]=col
        if len(panel.pixels)>20:
            implot=plt.imshow(arr)
            plt.show()
            plt.pause(0.01)
    implot=plt.imshow(arr)
    plt.show()
    plt.pause(0.01)
    img=Image.fromarray(arr)

"""
Tools for converting to and dealing with polygons.
"""
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
from collections import defaultdict
import os
#Reference from https://stackoverflow.com/a/43971906/10717280 
# points = ((1,1), (2,1), (2,2), (1,2), (0.5,1.5))
image=None
outline=None
image=None
img=None
smoothimg=1
scale=1
def smooth(pgon):
    smoothgons=[]
    for i in range(len(pgon)-1):
        dist=((pgon[i][0]-pgon[i+1][0])**2+(pgon[i][1]-pgon[i+1][1])**2)**0.5
        if(not dist==0):
            oweight=dist/(dist+smoothimg*scale*dist**0.5)
            nweight=smoothimg*scale*dist**0.5/(dist+smoothimg*scale*dist**0.5)
            smoothgons.append(tuple([int(oweight*pgon[i][j]+nweight*pgon[i+1][j]) for j in (0,1)]))
            print("point: "+str(smoothgons[-1]))
        else:
            smoothgons.append(pgon[i])
    smoothgons.append(pgon[-1])
    return smoothgons
def polygonize(panel):
    global outline, image,scale,img
    if len(panel.pixels)>1:
        #Sort panel by y,then by x. Starting with the highest y, work down
        #to the lowest y with the lowest x. The start with the lowsest y and highest x,
        #working up to the highest y. These are the vertices.
        pxs_uns=panel.pixels#unsorted pixels
        pxs_uns=sorted(pxs_uns,key=(lambda p: p.pos[1]))
        pxs=defaultdict(lambda: [])
        for p in pxs_uns:
            pxs[str(p.pos[1])].append(p)
        del pxs_uns
        points=[]
        pxskeys=sorted(pxs,key=lambda s:int(s))
        for key in pxskeys:
            pxs[key]=sorted(pxs[key], key=lambda p:p.pos[0])
            a=pxs[key]
            points.append((a[0].pos[1]*scale,a[0].pos[0]*scale))
            points=[(a[-1].pos[1]*scale,a[-1].pos[0]*scale)]+points
        # print(points[0])
        # print(points[-1])
        # print()
        draw = ImageDraw.Draw(image)
        if smoothimg>0:
            points=smooth(points)
        print(points)
        draw.polygon(points, fill=tuple([int(p) for p in panel.color]),outline=outline)
    else:
        point=panel.pixels[0].pos
        point=point[1]*scale,point[0]*scale#Reflection needed, polygon library has differenct order
        draw = ImageDraw.Draw(image)
        draw.polygon((point,point), fill=tuple(panel.pixels[0].value),outline=outline)
    
def polyImage(img):
    global image, panels,scale
    scale=min(2,max(10000/img.size[0],10000/img.size[1]))
    image = Image.new("RGB",(img.size[0]*scale,img.size[1]*scale))#canvas
    if(panels==None):
        print("Load Image First")
        return
    for p in panels:
        polygonize(p)
    while(True):
        inp=input("save or abandon image?")
        if inp=="save":
            image.save('results.png','png')
            break
        elif inp=='abandon':
            break
        else:
            print("Unrecognized. Commands are 'save' and 'abandon'")
    return image
def getValue(msg,type):
    while(True):
        inp=input(msg)
        try:
            return type(inp)
        except:
            print("!Please Enter a "+str(type))

def help():
    print("""Command List:
    quit -- exits the program
    show -- defines the image in polygons and shows
    setborder -- set the border to an rgb value for the next polygonize"
    clearborder -- sets the border to none
    scale -- sets the scale of the image
    smooth -- Set to True or False, makes edges smoothers
    help -- pull up this list""")

def alter(img):
    global scale, outline, smoothimg
    while True:
        prompt=input("Command?")
        if prompt=='quit':
            break
        elif prompt=='show':
            polyImage(img).show()
        elif prompt=='setborder':
            outline=getValue("R:",int),getValue("G:",int),getValue("B:",int)
        elif prompt=='clearborder':
            outline=None
        elif prompt=='scale':
            scale=getValue("Scale?",int)
        elif prompt=='help':
            help()
        elif prompt=='smooth':
            smoothimg=getValue("How Smooth (0 is no smoothing, scales upward)?",int)
        else:
            print("Unrecognized. Try 'help'")

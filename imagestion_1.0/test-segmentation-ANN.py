import scipy
from scipy import ndimage
from scipy import stats
from scipy.misc import toimage
import math
import matplotlib.pyplot as plt
import numpy as np
import colorsys, sys, os, re
from PIL import Image, ImageDraw, ImageFont
from scipy.optimize import curve_fit
from scipy.misc import factorial
from Segmentation import *
from ANN import *
from datetime import datetime

## import json
## from pybrain.tools.shortcuts import buildNetwork
## from pybrain.datasets import SupervisedDataSet
## from pybrain.supervised.trainers import BackpropTrainer
## from pybrain.structure import TanhLayer
## import pickle

#-----------------------------------------------------------------------

def evalPixel(pix, net):
	r,g,b = pix
	pixel = np.array([float(r)/255, float(g)/255, float(b)/255])
	test  = net.actualiza_nodos(pixel)
	return test[0]
   
#-----------------------------------------------------------------------

# Referencias: http://www.scipy-lectures.org/advanced/image_processing/
#  http://gis.stackexchange.com/questions/24827/how-to-smooth-the-polygons-in-a-contour-map
#  http://scikit-image.org
#  https://sites.google.com/site/bustosmerino/home/segmentacion---color-de-piel
        
imgFile = sys.argv[1]
dbFile = sys.argv[2]
print imgFile
print dbFile
shape1 = (2,2)
shape2 = (6,6)

seg = Segmentation(imgFile)
w = 300
h = int(round((seg.height * w) / seg.width))
rgb = seg.resize(seg.rgb,w,h)
seg.setRGB(toimage(rgb))
seg.splitRGB()


## rgb1 = np.array(seg.erodeRGB(shape1))
## rgb2 = np.array(seg.dilateRGB(shape2))

## diff = rgb2 - rgb1

## seg.rgb2hsv()
## seg.erodeHSV(shape2)
## seg.dilateHSV(shape1)
## seg.statisticalDispersionHSV()
## hsv = seg.getHSV()
## mask = seg.getHSVmask()
## invMask = ~mask
## mask[mask != 0xFF] = 0
## piel = seg.applyMask2Rgb(mask)
## invMask[invMask != 0xFF] = 0
## fondo = seg.applyMask2Rgb(invMask)

## seg.setRGB(piel)
## img1 = np.array(seg.erodeRGB(shape1)) 
## img2 = np.array(seg.dilateRGB(shape2)) 
## diff2 = img2 - img1

## toimage(seg.maskH).show()
## toimage(seg.maskS).show()
## toimage(seg.maskV).show()
## toimage(hsv).show()
## toimage(mask).show()
## toimage(invMask).show()
## toimage(piel).show()
## toimage(fondo).show()
## toimage(diff).show()
## toimage(diff2).show()

#-----------------------------------------------------------------------

net = ANN(3, 4, 1)

if os.path.isfile(dbFile) :
	print '3.- Restore previous session #########################'
	net.load(dbFile)
else:
	print 'Neural network file is missing '
	exit(0)

print '5.- Perform segmentation #########################'
## toimage(rgb).show()

im = np.array(rgb)
#im[evalPixel(x, net) < 0.6] = 0

start = datetime.now()
rgb = [[x if evalPixel(x, net) > 0.6 else (0,0,0) for x in row] for row in im]

stop = datetime.now()
delay = stop - start
print "delay: %s seg." % (delay)

toimage(rgb).show()
seg.setRGB(toimage(rgb))
seg.splitRGB()

diff = seg.getBorder(shape1,shape2)
# http://stackoverflow.com/questions/23935840/converting-an-rgb-image-to-grayscale-and-manipulating-the-pixel-data-in-python
bw = seg.color2grayScale(toimage(diff))
border = toimage(bw)
border.show()

print "continue? (y/n): "
k = sys.stdin.read(1)
ch = sys.stdin.readline()

if k == 'n':
	print 'exit #########################'
	exit(0)


ds = [] 
hist = {}
muestra1 = []
muestra2 = []
muestra3 = []
expect = [0.0, 0.0, 0.0, 0.0, 0.0]
expr = re.search('.+\W(\w+)[.]\w{3}', imgFile)
item = expr.group(1)[-1:]
idx = int(item) if re.search('^\d+$',item) else 0
expect[idx] = 1.0


i = j = k = 0
vectors = np.zeros(shape=(int(seg.height/3)+1, int(seg.width/3)+1))

for y in range(0,seg.height,3):
	for x in range(0,seg.width,3):
		dx = np.random.randint(0,2) + x
		dy = np.random.randint(0,2) + y
		col = border.getpixel((dx,dy)) if (dx<seg.width and dy<seg.height) else 0
		if i+j+k < 1500 :
			xx = float(dx)/seg.width
			yy = float(dy)/seg.height

			if (col == 0 and k < 500 and y%24 == 0 and x%24 == 0) :
				muestra3 = [yy, xx, float(col)/256]
				print "%05d (%02x, %d, %d) => [0] %s" % (k,col, dy, dx, [1.0, 0.0, 0.0, 0.0, 0.0])
				ds.append([muestra3, [1.0, 0.0, 0.0, 0.0, 0.0]])
				k += 1
				border.putpixel((dx,dy),(128))
			
			if (col & 0x1F > 0 and i < 500 and y%12 == 0 and x%12 == 0) :
				muestra2 = [yy, xx, float(col)/256]
				print "%05d (%02x, %d, %d) => [-1] %s" % (i,col, dy, dx, expect)
				ds.append([muestra2, expect])
				i += 1
				border.putpixel((dx,dy),(64))
			
			if (col > 0x1F and j < 500 and y%6 == 0 and x%6 == 0) :
				muestra1 = [yy, xx, float(col)/256]
				print "%05d (%02x, %d, %d) => [+1] %s" % (j,col, dy, dx, expect)
				ds.append([muestra1, expect])
				j += 1
				border.putpixel((dx,dy),(255))

			
border.show()

epochs = 5000
threshold = 0.05
error = 1

net2 = ANN(3, 4, 5, threshold)

if os.path.isfile(dbFile+'.recog') :
	print '3.- Restore previous session #########################'
	net2.load(dbFile+'.recog')
else:
	net2.iniciar_perceptron()

start = datetime.now()

print '4.- Training neural network #########################'
net2.entrenar_perceptron(ds,epochs)

stop = datetime.now()
delay = stop - start
print "delay: %s seg." % (delay)

print "write changes? (y/n): "
k = sys.stdin.read(1)
ch = sys.stdin.readline()

if k == 'y':
	print '6.- Store data to file #########################'
	net2.save(dbFile+'.recog')

import scipy
from scipy import ndimage
from scipy import stats
from scipy.misc import toimage
import math
import matplotlib.pyplot as plt
import numpy as np
import colorsys, sys, os
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
toimage(rgb).show()

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

case = sys.argv[3]
ds = [] 
hist = {}
muestra1 = []
muestra2 = []
expect = [0,0,0,0,0]



i = 0
for y in range(seg.height):
	if i > 30:
		break
	for x in range(seg.width):
		r,g,b = border.getpixel((x,y))
		xx = float(x)/seg.width
		yy = float(y)/seg.height
		key = "x%02x%02x%02x" % (r, g, b)
		hist[key] = hist[key] + 1 if key in hist else 0
		
		if (r|g|b > 0x1F and hist[key] == 0) :
			muestra1 = [yy, xx, float(r)/256, float(g)/256, float(b)/256]
			print "%05d (%02x, %02x, %02x) => [1] %s" % (i,r,g,b, muestra1)
			ds.append([muestra1, expect])
			i += 1
		if (r|g|b <= 0x1F and hist[key] == 0) :
			muestra2 = [yy, xx, float(r)/256, float(g)/256, float(b)/256]
			print "%05d (%02x, %02x, %02x) => [1] %s" % (i,r,g,b, muestra2)
			ds.append([muestra2, [0,0,0,0,0]])
			i += 1
			

net = ANN(5, 4, 5, threshold)

if os.path.isfile('fr-'+dbFile) :
	print '3.- Restore previous session #########################'
	net.load(dbFile)
else:
	net.iniciar_perceptron()

net.entrenar_perceptron(ds,epochs)

print "write changes? (y/n): "
k = sys.stdin.read(1)
ch = sys.stdin.readline()

if k == 'y':
	print '6.- Store data to file #########################'
	net.save('fr-'+dbFile)

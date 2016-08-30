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
	y,x,bw = pix
	data = np.array([float(yy), float(xx), float(bw)/255])
	test  = net.actualiza_nodos(data)
	return test
   
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

diff = seg.getBorder(shape1,shape2)
# http://stackoverflow.com/questions/23935840/converting-an-rgb-image-to-grayscale-and-manipulating-the-pixel-data-in-python
bw = seg.color2grayScale(toimage(diff))
border = toimage(bw)
border.show()


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


epochs = 5000
threshold = 0.05
error = 1

net = ANN(3, 4, 5, threshold)

if os.path.isfile(dbFile+'.recog') :
	print '1.- Restore previous session #########################'
	net.load(dbFile+'.recog')
else:
	exit(1)

start = datetime.now()

recog = np.array([0,0,0,0,0])
i = 1
for y in range(0,seg.height,3):
	for x in range(0,seg.width,3):
		col = border.getpixel((x,y))
		xx = float(x)/seg.width
		yy = float(y)/seg.height

		if (y%6 == 0 and x%6 == 0) :
			result = evalPixel([yy, xx, float(col)/256], net)
			## print "%05d (%02x, %d, %d) => %s" % (i, col, y, x, result)
			recog = recog + result
			i += 1
			
conclusion = recog / float(i)

print conclusion
				
stop = datetime.now()
delay = stop - start
print "delay: %s seg." % (delay)


# K-Nearest Neighbors
# http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
# http://scikit-learn.org/stable/modules/neighbors.html

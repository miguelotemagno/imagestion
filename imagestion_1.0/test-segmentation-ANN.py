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
rgb = seg.rgb
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

	
#http://pybrain.org/docs/quickstart/dataset.html
## ds = [] #SupervisedDataSet(3, 1)
## hist = {}
## muestra1 = []
## muestra2 = []		

#http://pybrain.org/docs/api/supervised/trainers.html#pybrain.supervised.trainers.BackpropTrainer
#http://pybrain.org/docs/quickstart/training.html
## net = buildNetwork(3, 3, 1, bias=True, hiddenclass=TanhLayer)
## trainer = BackpropTrainer(net, ds)
epochs = 5000
threshold = 0.05
error = 1

## trainer.trainUntilConvergence()

## while error > threshold:
	## error = trainer.train()
	## epochs -= 1
	## print "%d) e -> %f" % (epochs, error)
	## if epochs <= 0:
		## break
	

## print ("epochs:%d error:%f" % (epochs,error))
## print net.activate([muestra1[0], muestra1[1], muestra1[2]])
## print net.activate([muestra2[0], muestra2[1], muestra2[2]])

net = ANN(3, 4, 1, threshold)

if os.path.isfile(dbFile) :
	print '3.- Restore previous session #########################'
	net.load(dbFile)

	print '5.- Perform segmentation #########################'
	toimage(rgb).show()

	## start = datetime.now()
	## for yy in range(seg.height):
		## for xx in range(seg.width):
			## if (evalPixel(rgb.getpixel((xx,yy)), net) < 0.6) :
				## rgb.putpixel((xx,yy), 0)

	## stop = datetime.now()
	## delay = stop - start
	## print "delay: %d seg." % (delay)

	im = np.array(rgb)
	#im[evalPixel(x, net) < 0.6] = 0

	start = datetime.now()
	rgb = [[x if evalPixel(x, net) > 0.6 else (0,0,0) for x in row] for row in im]
	
	stop = datetime.now()
	delay = stop - start
	print "delay: %s seg." % (delay)

	toimage(rgb).show()
	## im = Image.fromarray(rgb)
	seg.setRGB(toimage(rgb))
	seg.splitRGB()
	
	## rgb1 = np.array(seg.erodeRGB(shape1))
	## rgb2 = np.array(seg.dilateRGB(shape2))
	## diff = rgb2 - rgb1
	
	diff = seg.getBorderBW(shape1,shape2)
	toimage(diff).show()


import scipy
from scipy import ndimage
from scipy import stats
from scipy.misc import toimage
import math
import matplotlib.pyplot as plt
import numpy as np
import colorsys, sys # Image
from PIL import Image, ImageDraw, ImageFont
from scipy.optimize import curve_fit
from scipy.misc import factorial
from Segmentation import *

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
from pybrain.structure import FeedForwardNetwork
import pickle
## from ANN import *

#-----------------------------------------------------------------------

def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None
        
def plotHistogram(arr, b):
    hist, bins = np.histogram(arr, bins=b)
    #width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center') #, width=width)
    plt.show()
    
# http://stackoverflow.com/questions/16373425/add-text-on-image-using-pil 
def showImage(img, text):
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 16)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((10, 10),text) #,font=font,fill=(255,255,255))
    img.show()
   
#-----------------------------------------------------------------------

# Referencias: http://www.scipy-lectures.org/advanced/image_processing/
#  http://gis.stackexchange.com/questions/24827/how-to-smooth-the-polygons-in-a-contour-map
#  http://scikit-image.org
#  https://sites.google.com/site/bustosmerino/home/segmentacion---color-de-piel
        
imgFile = sys.argv[1]
print imgFile
shape1 = (2,2)
shape2 = (6,6)

seg = Segmentation(imgFile)

rgb1 = np.array(seg.erodeRGB(shape1))
rgb2 = np.array(seg.dilateRGB(shape2))

diff = rgb2 - rgb1

seg.rgb2hsv()
seg.erodeHSV(shape2)
seg.dilateHSV(shape1)
seg.statisticalDispersionHSV()
hsv = seg.getHSV()
mask = seg.getHSVmask()
invMask = ~mask
mask[mask != 0xFF] = 0
piel = seg.applyMask2Rgb(mask)
invMask[invMask != 0xFF] = 0
fondo = seg.applyMask2Rgb(invMask)

seg.setRGB(piel)
img1 = np.array(seg.erodeRGB(shape1)) 
img2 = np.array(seg.dilateRGB(shape2)) 
diff2 = img2 - img1

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
ds = SupervisedDataSet(3, 1)
hist = {}
muestra1 = []
muestra2 = []

i = 0
for y in range(seg.height):
	if i > 10:
		break
	for x in range(seg.width):
		r,g,b = piel.getpixel((x,y))
		key = "x%02x%02x%02x" % (r, g, b)
		hist[key] = hist[key] + 1 if key in hist else 0
		
		if (r|g|b and hist[key] == 0) :
			print "%05d (%02x, %02x, %02x)" % (i,r,g,b)
			ds.addSample((r/256, g/256, b/256), (1))
			## ds.append([[r, g, b], [1]])
			muestra1 = [r/256, g/256, b/256]
			i += 1
			
i = 0
for y in range(seg.height):
	if i > 10:
		break
	for x in range(seg.width):
		r,g,b = fondo.getpixel((x,y))
		key = "x%02x%02x%02x" % (r, g, b)
		hist[key] = hist[key] + 1 if key in hist else 0
		
		if (r|g|b and hist[key] == 0) :
			print "%05d (%02x, %02x, %02x)" % (i,r,g,b)
			ds.addSample((r/256, g/256, b/256), (0))
			## ds.append([[r/256, g/256, b/256], [0]])
			muestra2 = [r/256, g/256, b/256]
			i += 1
			

print '#########################'
#http://pybrain.org/docs/api/supervised/trainers.html#pybrain.supervised.trainers.BackpropTrainer
#http://pybrain.org/docs/quickstart/training.html
#http://pybrain.org/docs/tutorial/netmodcon.html#netmodcon
net = buildNetwork(3, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds)
epochs = 5000
threshold = 0.05
error = 1

## trainer.trainUntilConvergence()

while error > threshold:
	error = trainer.train()
	epochs -= 1
	print "%d) e -> %f" % (epochs, error)
	if epochs <= 0:
		break
	

print ("epochs:%d error:%f" % (epochs,error))
print net.activate([muestra1[0], muestra1[1], muestra1[2]])
print net.activate([muestra2[0], muestra2[1], muestra2[2]])

## net = ANN(3, 4, 1, 0.001)
## net.iniciar_perceptron()
## net.entrenar_perceptron(ds, 5000)

## net.clasificar(ds)


#http://stackoverflow.com/questions/6006187/how-to-save-and-recover-pybrain-training
fileObject = open('color-neuralnet2.bkp', 'w')

pickle.dump(net, fileObject)

fileObject.close()



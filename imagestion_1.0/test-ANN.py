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

## from pybrain.tools.shortcuts import buildNetwork
## from pybrain.datasets import SupervisedDataSet
## from pybrain.supervised.trainers import BackpropTrainer
## from pybrain.structure import TanhLayer
import pickle
from ANN import *

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
ds = [] #SupervisedDataSet(3, 1)
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
			muestra1 = [float(r)/256, float(g)/256, float(b)/256]
			print "%05d (%02x, %02x, %02x) => [1] %s" % (i,r,g,b, muestra1)
			## ds.addSample((muestra1[0], muestra1[1], muestra1[2]), (1))
			ds.append([muestra1, [1]])
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
			muestra2 = [float(r)/255, float(g)/255, float(b)/255]
			print "%05d (%02x, %02x, %02x) => [0] %s" % (i,r,g,b, muestra2)
			## ds.addSample((muestra2[0], muestra2[1], muestra2[2]), (0))
			ds.append([muestra2, [0]])
			i += 1
			

print '4.- Training network ############################################'
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
net.iniciar_perceptron()
net.entrenar_perceptron(ds,epochs)

print '5.- Perform segmentation #########################'
## toimage(rgb).show()

## for yy in range(seg.height):
	## for xx in range(seg.width):
		## if (evalPixel(rgb.getpixel((xx,yy)), net) < 0.6) :
			## rgb.putpixel((xx,yy), 0)

im = np.array(rgb)
#im[evalPixel(x, net) < 0.6] = 0
im = [[255 if evalPixel(x, net) > 0.6 else 0 for x in row] for row in im]
r,g,b = rgb.split()
r = Image.fromarray(np.array(r, np.uint8) & np.array(im, np.uint8))
g = Image.fromarray(np.array(g, np.uint8) & np.array(im, np.uint8))
b = Image.fromarray(np.array(b, np.uint8) & np.array(im, np.uint8))
rgb = Image.merge('RGB',(r,g,b))

toimage(rgb).show()

#http://stackoverflow.com/questions/6006187/how-to-save-and-recover-pybrain-training
## fileObject = open('neuralnet-ann.bkp', 'w')

print "write changes? (y/n): "
k = sys.stdin.read(1)
ch = sys.stdin.readline()

if k == 'y':
	print '6.- Store data to file #########################'
	pickle.dump(net, dbFile)
	fileObject.close()
else:
	print 'Changes dismissed'
	




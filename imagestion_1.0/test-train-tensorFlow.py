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

import pickle
import tensorflow as tf

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
        
        
print '1.- Working on image #########################'

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
toimage(piel).show()
## toimage(fondo).show()
## toimage(diff).show()
## toimage(diff2).show()

#-----------------------------------------------------------------------

print '2.- Preparing data set #########################'
	
#https://gist.github.com/pannous/2b8e2e05cf05a630b132
ds = [] # Data set
hist = {}
muestra1 = []
muestra2 = []
outputs = []

i = 0
for y in range(seg.height):
	
	## if i > 10:  # comentar esta linea
		## break   # comentar esta linea
		
	for x in range(seg.width):
		r,g,b = piel.getpixel((x,y))
		key = "x%02x%02x%02x" % (r, g, b)
		hist[key] = hist[key] + 1 if key in hist else 0
		
		if (r|g|b and hist[key] == 0) :
			muestra1 = [float(r)/256, float(g)/256, float(b)/256]
			print "%05d (%02x, %02x, %02x) => %s" % (i,r,g,b, muestra1)
			ds.append(muestra1)
			outputs.append([1,0])
			i += 1
			
i = 0
for y in range(seg.height):
	
	## if i > 10:  # comentar esta linea
		## break   # comentar esta linea
		
	for x in range(seg.width):
		r,g,b = fondo.getpixel((x,y))
		key = "x%02x%02x%02x" % (r, g, b)
		hist[key] = hist[key] + 1 if key in hist else 0
		
		if (r|g|b and hist[key] == 0) :
			muestra2 = [float(r)/256, float(g)/256, float(b)/256]
			print "%05d (%02x, %02x, %02x) => %s" % (i,r,g,b, muestra2)
			ds.append(muestra2)
			outputs.append([0,1])
			i += 1
			
xTrain = np.array(ds)
yTrain = np.array(outputs)

print xTrain
print yTrain

#-----------------------------------------------------------------------
# https://gist.github.com/vinhkhuc/e53a70f9e5c3f55852b0

print '3.- Initialization network #########################'

## http://stackoverflow.com/questions/33759623/tensorflow-how-to-restore-a-previously-saved-model-python€

HIDDEN_NODES = 10
flags = tf.app.flags
FLAGS = flags.FLAGS

# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/mnist/fully_connected_feed.py
# Basic model parameters as external flags.

# Try to find values for W and b that compute y_data = W * x_data + b
# (We know that W should be 0.1 and b 0.3, but Tensorflow will
# figure that out for us.)

x = tf.placeholder(tf.float32, [None, 3])
W_hidden = tf.Variable(tf.truncated_normal([3, HIDDEN_NODES], stddev=1./math.sqrt(3)))
b_hidden = tf.Variable(tf.zeros([HIDDEN_NODES]))
hidden = tf.nn.relu(tf.matmul(x, W_hidden) + b_hidden)

# Try to find values for W and b that compute y_data = W * x_data + b
# (We know that W should be 0.1 and b 0.3, but Tensorflow will
# figure that out for us.)

W_logits = tf.Variable(tf.truncated_normal([HIDDEN_NODES, 2], stddev=1./math.sqrt(HIDDEN_NODES)))
b_logits = tf.Variable(tf.zeros([2]))
logits = tf.matmul(hidden, W_logits) + b_logits

y = tf.nn.softmax(logits)

y_input = tf.placeholder(tf.float32, [None, 2])

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, y_input)
loss = tf.reduce_mean(cross_entropy)

train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

init_op = tf.initialize_all_variables()

saver = tf.train.Saver()
sess = tf.Session()
sess.run(init_op)

# http://stackoverflow.com/questions/33759623/tensorflow-how-to-restore-a-previously-saved-model-python
if os.path.isfile(dbFile) :
	print '3a.- Restore previous session #########################'
	saver.restore(sess, dbFile)

print '4.- Training network #########################'

for i in xrange(1000):
	_, loss_val = sess.run([train_op, loss], feed_dict={x: xTrain, y_input: yTrain})

	if i % 100 == 0:
		print "Step:", i, "Current loss:", loss_val
		for x_input in [muestra1, muestra2]:
			result = sess.run(y, feed_dict={x: [x_input]})
			print "%s => %s" % (x_input, result)

print '5.- Perform segmentation #########################'

# https://www.tensorflow.org/versions/r0.9/get_started/basic_usage.html#tensors
# https://www.tensorflow.org/versions/r0.9/resources/dims_types.html
# https://www.tensorflow.org/versions/r0.9/tutorials/mnist/tf/index.html
# https://www.tensorflow.org/versions/r0.9/tutorials/mnist/pros/index.html
# http://effbot.org/imagingbook/image.htm

for yy in range(seg.height):
	for xx in range(seg.width):
		r,g,b = rgb.getpixel((xx,yy))
		pixel = [float(r)/255, float(g)/255, float(b)/255]
		test  = sess.run(y, feed_dict={x: [pixel]})
		
		if (test[0][0] < 0.6 ) :
			rgb.putpixel((xx,yy), 0)

toimage(rgb).show()

print "write changes? (y/n): "
k = sys.stdin.read(1)
ch = sys.stdin.readline()

if k == 'y':
	print '6.- Store data to file #########################'
	saver.save(sess, dbFile, global_step=None, latest_filename=None, meta_graph_suffix='meta', write_meta_graph=True)
else:
	print 'Changes dismissed'
	
	

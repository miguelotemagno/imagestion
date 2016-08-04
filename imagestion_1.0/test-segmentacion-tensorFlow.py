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
toimage(rgb).show()

#-----------------------------------------------------------------------

print '2.- Initialization network #########################'

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
	print '3.- Restore previous session #########################'
	saver.restore(sess, dbFile)

	print '4.- Perform segmentation #########################'

	# https://www.tensorflow.org/versions/r0.9/get_started/basic_usage.html#tensors
	# https://www.tensorflow.org/versions/r0.9/resources/dims_types.html
	# http://effbot.org/imagingbook/image.htm
	for yy in range(seg.height):
		for xx in range(seg.width):
			r,g,b = rgb.getpixel((xx,yy))
			pixel = [float(r)/255, float(g)/255, float(b)/255]
			test  = sess.run(y, feed_dict={x: [pixel]})
			
			if (test[0][0] < 0.6 ) :
				rgb.putpixel((xx,yy), 0)

	toimage(rgb).show()

	
	

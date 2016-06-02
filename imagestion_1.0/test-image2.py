import scipy
from scipy import ndimage
from scipy.misc import toimage
#import matplotlib.pyplot as plt
import numpy as np
import Image
import sys

# Referencias: http://www.scipy-lectures.org/advanced/image_processing/
#  http://gis.stackexchange.com/questions/24827/how-to-smooth-the-polygons-in-a-contour-map

imgFile = sys.argv[1]
print imgFile


#im = Image.open(imgFile)
#im.show()

shape1 = (3,3)
shape2 = (6,6)

im1 = ndimage.imread(imgFile, flatten=True).astype(np.uint8)
print im1.shape
im2 = ndimage.grey_erosion(im1, size=(shape1)) 
im2 = ndimage.grey_dilation(im2, size=(shape1)) 

im3 = ndimage.grey_dilation(im1, size=(shape2))
#im3 = ndimage.grey_erosion(im3, size=(shape2)) 

diff = im3 - im2
toimage(diff).show()

#im4 = ndimage.grey_erosion(diff, size=(shape1)) 
#im4 = ndimage.grey_dilation(im4, size=(shape1)) 

#im5 = ndimage.grey_dilation(diff, size=(shape2))
#im5 = ndimage.grey_erosion(im5, size=(shape2)) 

#diff2 = im5 - im4

#im4 = ndimage.rotate(diff, 15, mode='constant')
im4 = ndimage.gaussian_filter(diff, 2)
sx = ndimage.sobel(im4, axis=0, mode='constant')
sy = ndimage.sobel(im4, axis=1, mode='constant')
sob = np.hypot(sx, sy)

toimage(sob).show()
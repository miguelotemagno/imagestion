import scipy
from scipy import ndimage
from scipy.misc import toimage
#import matplotlib.pyplot as plt
import numpy as np
import Image
import sys

imgFile = sys.argv[1]
print imgFile


im = Image.open(imgFile)
im.show()
#r,g,b = im.split()

#r = ndimage.binary_dilation(r)
#g = ndimage.binary_dilation(g)
#b = ndimage.binary_dilation(b)

#r = ndimage.binary_erosion(r)
#g = ndimage.binary_erosion(g)
#b = ndimage.binary_erosion(b)

#rgb = Image.merge("RGB", (r,g,b))
#rgb.show()
shape1 = (5,5)
shape2 = (5,5)

im1 = ndimage.imread(imgFile, flatten=True).astype(np.uint8)
print im1.shape
im2 = ndimage.grey_erosion(im1, size=(shape1)) 
im2 = ndimage.grey_dilation(im2, size=(shape1)) 
#toimage(im2).show()

im3 = ndimage.grey_dilation(im1, size=(shape2))
im3 = ndimage.grey_erosion(im3, size=(shape2)) 

diff = im2 - im3

toimage(diff).show()
import scipy
from scipy import ndimage
from scipy.misc import toimage
#from skimage import io, color
import matplotlib.pyplot as plt
import numpy as np
import Image, colorsys, sys


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
    
def drawHistogram(arr, b):
    bins, edges = np.histogram(arr, b, normed=1)
    left,right = edges[:-1],edges[1:]
    X = np.array([left,right]).T.flatten()
    Y = np.array([bins,bins]).T.flatten()
    
    plt.plot(X,Y)
    plt.show()    
    
# Referencias: http://www.scipy-lectures.org/advanced/image_processing/
#  http://gis.stackexchange.com/questions/24827/how-to-smooth-the-polygons-in-a-contour-map
#  http://scikit-image.org
        
imgFile = sys.argv[1]
print imgFile



shape1 = (2,2)
shape2 = (6,6)

im1 = ndimage.imread(imgFile, flatten=True).astype(np.uint8)
print im1.shape
w,h = im1.shape
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
#im4 = ndimage.gaussian_filter(diff, 2)
#sx = ndimage.sobel(im4, axis=0, mode='constant')
#sy = ndimage.sobel(im4, axis=1, mode='constant')
#sob = np.hypot(sx, sy)
#
#toimage(sob).show()


print diff
print np.amin(diff)
print np.amax(diff)

filter = (np.amin(diff) + np.amax(diff)) // 8
print filter

im5 = np.array(diff, np.uint8)
im5[im5 < filter] = 0
#im5[im5 > filter*3] = 255
im5 = ndimage.grey_erosion(im5, size=(shape1)) 
im5 = ndimage.grey_dilation(im5, size=(shape1)) 

im = Image.fromarray(im5)
im6 = Image.merge('RGB',(im,im,im))

toimage(im6).show()

hist = ndimage.measurements.histogram(im6, 0, 255, 256)

print hist

#plotHistogram(im6,256)

img = Image.open(imgFile)
r,g,b = img.split()

R = Image.fromarray(ndimage.grey_dilation(r, size=(shape2)))
G = Image.fromarray(ndimage.grey_dilation(g, size=(shape2)))
B = Image.fromarray(ndimage.grey_dilation(b, size=(shape2)))

rgb = Image.merge('RGB',(R,G,B))
#rgb.show()
#toimage(rgb).show()

hsv = HSVColor(rgb)
#toimage(hsv).show()

#lab = color.rgb2lab(rgb)
#toimage(lab).show()


plotHistogram(R,256)
plotHistogram(G,256)
plotHistogram(B,256)


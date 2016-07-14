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

toimage(seg.maskH).show()
toimage(seg.maskS).show()
toimage(seg.maskV).show()
toimage(hsv).show()
toimage(mask).show()
toimage(invMask).show()
toimage(piel).show()
toimage(fondo).show()
toimage(diff).show()
toimage(diff2).show()

########################################################################

## im1 = ndimage.imread(imgFile, flatten=True).astype(np.uint8)
## print "width:%d x height:%d" % im1.shape
## w,h = im1.shape
## im2 = ndimage.grey_erosion(im1, size=(shape1)) 
## im2 = ndimage.grey_dilation(im2, size=(shape1)) 

## im3 = ndimage.grey_dilation(im1, size=(shape2))
## #im3 = ndimage.grey_erosion(im3, size=(shape2)) 

## diff = im3 - im2
## toimage(diff).show()



## #im4 = ndimage.grey_erosion(diff, size=(shape1)) 
## #im4 = ndimage.grey_dilation(im4, size=(shape1)) 

## #im5 = ndimage.grey_dilation(diff, size=(shape2))
## #im5 = ndimage.grey_erosion(im5, size=(shape2)) 

## #diff2 = im5 - im4

## #im4 = ndimage.rotate(diff, 15, mode='constant')
## #im4 = ndimage.gaussian_filter(diff, 2)
## #sx = ndimage.sobel(im4, axis=0, mode='constant')
## #sy = ndimage.sobel(im4, axis=1, mode='constant')
## #sob = np.hypot(sx, sy)
## #
## #toimage(sob).show()


## #print diff
## print "min:%s , max:%s" % (np.amin(diff),np.amax(diff))
## filter = (np.amin(diff) + np.amax(diff)) // 8
## print "filter: %s " % (filter)

## im5 = np.array(diff, np.uint8)
## im5[im5 < filter] = 0
## #im5[im5 > filter*3] = 255
## im5 = ndimage.grey_erosion(im5, size=(shape1)) 
## im5 = ndimage.grey_dilation(im5, size=(shape1)) 

## im = Image.fromarray(im5)
## im6 = Image.merge('RGB',(im,im,im))

## #toimage(im6).show()

## #hist = ndimage.measurements.histogram(im6, 0, 255, 256)
## #print hist

## #plotHistogram(im6,256)

## img = Image.open(imgFile)
## r,g,b = img.split()

## R = Image.fromarray(ndimage.grey_dilation(r, size=(shape2)))
## G = Image.fromarray(ndimage.grey_dilation(g, size=(shape2)))
## B = Image.fromarray(ndimage.grey_dilation(b, size=(shape2)))

## rgb = Image.merge('RGB',(R,G,B))
## #rgb.show()
## toimage(rgb).show()


## hsv = HSVColor(rgb)
## #toimage(hsv).show()

## H,S,V = hsv.split()

## H = Image.fromarray(ndimage.grey_erosion(H, size=(shape2)))
## S = Image.fromarray(ndimage.grey_erosion(S, size=(shape2)))
## V = Image.fromarray(ndimage.grey_erosion(V, size=(shape2)))

## H = Image.fromarray(ndimage.grey_dilation(H, size=(shape2)))
## S = Image.fromarray(ndimage.grey_dilation(S, size=(shape2)))
## V = Image.fromarray(ndimage.grey_dilation(V, size=(shape2)))

## h1 = np.array(H, np.uint8)
## s1 = np.array(S, np.uint8)
## v1 = np.array(V, np.uint8)

## stH = np.std(h1)
## meH = np.mean(h1)
## mdH = np.ma.median(h1)
## cvH = np.cov(h1)
## print "std H: "+str(stH)
## print "mean H: "+str(meH)
## print "median H: "+str(mdH)
## #print "cov H: "+str(cvH)

## # http://stackoverflow.com/questions/25828184/fitting-to-poisson-histogram
## # http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mstats.mode.html
## stS = np.std(s1)
## meS = np.mean(s1)
## mdS = np.ma.median(s1)
## cvS = np.cov(s1)
## print "std S: "+str(stS)
## print "mean S: "+str(meS)
## print "median S: "+str(mdS)
## #print "cov S: "+str(cvS)

## stV = np.std(v1)
## meV = np.mean(v1)
## mdV = np.ma.median(v1)
## cvV = np.cov(v1)
## print "std V: "+str(stV)
## print "mean V: "+str(meV)
## print "median V: "+str(mdV)
## #print "cov V: "+str(cvV)

## delta = 25
## varH = 20 #math.sqrt(stH)  # :-) funciona!
## print "varH:%s" % (varH)

## h1[h1 <= varH - delta] = 0
## h1[h1 >= varH + delta] = 0
## h1[h1 != 0] = 0x92

## #h1[h1 > 250] = 0x55
## #h1[h1 < 50] = 0x55
## #h1[h1 < 1] = 0
## #h1[h1 != 0x55] = 0

## #varS = 100
## #s1[s1 >= varS + delta] = 0
## #s1[s1 <= varS - delta] = 0
## s1[s1 >= 256*0.6] = 0
## s1[s1 <= 256*0.1] = 0
## s1[s1//2 <= 30] = 0
## s1[s1 != 0] = 0x49

## #v1[v1 <= 256*0.1] = 0
## #v1 = v1//3
## v1[v1 < meV - delta] = 0
## #v1[v1 > meV + delta] = 0
## v1[v1 != 0] = 0x24

## #hs = h1 | s1 
## #hs[hs != 255] = 0
## #hsv2 = hs & v1
## hsv2 = h1 | s1 | v1
## hsv2[hsv2 < 150] = 0

## #showImage(toimage(h1),'H')
## toimage(h1).show()
## toimage(s1).show()
## toimage(v1).show()
## toimage(hsv2).show()

## #mh = stats.mode(h1)
## #print "moda H: "+str(mh)

## #toimage(H).show()
## #toimage(S).show()
## #toimage(V).show()

## #plotHistogram(h1, 256)
## #plotHistogram(H, 256)

## #plotHistogram(s1, 256)
## #plotHistogram(S, 256)
## #
## #plotHistogram(v1, 256)
## plotHistogram(V, 256)

## #plotHistogram(hsv2, 256)

## #http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.normal.html
## #mu, sigma = 0, 0.1 # mean and standard deviation
## #s = np.random.normal(mu, sigma, 1000)
## #abs(mu - np.mean(s)) < 0.01
## #abs(sigma - np.std(s, ddof=1)) < 0.01
## #count, bins, ignored = plt.hist(s, 30, normed=True)
## #plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
## #plt.show()

## # http://stackoverflow.com/questions/10138085/python-pylab-plot-normal-distribution
## #import matplotlib.pyplot as plt
## #import numpy as np
## #import matplotlib.mlab as mlab
## #import math
## #
## #mu = 0
## #variance = 1
## #sigma = math.sqrt(variance)
## #x = np.linspace(-3, 3, 100)
## #plt.plot(x,mlab.normpdf(x, mu, sigma))
## #
## #plt.show()






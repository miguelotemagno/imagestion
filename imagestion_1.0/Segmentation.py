# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL  -  Santiago de Chile           |
# | Licensed under the GNU GPL                                            |
# |                                                                       |
# | Redistribution and use in source and binary forms, with or without    |
# | modification, are permitted provided that the following conditions    |
# | are met:                                                              |
# |                                                                       |
# | o Redistributions of source code must retain the above copyright      |
# |   notice, this list of conditions and the following disclaimer.       |
# | o Redistributions in binary form must reproduce the above copyright   |
# |   notice, this list of conditions and the following disclaimer in the |
# |   documentation and/or other materials provided with the distribution.|
# | o The names of the authors may not be used to endorse or promote      |
# |   products derived from this software without specific prior written  |
# |   permission.                                                         |
# |                                                                       |
# | THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   |
# | "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     |
# | LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR |
# | A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  |
# | OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, |
# | SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      |
# | LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, |
# | DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY |
# | THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   |
# | (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE |
# | OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  |
# |                                                                       |
# +-----------------------------------------------------------------------+
# | Author: Miguel Vargas Welch <miguelote@gmail.com>                     |
# +-----------------------------------------------------------------------+

import colorsys, sys, math
import numpy as np
from scipy import ndimage
from scipy import stats
from scipy.misc import toimage
from PIL import Image

class Segmentation(object):
	
	def __init__(self, pathImage):
		self.imgFile = pathImage
		self.rgb = Image.open(pathImage)
		
		r,g,b = self.rgb.split()
		self.R = r
		self.G = g
		self.B = b
		
		self.hsv = None
		self.H = None
		self.S = None
		self.V = None
		
		self.shape1 = (2,2)
		self.shape2 = (6,6)

		self.stH = None
		self.meH = None
		self.mdH = None
		self.cvH = None

		self.stS = None
		self.meS = None
		self.mdS = None
		self.cvS = None

		self.stV = None
		self.meV = None
		self.mdV = None
		self.cvV = None
		
		self.delta = 25
		self.varH = 20 #math.sqrt(stH)  # :-) funciona!

		self.maskH = None
		self.maskS = None
		self.maskV = None
		self.maskHSV = None
		pass

	### ----------------------------------------------------------------
	
	def setRGB(self, img):
		self.rgb = img
		r,g,b = self.rgb.split()
		self.R = r
		self.G = g
		self.B = b

	### ----------------------------------------------------------------

	def getRGB(self):
		self.rgb = Image.merge('RGB',(self.R,self.G,self.B))
		return self.rgb

	### ----------------------------------------------------------------

	def getHSV(self):
		self.hsv = Image.merge('RGB',(self.H,self.S,self.V))
		return self.hsv		
	
	### ----------------------------------------------------------------

	def HSVColor(self,img):
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
			
	### ----------------------------------------------------------------
	
	def rgb2hsv(self):
		self.hsv = self.HSVColor(self.rgb)
		h,s,v = self.hsv.split()
		self.H = h
		self.S = s
		self.V = v
	
	### ----------------------------------------------------------------
	
	def dilateRGB(self, shape):
		self.R = Image.fromarray(ndimage.grey_dilation(self.R, size=(shape)))
		self.G = Image.fromarray(ndimage.grey_dilation(self.G, size=(shape)))
		self.B = Image.fromarray(ndimage.grey_dilation(self.B, size=(shape)))
		return Image.merge('RGB',(self.R,self.G,self.B))
			
	### ----------------------------------------------------------------
	
	def erodeRGB(self, shape):
		self.R = Image.fromarray(ndimage.grey_erosion(self.R, size=(shape)))
		self.G = Image.fromarray(ndimage.grey_erosion(self.G, size=(shape)))
		self.B = Image.fromarray(ndimage.grey_erosion(self.B, size=(shape)))
		return Image.merge('RGB',(self.R,self.G,self.B))
			
	### ----------------------------------------------------------------
	
	def dilateHSV(self, shape):
		self.H = Image.fromarray(ndimage.grey_dilation(self.H, size=(shape)))
		self.S = Image.fromarray(ndimage.grey_dilation(self.S, size=(shape)))
		self.V = Image.fromarray(ndimage.grey_dilation(self.V, size=(shape)))
		return Image.merge('RGB',(self.H,self.S,self.V))

	### ----------------------------------------------------------------
	
	def erodeHSV(self, shape):
		self.H = Image.fromarray(ndimage.grey_erosion(self.H, size=(shape)))
		self.S = Image.fromarray(ndimage.grey_erosion(self.S, size=(shape)))
		self.V = Image.fromarray(ndimage.grey_erosion(self.V, size=(shape)))
		return Image.merge('RGB',(self.H,self.S,self.V))

	### ----------------------------------------------------------------
	
	def statisticalDispersionHSV(self):
		self.stH = np.std(self.H)
		self.meH = np.mean(self.H)
		self.mdH = np.ma.median(self.H)
		self.cvH = np.cov(self.H)

		self.stS = np.std(self.S)
		self.meS = np.mean(self.S)
		self.mdS = np.ma.median(self.S)
		self.cvS = np.cov(self.S)

		self.stV = np.std(self.V)
		self.meV = np.mean(self.V)
		self.mdV = np.ma.median(self.V)
		self.cvV = np.cov(self.V)

	### ----------------------------------------------------------------
	
	def getHSVmask(self):
		h = np.array(self.H, np.uint8)
		s = np.array(self.S, np.uint8)
		v = np.array(self.V, np.uint8)
		
		h[h <= self.varH - self.delta] = 0
		h[h >= self.varH + self.delta] = 0
		h[h != 0] = 0x92

		s[s >= 256*0.6] = 0
		s[s <= 256*0.1] = 0
		s[s//2 <= 30] = 0
		s[s != 0] = 0x49

		v[v < self.meV + self.delta] = 0
		#v[v > self.meV + self.delta] = 0
		v[v != 0] = 0x24

		hsv = h | s | v
		hsv[hsv < 0x92] = 0
		
		self.maskH = h
		self.maskS = s
		self.maskV = v
		self.maskHSV = hsv
		
		return hsv

	### ----------------------------------------------------------------
	
	def setHSVmask(self, mask):
		h = mask[mask & 0x92]
		s = mask[mask & 0x49]
		v = mask[mask & 0x24]
		self.maskH = h
		self.maskS = s
		self.maskV = v
		self.maskHSV = mask

	### ----------------------------------------------------------------
	
	def applyMask2Rgb(self, mask):
		r = Image.fromarray(self.R & mask)
		g = Image.fromarray(self.G & mask)
		b = Image.fromarray(self.B & mask)
		rgb = Image.merge('RGB',(r,g,b))
		return rgb
		
        

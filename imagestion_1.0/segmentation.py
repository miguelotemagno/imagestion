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
from PIL import Imaget

class Segmentation(object):
	
	def __init__(self, pathImage):
		self.imgFile = pathImage
		self.rgb = ndimage.imread(imgFile, flatten=True).astype(np.uint8)
		self.hsv = None
		self.shape1 = (2,2)
		self.shape2 = (6,6)
		pass

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
        

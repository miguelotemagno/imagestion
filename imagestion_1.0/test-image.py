# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL   - Santiago de Chile           |
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

## http://docs.python.org/reference/index.html
from Imagen import *
from datetime import datetime

## http://luispedro.org/pymorph-apidocs/html/genindex.html

## REALIZAR CAMBIOS EN: 
## sudo gedit /usr/lib/python2.6/dist-packages/PIL/Image.py
## http://hg.effbot.org/pil-2009-raclette/changeset/fb7ce579f5f9
##
# 1494    def split(self):
# 1495        "Split image into bands"
# 1496
# 1497        self.load()
# 1498        if self.im.bands == 1:
# 1499            ims = [self.copy()]
# 1500        else:
# 1501            ims = []
# 1502            for i in range(self.im.bands):
# 1503                ims.append(self._new(self.im.getband(i)))
# 1504        return tuple(ims)


img = Imagen('../imgtest/exp1.jpg')
print 'ancho:', img.getAncho() ,' alto:', img.getAlto()

#r = img.getR()
#g = img.getG()
#b = img.getB()

#r.show()
#g.show()
#b.show()

img.getRGB().show()

#g = img._erode(img.getG())
#G = img._erode(G)
#g = img._dilate(g)

#G.show()

#g.show()

start = datetime.now()

img.dilate()
img.erode()

stop = datetime.now()
delay = stop - start

print delay

img.getRGB().show()

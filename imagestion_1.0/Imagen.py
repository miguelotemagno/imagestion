# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL       - Santiago de Chile       |
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

import Image
import thread
from datetime import datetime

## Referencias apoyo:
## http://www.pythonware.com/library/pil/handbook/introduction.htm
## http://www.pythonware.com/library/pil/handbook/image.htm
## http://www.tutorialspoint.com/python/python_multithreading.htm
## http://ostermiller.org/dilate_and_erode.html

class Imagen(object):
    
    def __init__(self,ruta):
        self.path = ruta
        self.busy = 0
        self.reload()
        pass
        
    def reload(self):
        self.RGB  = Image.open(self.path)
        self.ancho, self.alto  = self.RGB.size
        self.R, self.G, self.B = self.RGB.split()
        pass
        
    def dilate(self):
        self.busy = 1
        
        try:
            R = [self.R, self.R.copy()]
            G = [self.G, self.G.copy()]
            B = [self.B, self.B.copy()]
            thread.start_new_thread( self._dilate, (R, 0, 0, self.alto, self.ancho) )
            thread.start_new_thread( self._dilate, (G, 0, 0, self.alto, self.ancho) )
            thread.start_new_thread( self._dilate, (B, 0, 0, self.alto, self.ancho) )
        except:
            print "Error: unable to start thread dilate"
            self.busy = 0

        while self.busy > 0:
            pass

        self.R = R[1]
        self.G = G[1]
        self.B = B[1]

        print self.busy

    def _dilate(self, lst, y1, x1, y2, x2):
        """

        @return  :
        @author Miguelote 
        """
        id = self.busy
        ancho = x2 - x1
        alto  = y2 - y1

        if ancho > 100 and alto > 100:
            difX = ancho % 2
            difY = alto % 2

            width  = ancho // 2 if(difX > 0) else ancho / 2
            height = alto // 2  if(difY > 0) else alto / 2

            #print [id, '-', alto, ancho, '-', y1,x1, y2,x2]

            try:
                thread.start_new_thread( self._dilate, (lst, y1, x1, y2-height, x2-width) )
                thread.start_new_thread( self._dilate, (lst, y1, x1+width, y2-height, x2) )
                thread.start_new_thread( self._dilate, (lst, y1+height, x1, y2, x2-width) )
                thread.start_new_thread( self._dilate, (lst, y1+height, x1+width, y2, x2) )
            except:
                print "Error: unable to start thread _dilate"
                print [id, alto, ancho]
                print [y1, x1, y2-height, x2-width]
                print [y1, x1+width, y2-height, x2]
                print [y1+height, x1, y2, x2-width]
                print [y1+height, x1+width, y2, x2]
                print self.busy
        else:
            img, copia = lst
            self.busy  = self.busy + 1
            start = datetime.now()
            print [id, '-' ,self.busy, '_dilate' , alto, ancho]
            
            for y in xrange(y1,y2):
                for x in xrange(x1,x2):
                    punto = img.getpixel((x,y))
                    ##norte = im.getpixel((x,y-1))
                    ##sur   = im.getpixel((x,y+1))
                    ##este  = im.getpixel((x+1,y))
                    ##oeste = im.getpixel((x-1,y))

                    if y>0 and punto>img.getpixel((x,y-1)):
                        lst[1].putpixel((x,y-1),punto)

                    if x>0 and punto>img.getpixel((x-1,y)):
                        lst[1].putpixel((x-1,y),punto)

                    if y<self.alto-1 and punto>img.getpixel((x,y+1)):
                        lst[1].putpixel((x,y+1),punto)

                    if x<self.ancho-1 and punto>img.getpixel((x+1,y)):
                        lst[1].putpixel((x+1,y),punto)


                    if y>0 and x>0 and punto>img.getpixel((x-1,y-1)):
                        lst[1].putpixel((x-1,y-1),punto)

                    if y<self.alto-1 and x>0 and punto>img.getpixel((x-1,y+1)):
                        lst[1].putpixel((x-1,y+1),punto)

                    if y>0 and x<self.ancho-1 and punto>img.getpixel((x+1,y-1)):
                        lst[1].putpixel((x+1,y-1),punto)

                    if y<self.alto-1 and x<self.ancho-1 and punto>img.getpixel((x+1,y+1)):
                        lst[1].putpixel((x+1,y+1),punto)

            stop = datetime.now()
            delay = stop - start           
            print [id, '-' ,self.busy, "fin", delay]

            self.busy = self.busy -1
            
            if self.busy == 1:
                 self.busy = 0


    def erode(self):
        self.busy = 1

        try:
            R = [self.R, self.R.copy()]
            G = [self.G, self.G.copy()]
            B = [self.B, self.B.copy()]
            thread.start_new_thread( self._erode, (R, 0, 0, self.alto, self.ancho) )
            thread.start_new_thread( self._erode, (G, 0, 0, self.alto, self.ancho) )
            thread.start_new_thread( self._erode, (B, 0, 0, self.alto, self.ancho) )
        except:
            print "Error: unable to start thread erode"
            self.busy = 0

        while self.busy > 0:
            pass

        self.R = R[1]
        self.G = G[1]
        self.B = B[1]

        print self.busy
        
    def _erode(self, lst, y1, x1, y2, x2):
        """

        @return  :
        @author Miguelote
        """
        id = self.busy
        ancho = x2 - x1
        alto  = y2 - y1

        if ancho > 100 and alto > 100:
            difX = ancho % 2
            difY = alto % 2

            width  = ancho // 2 if(difX > 0) else ancho / 2
            height = alto // 2  if(difY > 0) else alto / 2

            #print [id, '-', alto, ancho, '-', y1,x1, y2,x2]

            try:
                thread.start_new_thread( self._erode, (lst, y1, x1, y2-height, x2-width) )
                thread.start_new_thread( self._erode, (lst, y1, x1+width, y2-height, x2) )
                thread.start_new_thread( self._erode, (lst, y1+height, x1, y2, x2-width) )
                thread.start_new_thread( self._erode, (lst, y1+height, x1+width, y2, x2) )
            except:
                print "Error: unable to start thread _erode"
                print [id, alto, ancho]
                print [y1, x1, y2-height, x2-width]
                print [y1, x1+width, y2-height, x2]
                print [y1+height, x1, y2, x2-width]
                print [y1+height, x1+width, y2, x2]
                print self.busy
        else:
            img, copia = lst
            self.busy  = self.busy + 1
            start = datetime.now()
            print [id, '-' ,self.busy, '_erode' , alto, ancho]
            
            for y in xrange(y1,y2):
                for x in xrange(x1,x2):
                    punto = img.getpixel((x,y))
                    ##norte = im.getpixel((x,y-1))
                    ##sur   = im.getpixel((x,y+1))
                    ##este  = im.getpixel((x+1,y))
                    ##oeste = im.getpixel((x-1,y))

                    if y>0 and punto>img.getpixel((x,y-1)):
                        lst[1].putpixel((x,y),img.getpixel((x,y-1)))
                        
                    if x>0 and punto>img.getpixel((x-1,y)):
                        lst[1].putpixel((x,y),img.getpixel((x-1,y)))
            
                    if y<self.alto-1 and punto>img.getpixel((x,y+1)):
                        lst[1].putpixel((x,y),img.getpixel((x,y+1)))
                        
                    if x<self.ancho-1 and punto>img.getpixel((x+1,y)):
                        lst[1].putpixel((x,y),img.getpixel((x+1,y)))


                    if y>0 and x>0 and punto>img.getpixel((x-1,y-1)):
                        lst[1].putpixel((x,y),img.getpixel((x-1,y-1)))
                        
                    if y>0 and x<self.ancho-1 and punto>img.getpixel((x+1,y-1)):
                        lst[1].putpixel((x,y),img.getpixel((x+1,y-1)))
            
                    if y<self.alto-1 and x>0 and punto>img.getpixel((x-1,y+1)):
                        lst[1].putpixel((x,y),img.getpixel((x-1,y+1)))
                        
                    if y<self.alto-1 and x<self.ancho-1 and punto>img.getpixel((x+1,y+1)):
                        lst[1].putpixel((x,y),img.getpixel((x+1,y+1)))

            stop = datetime.now()
            delay = stop - start           
            print [id, '-' ,self.busy, "fin", delay]

            self.busy = self.busy -1
            
            if self.busy == 1:
                 self.busy = 0

    def rgb2gray(self):
        """
         
        @return  :
        @author Miguelote
        """
        pass

    def substract(self,img):
        
        pass

    def getR(self):
        """
         
        @return int[][] :
        @author Miguelote
        """
        return self.R
        pass

    def getG(self):
        """
         
        @return int[][] :
        @author Miguelote
        """
        return self.G
        pass

    def getB(self):
        """
         
        @return int[][] :
        @author Miguelote
        """
        return self.B
        pass

    def getRGB(self):
        """
         
        @return int[][][3] :
        @author Miguelote
        """
        self.RGB = Image.merge("RGB", (self.R, self.G, self.B))
        return self.RGB
        pass

    def getAlto(self):
        return self.alto
        pass

    def getAncho(self):
        return self.ancho
        pass
    
    def getPath(self):
        return self.path
        pass

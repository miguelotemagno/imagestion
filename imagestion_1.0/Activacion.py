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

import math
from sys import *

class Activacion(object):

    """
    funciones de activacion para la simulacion y entrenamiento
    de un perceptron

    :version: 1.0
    :author:  Miguelote
    """

    def __init__(self,type):
        self.padre = None
        self.tipo = type
        self.funciones = {
            "HARDLIM"   : "self.hardlim(expr)",
            "HARDLIMS"  : "self.hardlims(expr)",
            "POSLIN"    : "self.poslin(expr)",
            "PURELIN"   : "self.purelin(expr)",
            "SATLIN"    : "self.satlin(expr)",
            "SATLINS"   : "self.satlins(expr)",
            "LOGSIG"    : "self.logsig(expr)",
            "TANSIG"    : "self.tansig(expr)",
            "RADBAS"    : "self.radbas(expr)",
            "UNDEFINED" : "self.undefined(expr)"
        }
        self.derivadas = {
            "LOGSIG"    : "self.logsig_derivada(expr)",
            "TANSIG"    : "self.tansig_derivada(expr)",
            "PURELIN"   : "self.purelin_derivada(expr)",
            "POSLIN"    : "self.poslin_derivada(expr)",
            "RADBAS"    : "self.undefined(expr)",
            "UNDEFINED" : "self.undefined(expr)"
        }
        pass
    
    def exe(self,val):
        valor   = None
        funcion = self.funciones[self.tipo].replace('expr',str(val))
        exec "valor = "+funcion
        return valor
        pass
        
    def train(self,val):
        valor   = None
        funcion = self.derivadas[self.tipo].replace('expr',str(val))
        exec "valor = "+funcion
        return valor
        pass
        
    def hardlim(self,val):
        return 0.0 if val < 0.0 else 1.0
        pass
        
    def hardlims(self,val):
        return -1.0 if val < 0.0 else 1.0
        pass
        
    def poslin(self,val):
        return 0.0 if val < 0.0 else val
        pass
        
    def purelin(self,val):
        return val
        pass
        
    def satlin(self,val):
        return 0.0 if val < 0.0 else 1.0 if val > 1.0 else val
        pass
        
    def satlins(self,val):
        return -1.0 if val < -1.0 else 1.0 if val > 1.0 else val
        pass
        
    def logsig(self,val):
        try:
            return 1.0 / (1.0 + math.exp(-val))
        except:
            err = str(exc_info())            
            print 'ERROR logsig('+str(val)+'):'+err
            return 0.0
        
    def tansig(self,val):
        #valor = (exp(val) - exp(-val)) / (exp(val) + exp(-val))      
        #return self.satlin(valor)    # Corregir que valores devueltos no se disparen durante entrenamiento
        return math.tanh(val)
        
    def radbas(self,val):
        pass
        
    def logsig_derivada(self,val):
        valor = val * (1.0 - val)
        #return valor 
        return self.satlin(valor)    # Corregir que valores devueltos no se disparen durante entrenamiento
        pass
        
    def tansig_derivada(self,valor):
        val = valor #self.tansig(valor)
        return 1 - val**2
        pass
        
    def poslin_derivada(self,val):
        return 1.0
        pass
        
    def purelin_derivada(self,val):
        return 1.0
        pass
        
    def undefinded(self,val):
        return None
        pass
        
    def addLog(self,str):
        if self.padre != None :
            if self.padre.debug :
                self.padre.addLog(str)    
        



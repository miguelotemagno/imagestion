# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL - Santiago de Chile             |
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

from Activacion import *
import json
import random

class Perceptron(object):

    """
    :version: 1.0
    :author:  Miguelote
    """

    def __init__(self,name,inputs,funcion,padre,capa):
        self.entradas = [0 for x in range(inputs)] 
        self.nInputs  = inputs
        self.name     = name
        self.padre    = padre
        self.capa     = capa
        self.delta    = 0.0
        self.error    = 0.0
        self.funcion  = funcion
        self.fnTransf = Activacion(funcion)
        self.fnTransf.padre = padre
        self.expect   = 0
        self.reInit()
        pass
    
    def reInit(self):
        min, max = (self.padre.min,self.padre.max)
        self.pesos    = [random.uniform(min, max) for x in range(self.nInputs)]
        self.wBias    = random.uniform(min, max) #if self.capa==0 else 1.0        
        self.bias     = 1.0
        self.salida   = 1.0
       
    def getSumPesosEntradas(self):
        i    = 0
        suma = 0.0
        
        try:
            for i in range(len(self.entradas)):
                suma += self.entradas[i] * self.pesos[i]
                #self.padre.addLog(">> nodo[%s].neta:%f += i[%d]:%f * w[%d]:%f" % (self.name,suma,i,self.entradas[i],i,self.pesos[i]))
            pass
            
        except:
            err = exc_info()[0]
            self.addLog ("ERROR en Perceptron.getSumPesosEntradas() - Iteracion i="+str(i))
            self.addLog (err)
        
        if self.padre.layers[self.capa].isHidden:
            suma += self.bias * self.wBias
            
        self.neta = suma 

        return self.neta
        
    def calcular(self):
        #self.addLog("Perceptron.calcular(name:"+self.name+", entradas:"+str(self.entradas)+')')
        suma = self.getSumPesosEntradas()
        res  = self.fnTransf.exe(suma)
        self.padre.addLog(">> res:%f = %s(%f)" % (res,self.fnTransf.funciones[self.fnTransf.tipo],suma))
        self.salida = res

        return res

    """
    # setDelta
    # 
    #  Al comparar la senal de salida con una respuesta deseada o salida objetivo,
    #  d(t), se produce una senal de error, e(t), energia de error. Senal de error
    #  en la neurona de salida j en la iteracion t
    #          e(t)=d(t) - y(t)
    #  donde t denota el tiempo discreto, y(t) representa la salida de la capa previa.
    # 
    #  Regla Delta Generalizada Es una extension de la regla delta propuesta por Widrow (1960).
    #  Se usa en redes con capas intermedias con conexiones hacia delante y cuyas celulas
    #  tienen funciones de activacion continuas. Estas funciones continuas son no decrecientes
    #  y derivables (la funcion sigmoidal pertenece a este tipo de funciones).
    #
    """         
    def setDelta(self, val):
        self.delta = val
    
    """
    #  getErrorDelta
    #             error = error + delta_salida[0..k] * pesos_sal[j][0..k]
    #             delta_oculto[j] = fnSigmoidal(entrada_ocu[j]) * error
    #
    """
         
    def getErrorDelta(self, delta):
        self.delta = delta
        error = self.fnTransf.train(self.salida) * self.delta
        self.error = error
        self.padre.addLog(">> errorDelta:%f = %s(%f) * %f" % (self.error,self.fnTransf.derivadas[self.fnTransf.tipo],self.salida,self.delta))
        return self.error
     
    def getCoeficiente(self,i):
        try:
            coef = self.pesos[i] * self.delta
            self.padre.addLog(">> nodo[%s].peso(%d).getCoeficiente: %f = w:%f * d:%f ; Layer.id:%d" % (self.name,i,coef,self.pesos[i],self.delta,self.capa))
            return coef
        except:
            err = exc_info()
            self.padre.addLog("ERROR Perceptron.getCoeficiente(%d): Layer.id:%d" % (i,self.capa))
            self.padre.panic = True 
            self.padre.addLog(str(err)+" - "+str(self.getConfiguracion()))
            raise err
    
    def setBias(self, rate):
        self.wBias += rate * self.delta
        pass
    
    def setSalida(self,salida):
        self.salida = salida

        
    def setPeso(self,idx,peso):
        self.pesos[idx] = peso
        pass
        
    def getPeso(self,idx):
        return self.pesos[idx]
    
    def getEntrada(self,idx):
        return self.entradas[idx]
    
    def getPesos(self):
        pesos = self.pesos
        return pesos    
        
    def setEntradas(self,inputs):
        for n in range(len(inputs)):
            self.entradas[n] = inputs[n]
        pass
        

    def addLog(self,str):
        if self.padre.debug :
            self.padre.addLog(str)
        
    def getConfiguracion(self):
        data = {
            'name':self.name,
            'capa':self.capa,
            'error':self.error,
            'nInputs':self.nInputs,
            'funcion':self.funcion,
            'entradas':self.entradas,
            'salida':self.salida,
            'delta':self.delta,
            'pesos':self.pesos,
            'bias':self.bias,
            'wBias':self.wBias

        }

        return data
    
    def setConfiguracion(self,data):
        self.name = data['name']
        self.capa = data['capa']
        self.error = data['error']
        self.funcion = data['funcion']
        self.entradas = data['entradas']
        self.salida = data['salida']
        self.delta = data['delta']
        self.pesos = data['pesos']
        self.nInputs = data['nInputs']
        self.bias = data['bias']
        self.wBias = data['wBias']
                    
    def printLog(self):
        #print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))
        pass

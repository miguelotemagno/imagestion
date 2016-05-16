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

from Perceptron import *
from random import *
from json import *
from sys import *

class Layer(object):
    def __init__(self,capa,neurons,inputs,function,layers,padre):
        self.error    = 0.0
        #self.deltas   = [0.0] * neurons
        self.id       = capa
        self.cant     = neurons
        self.layers   = layers
        self.padre    = padre
        self.nodos    = [Perceptron(str(capa)+'x'+str(x),inputs,function,padre,capa) for x in xrange(neurons)]
        self.isInput  = True if capa == 0 else False
        self.isOutput = True if capa == padre.nCapas - 1 else False
        #self.isHidden = True if capa > 0 and not self.isOutput else False
        self.isHidden = True if not self.isOutput else False
        self.bias     = Perceptron(str(capa)+'xBias',inputs,function,padre,capa) if self.isHidden else None
        pass
      
    def getDeltas(self):
        deltas = [self.nodos[x].error for x in xrange(self.cant)]
        if self.isHidden:
            deltas.append(self.bias.error)
            
        return deltas
        
    def setDeltas(self,expect,result):
        self.addLog("Layer->setDeltas("+str(expect)+","+str(result)+") Layer:"+str(self.id))
        self.error = 0.0
        post = self.id + 1
        prev = self.id -1
        capa = self.id
        #  error = error + delta_salida[0..k] * pesos_sal[j][0..k]   ;   delta_oculto[j] = fnSigmoidal(entrada_ocu[j]) * error   

        try:
            # capa salida
            if self.isOutput:
                self.addLog(">> CAPA SALIDA Layer:"+str(capa))
                
                for k in range(self.cant):
                    self.nodos[k].delta = expect[k] - result[k]
                    #self.nodos[k].getErrorDelta()
                    
                    self.addLog(">> nodo[%s].delta:%f = r:%f - o:%f" % (self.nodos[k].name,self.nodos[k].delta,expect[k],result[k]))
                    self.addLog(">> output.error = "+str(self.nodos[k].delta))         
                    
            if self.isHidden:
            # capas ocultas
                self.addLog(">> CAPA OCULTA Layer:"+str(capa))
                for j in range(self.cant):
                    self.error = self.bias.getCoeficiente(j) if self.bias else 0.0
                    size = self.layers[post].cant
                    for k in range(size):
                        delta = self.layers[post].nodos[k].delta
                        peso  = self.nodos[j].getPeso(k)
                        self.error += delta * peso
                        self.addLog(">> nodo[%s].delta:%f = d:%f * w:%f" % (self.nodos[j].name,self.error,delta,peso))
                        #self.layers[capa].nodos[k].getErrorDelta()
                        self.addLog(">> error += "+str(self.error))
                    
                    self.nodos[j].delta = self.error
                    #self.nodos[j].getErrorDelta()
                    self.addLog("<< hidden.error = "+str(self.nodos[j].error))         
                    
                if self.bias:   
                    self.bias.delta = self.error
                    #self.bias.getErrorDelta()
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setDeltas(%s,%s): Layer.id:%d" % (str(expect),str(result),self.id))
            self.padre.panic = True 
            self.padre.addLog(str(err)+" - "+str(self.getConfiguracion()))
            raise err
        pass
            
    def setPesos(self,rate):
        self.addLog("Layer->setPesos("+str(rate)+") Layer:"+str(self.id))
        post = self.id + 1
        prev = self.id - 1
        capa = self.id
        
        try:        
            for k in range(self.cant):
                for j in range(self.nodos[k].nInputs):
                    #cambio = delta_oculto[post] * act_ent[capa] ; delta_salida[post] * act_ocu[capa]
                    self.nodos[k].getErrorDelta()
                    error   = self.nodos[k].error
                    entrada = self.nodos[k].getEntrada(j)
                    peso    = self.nodos[k].getPeso(j)
                    self.nodos[k].setPeso(j, peso + rate*error*entrada)
                    self.addLog(">> nodo[%s].peso[%d]:%f = w:%f + l:%f * e:%f * i:%f  ;  l*e*i:%f" % (self.nodos[k].name, j, self.nodos[k].getPeso(j), peso, rate, error, entrada, rate*error*entrada))  
                    if self.bias:
                        self.bias.getErrorDelta()
                        cambio = self.bias.error * self.bias.entradas[j]
                        peso = self.bias.getPeso(j)
                        self.bias.setPeso(j, peso + rate*cambio)
                        
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setPesos(%d): Layer.id:%d" % (rate,self.id))
            traceback.print_stack()
            self.padre.addLog(str(err)+" - "+str(self.getConfiguracion()))
            self.padre.panic = True 
            raise err
        pass

	def setWeight(self, x, y, value):
        post = self.id + 1
        prev = self.id - 1
        capa = self.id
		pass

	def setDelta(self, x, y, value):
        post = self.id + 1
        prev = self.id - 1
        capa = self.id
		pass

	def getWeigth(self, x, y):
        post = self.id + 1
        prev = self.id - 1
        capa = self.id
		self.layers[post].nodos[x].getPeso(y)
		pass

	def getDelta(self, x, y):
        post = self.id + 1
        prev = self.id - 1
        capa = self.id
		self.layers[post].nodos[x].error(y)
		pass
		
    def addLog(self,str):
        if self.padre.debug :
            self.padre.addLog(str)

    def getConfiguracion(self):
        capa = {
            'id'       : self.id,
            'error'    : self.error,
            'isInput'  : self.isInput,
            'isHidden' : self.isHidden,
            'isOutput' : self.isOutput,
            'cant'     : self.cant,
            'bias'     : self.bias.getConfiguracion() if self.bias != None else [],
            'nodos'    : [
                self.nodos[x].getConfiguracion() 
                for x in xrange(self.cant)
            ]
        }
        return capa
    
    def setConfiguracion(self,data):
        self.id     = data['id']
        self.error  = data['error']
        self.cant   = data['cant']
        self.bias   = Perceptron( data['bias']['name'],
                        data['bias']['nInputs'],
                        data['bias']['funcion'],
                        self.padre,
                        self.id) if data['bias'] else []
        self.bias.setConfiguracion(data['bias'])
        self.nodos = [
            Perceptron( data['nodos'][x]['name'],
                        data['nodos'][x]['nInputs'],
                        data['nodos'][x]['funcion'],
                        self.padre,
                        self.id
            ) for x in xrange(data['cant'])
        ]
        for x in xrange(data['cant']):
            self.nodos[x].setConfiguracion(data['nodos'][x])
        pass
        

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
        self.error = 0.0
        self.deltas = [0.0] * neurons
        self.id = capa
        self.cant = neurons
        self.layers = layers
        self.padre = padre
        self.nodos = [Perceptron(str(capa)+'x'+str(x),inputs,function,padre,capa) for x in xrange(neurons)]
        pass
      
    def getPeso(self, i, j):
        capa = self.id
        post = capa + 1
        prev = capa -1
        return self.layers[post].nodos[i].getPeso(j)
        pass
        
    def setPeso(self, i, j, value):
        capa = self.id
        post = capa + 1
        prev = capa -1
        self.layers[post].nodos[i].setPeso(j, value)
        pass
        
    def getEntrada(self, x, y):
        pass
        
    def getDeltas(self):
        return self.deltas
        
    def setDeltas(self,expect,result):
        self.addLog("Layer->setDeltas("+str(expect)+","+str(result)+") capa:"+str(self.id))
        post = self.id + 1
        prev = self.id -1
        capa = self.id

        # capa salida
        if self.id == len(self.layers) -1:
            self.addLog(">> capa salida ID:"+str(self.id))
            self.error = 0.0
            
            for k in xrange(self.cant):
                delta = expect[k] - result[k]
                self.nodos[k].setError(delta)
                self.deltas[k] = self.nodos[k].getErrorDelta()
                self.nodos[k].setDelta(self.deltas[k])
                self.error += self.deltas[k]
                
                self.addLog(">> "+str(self.deltas[k])+" = "+str(expect[k])+" - "+str(result[k]))            
        else:  
        # capas ocultas
            self.addLog(">> capa oculta ID:"+str(self.id))
            self.error = 0.0
            for j in xrange(self.cant):
                error = 0.0
                
                for k in xrange(self.layers[post].cant):
                    peso = self.layers[post].nodos[k].getPeso(j)
                    delta = self.layers[post].deltas[k]
                    error += delta * peso
                    self.error += delta * peso
                    
                    self.addLog(">> nodo["+str(j)+"].peso["+str(k)+"]: "+str(self.error)+" += "+str(delta)+"*"+str(peso))
                
                self.nodos[j].setError(error)                
                #self.deltas[j] = self.nodos[j].fnTransf.train(self.nodos[j].getSalidaNeta()) * error
                self.deltas[j] = self.nodos[j].getErrorDelta()
                self.nodos[j].setDelta(self.deltas[j])   
            pass
            
    def setPesos(self,rate):
        self.addLog("Layer->setPesos("+str(rate)+") capa:"+str(self.id))
        post = self.id + 1
        prev = self.id - 1
        
        for k in xrange(self.cant):
            for j in xrange(self.nodos[k].nInputs):
                cambio = self.deltas[k] * self.nodos[k].entradas[j]
                peso = self.nodos[k].getPeso(j)
                self.nodos[k].setPeso(j, peso + rate*cambio)
                self.addLog(">> nodo["+str(k)+"].peso["+str(j)+"]: "+str(peso)+
                            " + "+str(rate)+"*"+str(cambio)+" = "+str(self.nodos[k].getPeso(j))+
                            "   diff("+str(rate*cambio)+")")
                if self.id == 0:
                    cambio = self.deltas[k] * self.nodos[k].entradas[j]
                    peso = self.nodos[k].getwBias()
                    self.nodos[k].setwBias(peso + rate*cambio)
                    self.addLog(">> nodo["+str(k)+"].wBias: "+str(peso)+
                                " + "+str(rate)+"*"+str(cambio)+" = "+str(self.nodos[k].getwBias())+
                                "   diff("+str(rate*cambio)+")")
                

    def getStrDeltas(self):
        return {'layer_'+str(self.id) : [
                self.nodos[x].getConfiguracion() 
                for x in xrange(self.cant)
            ]}
            
    def addLog(self,str):
        if self.padre.debug :
            self.padre.addLog(str)

    def getConfiguracion(self):
        capa = {
            'id'     : self.id,
            'error'  : self.error,
            'deltas' : self.deltas,
            'cant'   : self.cant,
            'nodos'  : [
                self.nodos[x].getConfiguracion() 
                for x in xrange(self.cant)
            ]
        }
        return capa
    
    def setConfiguracion(self,data):
        self.id = data['id']
        self.error = data['error']
        self.cant = data['cant']
        self.deltas = data['deltas']
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
        
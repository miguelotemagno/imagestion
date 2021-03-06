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

from Activacion import *
from Perceptron import *
from random import *
from json import *
from sys import *
import random

class Layer(object):
    def __init__(self,capa,neurons,inputs,function,layers,padre):
        self.func     = Activacion(function)
        self.error    = 0.0
        self.deltas   = [0.0] * neurons
        self.id       = capa
        self.cant     = neurons
        self.layers   = layers
        self.padre    = padre
        self.nodos    = [Perceptron(str(capa)+'x'+str(x),inputs,function,padre,capa) for x in range(neurons)]
        self.isInput  = True if capa == 0 else False
        self.isOutput = True if capa == padre.nCapas - 1 else False
        #self.isHidden = True if capa > 0 and not self.isOutput else False
        self.isHidden = True if not self.isOutput else False
        weights = inputs + 1 if self.isHidden else inputs
        self.wMatrix  = [] 

        for y in range(neurons):
            self.wMatrix.append([random.uniform(padre.min, padre.max) for x in range(weights)])
        pass
    
    def reInit(self):
        for x in range(self.cant):
            self.nodos[x].reInit()
      
    def getDeltas(self):
        self.deltas = [self.nodos[x].error for x in range(self.cant)]
        if self.isHidden:
            self.deltas.append(self.bias.error)
            
        return self.deltas
        
    def setDeltas(self,expect,result):
        self.addLog("Layer->setDeltas("+str(expect)+","+str(result)+") Layer:"+str(self.id))
        post = self.id + 1
        prev = self.id - 1
        capa = self.id

        try:
            k = None
            # capa salida
            if self.isOutput:
                self.addLog(">> CAPA SALIDA Layer:"+str(capa))
                nodosSalida = self.cant
                # error = objetivo[k] - act_sal[k]
                # delta_salida[k] = dsigmoide(act_sal[k]) * error
                for j in range(nodosSalida):
                    error = expect[j] - result[j]   
                    error = self.func.tansig_derivada(result[j]) * error   #self.nodos[j].getErrorDelta(error)
                    self.setDelta(capa,j, error)
                    self.addLog(">> nodo[%s].delta:%f = r:%f - o:%f" % (self.nodos[j].name,self.getDelta(capa,j),expect[j],result[j]))
                    self.addLog(">> output.error = %f" % (self.nodos[j].delta))
                    
            if self.isHidden:
            # capas ocultas
                self.addLog(">> CAPA OCULTA Layer:"+str(capa))
                nodosOculto = self.cant
                nodosSalida  = self.layers[post].cant
                # error = error + delta_salida[0..k] * pesos_sal[j][0..k]
                # delta_oculto[j] = fnSigmoidal(entrada_ocu[j]) * error
                for j in range(nodosOculto):
                    error = 0.0
                    for k in range(nodosSalida):
                        delta = self.getDelta(post,k) 
                        error = self.getWeightBias(capa,j) * delta if error == 0.0 else error
                        peso  = self.getWeight(capa,j,k) 
                        error += delta * peso
                        self.addLog(">> nodo[%s].delta:%f = d:%f * w:%f" % (self.nodos[j].name, error, delta, peso))
                        self.addLog(">> error += "+str(self.error))
                    
                    error = self.func.tansig_derivada(self.getOutput(capa,j)) * error   #self.nodos[j].getErrorDelta(error)
                    self.setDelta(capa,j, error)
                    self.addLog("<< hidden.error = %f" % (self.getDelta(capa,k)))                             
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setDeltas(%s,%s): Layer.id:%d ; j:%d ; k:%d" % (str(expect),str(result),self.id,j,k))
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
            nodosSalida = self.cant
            # pesos_sal[j][k] = pesos_sal[j][k] + rate * delta_salida[k] * act_ocu[j]
            # pesos_ent[i][j] = pesos_ent[i][j] + rate * delta_oculto[j] * act_ent[i]
            for k in range(nodosSalida):
                nodosOculto = self.nodos[k].nInputs
                error = self.getDelta(capa,k)
                if self.isHidden:
                    wBias  = self.getWeightBias(capa,k)
                    cambio = error * rate * wBias
                    self.addLog(">> nodo[%s].wBias += wb:%f * d:%f * l:%f" % (self.getNodeName(capa,k),wBias,error,rate))
                    self.setWeightBias(capa,k, wBias + cambio)
                for j in range(nodosOculto):
                    salida = self.getInput(capa,k,j) if self.isInput else self.getOutput(prev,j)
                    peso   = self.getWeight(capa,k,j)
                    cambio = rate * error * salida
                    self.setWeight(capa,k,j, peso + cambio)
                    self.addLog(">> nodo[%s].peso[%d]:%f = w:%f + l:%f * e:%f * i:%f  ;  l*e*i:%f" % (self.getNodeName(capa,k), j, self.getWeight(capa,k,j), peso, rate, error, salida, cambio))  
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setPesos(%d): Layer.id:%d" % (rate,self.id))
            self.padre.addLog(str(err)+" - "+str(self.getConfiguracion()))
            self.padre.panic = True 
            raise err
        pass

    def inputsNextLayer(self):
        if self.isOutput:
            return 0
        else:
            post = self.id + 1
            return self.layers[post].cant
            
    def setWeight(self, z, y, x, value):
        self.layers[z].nodos[y].setPeso(x,value)
        pass

    def setDelta(self, z, y, value):
        try:
            #self.layers[z].nodos[y].delta = value
            self.layers[z].deltas[y] = value
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setDelta(%d,%d,%d): Layer.id:%d" % (z,y,value,self.id))
            self.padre.panic = True 
            raise err


    def getWeight(self, z, y, x):
        try:
            #self.padre.addLog("Layer.getWeight(%d,%d): Layer.id:%d" % (y,x,z))
            return self.layers[z].nodos[y].getPeso(x)
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getWeight(%d,%d,%d): Layer.id:%d" % (z,y,x,self.id))
            self.padre.panic = True 
            raise err
    
    def getWeightBias(self, z, y):
        try:
            return self.layers[z].nodos[y].wBias
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getWeightBias(%d,%d): Layer.id:%d" % (z,y,self.id))
            self.padre.panic = True 
            raise err
            
    def setWeightBias(self, z, y, value):
        try:
            self.layers[z].nodos[y].wBias = value
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.setWeightBias(%d,%d,%f): Layer.id:%d" % (z,y,value,self.id))
            self.padre.panic = True 
            raise err
            
    def getDelta(self, z, y):
        try:
            #self.padre.addLog("Layer.getDelta(%d): Layer.id:%d" % (y,z))
            return self.layers[z].deltas[y]
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getDelta(%d,%d): Layer.id:%d" % (z,y,self.id))
            self.padre.panic = True 
            raise err

    def getInput(self, z, y, x):
        try:
            return self.layers[z].nodos[y].getEntrada(x)
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getInput(%d,%d,%d): Layer.id:%d" % (z,y,x,self.id))
            self.padre.panic = True 
            raise err

    def getOutput(self, z, y):
        try:
            return self.layers[z].nodos[y].salida
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getOutput(%d,%d): Layer.id:%d" % (z,y,self.id))
            self.padre.panic = True 
            raise err
            
    def getNodeName(self,z,y):
        try:
            return self.layers[z].nodos[y].name
        except:
            err = exc_info()
            self.padre.addLog("ERROR Layer.getNodeName(%d,%d): Layer.id:%d" % (z,y,self.id))
            self.padre.panic = True 
            raise err

            
    def addLog(self,str):
        if self.padre.debug :
            self.padre.addLog(str)

    def getConfiguracion(self):
        capa = {
            'id'       : self.id,
            'error'    : self.error,
            'deltas'   : self.deltas,
            'isInput'  : self.isInput,
            'isHidden' : self.isHidden,
            'isOutput' : self.isOutput,
            'cant'     : self.cant,
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

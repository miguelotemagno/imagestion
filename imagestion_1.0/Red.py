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
import json
from Perceptron import *
from Layer import *
from random import *
from sys import *

class Net(object):

    """
    :version: 1.0
    :author:  Miguelote
    """

    #Ejemplo:
    #net = Net(2,1,[2,1],['TANSIG','TANSIG'])
    #net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])
    def __init__(self,entradas,salidas,layers,funciones):
        ####################
        self.debug    = False
        ####################
        self.nCapas   = len(layers)
        self.capas    = layers
        self.log      = []
        self.layers   = []        
        self.layers   = [None] * self.nCapas
        self.neuronas = 0
        self.rate     = 0.5
        self.entradas = entradas
        self.salidas  = salidas
        self.transferencias = funciones
        self.epochs   = None
        self.panic    = False
        self.expect   = []
        self.historial = []
        self.error    = 0.0
        self.capaMax  = 0
        self.umbralError = 0.1
        max,size      = 0,0
                
        for i in xrange(self.nCapas):
            inputs = entradas if i == 0 else layers[i-1]
            size   = layers[i]
            max    = size if size > max else max
            
            self.layers[i] = Layer(i,size,inputs,funciones[i],self.layers,self)
            self.neuronas += size
            self.capaMax = max
        pass

    """
    /**
    * simular
    * 
    * @param inputs
    * @return Double[]
    * 
    * Propagacion hacia adelante del la red neuronal, devolviendo una salida
    * en funcion de los argumentos de entrada.
    * 
    * Mas detalle en profundidad visitar:
    * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
    **/
    """
    def simular(self,inputs):
        self.addLog("Red.simular -> inputs:"+str(inputs))
        outputs  = [None] * self.salidas
        sinapsis = [None] * (self.nCapas + 1)
        i,j,n = 0,0,0
        
        for i in xrange(1,self.nCapas+1):
            sinapsis[i]   = [1.0] * (self.layers[i-1].cant)

        sinapsis[0] = inputs
        
        try:
            for i in xrange(self.nCapas):            
                for j in xrange(self.layers[i].cant):
                    self.layers[i].nodos[j].setEntradas(sinapsis[i])
                    sinapsis[i+1][j] =  self.layers[i].nodos[j].calcular();
                    
            outputs = sinapsis[self.nCapas]
        except:
            err = str(exc_info())
            self.addLog("ERROR en Red.simular('"+str(err)+"') Iteracion i="+str(i)+" j="+str(j)+" n="+str(n))
            self.addLog(err)
            self.addLog(str(sinapsis))
            self.panic = True
            pass
            
        self.addLog("<< "+str(outputs))
        return outputs
        
    """
    /** 
     * entrenar
     *
     * Estructura y aprendizaje:
     * - Capa de entrada con n neuronas.
     * - Capa de salida con m neuronas.
     * - Al menos una capa oculta de neuronas.
     * - Cada neurona de una capa recibe entradas de todas las
     *   neuronas de la capa anterior y envia su salida a todas
     *   las neuronas de la capa posterior. No hay conexiones
     *   hacia atras ni laterales entre neuronas de la misma capa.
     *
     * Mas detalle en profundidad visitar:
     * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
     **/    
    """
    
    ##    Ejemplo
    ##    net.entrenar([
    ##            [0.0,0.0], [0.0,1.0], [1.0,0.0], [1.0,1.0]
    ##        ],[
    ##            [0.0], [1.0], [1.0], [0.0]
    ##        ])

    def entrenar(self,inputs,outputs):
        self.addLog("Net.entrenar -> inputs:"+str(inputs)+"\n outputs:"+str(outputs))
        self.expect = outputs
        idx = 0
        minimo = 1
        
        # paso 1: Se inicializan los pesos de todas las neuronas con valores
        #         aleatorios rango [0..1]
        #         N <= {[in1,in2,...,inN] [entrada2...]}
        epochs = self.epochs if self.epochs != None else len(inputs) 
        self.addLog("PASO 1: Se inicializan los pesos de todas las neuronas con valores aleatorios rango [0..1]")
        self.addLog(">> epochs:"+str(epochs)+' idx=len(inputs[0]):'+str(len(inputs[0])))
        
        try:
            for ciclo in range(epochs):
                self.addLog(">> ciclo:"+str(ciclo)+" ====================================================================================================================")
                salidas = [[None] * len(outputs[0])] * len(outputs)
                self.error = 0.0

                ## [[0.0,0.0], [0.0,1.0], [1.0,0.0], [1.0,1.0]]
                for idx in range(len(inputs)):
                    # paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de
                    #         entrenamiento, aplicando el vector de entrada a la entrada de la red.
                    self.addLog('>> idx:'+str(idx)+' -------------------------------------------------------------------------------------------------------')
                    self.addLog("PASO 2: Seleccionar el siguiente par de entrenamiento para el vector de entrada a la red.")
                    
                    datos = [None] * len(inputs[idx])
                    
                    for i in range(len(inputs[idx])):
                        datos[i] = inputs[idx][i]
                    
                    # paso 3: Calcular salida de la red    
                    resultado = self.simular(datos)
                    
                    self.addLog("PASO 3: Calcular salida de la red")
                    self.addLog(">> datos:"+str(datos)+" resultado:"+str(resultado)+" size:"+str(len(resultado))+" salidas:"+str(salidas))
                    
                    for i in range(len(salidas[idx])):
                        self.addLog('>> salidas['+str(idx)+']['+str(i)+']='+str(resultado[i]))
                        salidas[idx][i] = resultado[i]
                    
                    expect = outputs[idx]
                                        
                    # paso 5: balancea los pesos en funcion a la variacion del delta de error
                    self.addLog("PASO 4: balancea los pesos en funcion a la variacion del delta de error")
                    self.addLog(">> epochs:"+str(epochs)+' pesos:'+self.getPesos())
                    
                    self.error += self.backPropagation(resultado,expect)
                pass

                self.historial.append({self.error:self.getPesos()})
                self.addLog(">> errorCuadratico = "+str(self.error))
                    
                if abs(self.error) < self.umbralError:
                    break
            pass
        except:
            err = str(exc_info())
            self.addLog("ERROR Net.entrenar():\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
            print("ERROR Net.entrenar('"+str(err)+"'):\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
            self.addLog(err)
            self.panic = True
            pass        

    """   
    #  backPropagation
    # 
    # Algoritmo de retropropagacion
    # 
    # El procedimiento de retropropagacion es una forma relativamente eficiente
    # de calcular que tanto se mejora el desempeno con los cambios individuales
    # en los pesos. Se conoce como procedimiento de retropropagacion porque,
    # primero calcula cambios en la capa final, reutiliza gran parte de los
    # mismos calculos para calcular los cambios de los pesos de la penultima
    # capa y, finalmente, regresa a la capa inicial.
    #
    #
    """                 
    def backPropagation(self,result,expect):
        self.addLog("Net.backPropagation -> result:"+str(result)+" expect:"+str(expect))
        i,j = 0,0
                
        try:
            self.addLog(">> Calculo de deltas en la capa")
            for idx in xrange(self.nCapas -1, -1, -1):
                self.layers[idx].setDeltas(result,expect)
                
            self.addLog(">> Actualizacion de pesos en la capa")
            for idx in xrange(self.nCapas):
                self.layers[idx].setPesos(self.rate)
                
            self.addLog(">> Calculo de error cuadratico de la red")
            error = self.getErrorCuadratico(result,expect)
            self.addLog("<< "+str(error))
            return error
        except:
            err = str(exc_info())
            self.addLog("ERROR Net.backPropagation(): iteracion idx="+str(idx)+" de "+str(self.nCapas)+"\n")
            print("ERROR Net.backPropagation('"+str(err)+"'): iteracion idx="+str(idx)+" de "+str(self.nCapas)+"\n")
            self.addLog(err)
            self.panic = True 
        pass
        
       
    """
    # Obtiene el error cuadratico de la red
    """ 
    def getErrorCuadratico(self,resultado,expect):
        error = 0
        
        for j in xrange(len(expect)):
            error += 0.5 * (expect[j] - resultado[j])**2
            
        return error
        
    def getEpochs(self):
        return self.epochs
        
    def setEpochs(self,valor):
        self.epochs = valor
        
    def getPeso(self,i,w,capa):
        return self.layers[capa].nodos[w].getPeso[i]
        
    def setPeso(self,i,w,capa,valor):
        self.layers[capa].nodos[w].setPeso(i,valor)
        
    def getSalida(self,w,capa):
        return self.layers[capa].nodos[w].getSalida()
        
    def addLog(self,str):
        if self.debug :
            self.log.append(str)
        
    def getLog(self):
        return self.log
        
    def getPesos(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].pesos})
                
        return str(lst)

    def getDeltas(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].delta})
                
        return str(lst)
            
    def getErrores(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].error})
                
        return str(lst)
            
    def getEntradas(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].entradas})
                
        return dumps(lst, sort_keys=True,indent=4, separators=(',', ': '))
    
    def getHistorial(self):
        return dumps(self.historial, sort_keys=True,indent=4, separators=(',', ': '))
            
    def printLog(self):
        print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))
        
    """
    # Obtiene una estructura de la instancia de la red neuronal
    # y la exporta en formato JSON 
    """
    def getConfiguracion(self):
        red = {
            'nCapas'    : self.nCapas,
            'capas'     : self.capas,
            'layers'    : [
                self.layers[x].getConfiguracion() 
                for x in xrange(self.nCapas)
            ],       
            'neuronas'  : self.neuronas,
            'rate'      : self.rate,
            'entradas'  : self.entradas,
            'salidas'   : self.salidas,
            'funciones' : self.transferencias,
            'epochs'    : self.epochs,
            'expect'    : self.expect,
            'error'     : self.error
        }
        return red
    
    def setConfiguracion(self,js):
        data = json.loads(js)
        self.nCapas   = data['nCapas']
        self.capas    = data['capas']
        self.neuronas = data['neuronas']
        self.entradas = data['entradas']
        self.salidas  = data['salidas']
        self.rate     = data['rate']
        self.epochs   = data['epochs']
        self.error    = data['error']
        self.transferencias = data['funciones']
        self.expect   = data['expect']
        self.layers   = [None] * self.nCapas
        
        for i in xrange(self.nCapas):
            self.layers[i] = Layer(i,data['capas'][i],data['entradas'],data['funciones'][i],self.layers,self)
            self.layers[i].setConfiguracion(data['layers'][i])
        pass


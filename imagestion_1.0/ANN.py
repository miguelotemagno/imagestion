import math
import random
import string
import json
from sys import *

class ANN:
	
	def __init__(self, inputs, hidden, outputs, rate=0.5, threshold=0.001):
		self.datos_ent = [
			[[0,0], [0]],
			[[0,1], [1]],
			[[1,0], [1]],
			[[1,1], [0]],
		]
		
		self.debug = True
		self.threshold = threshold
		self.log = []
		self.nodos_ent = inputs
		self.nodos_ocu = hidden
		self.nodos_sal = outputs
		self.l = rate
		self.pesos_ent = []
		self.pesos_sal = []
		self.act_ent = []
		self.act_ocu = []
		self.act_sal = []
		pass

	####################################################################

	def exportJSON(self):
		json = {
			'inputs':  self.nodos_ent,
			'outputs': self.nodos_sal,
			'hidden':  self.nodos_ocu,
			'rate':    self.l,
			'wInputs': [
				self.pesos_ent[x] for x in range(self.nodos_ent)
			],
			'wHidden': [
				self.pesos_sal[x] for x in range(self.nodos_ocu)
			],
			'dataInput':  self.act_ent,
			'dataHidden': self.act_ocu,
			'dataOutput': self.act_sal
		}
		return json

	####################################################################
		
	def importJSON(self,js):
		data = json.loads(js)
		self.nodos_ent = data['inputs']
		self.nodos_sal = data['outputs']
		self.nodos_ocu = data['hidden']
		self.l         = data['rate']
		self.act_ent   = [None] * self.nodos_ent		
		self.act_ocu   = [None] * self.nodos_ocu
		self.act_sal   = [None] * self.nodos_sal
		self.pesos_ent = self.matriz(self.nodos_ent, self.nodos_ocu)
		self.pesos_sal = self.matriz(self.nodos_ocu, self.nodos_sal)

		for x in range(len(data['dataInput'])):
			self.act_ent[x] = data['dataInput'][x]

		for x in range(len(data['dataHidden'])):
			self.act_ocu[x] = data['dataHidden'][x]

		for x in range(len(data['dataOutput'])):
			self.act_sal[x] = data['dataOutput'][x]
			
		for y in range(len(data['wInputs'])):
			for x in range(len(data['wInputs'][y])):
				self.pesos_ent[y][x] = data['wInputs'][y][x]
			
		for y in range(len(data['wHidden'])):
			for x in range(len(data['wHidden'][y])):
				self.pesos_sal[y][x] = data['wHidden'][y][x]
		pass
		
	####################################################################
		
	def load(self, dbFile):
		f = open(dbFile, 'r')
		jsNet = f.read();
		f.close()
		self.importJSON(jsNet)
		pass
		
	####################################################################
		
	def save(self, dbFile):
		with open(dbFile, "w") as text_file:
			text_file.write(json.dumps(self.exportJSON(), sort_keys=True,indent=4, separators=(',', ': ')))
		pass
	
	####################################################################

	def setData(self,data):
		self.datos_ent = data
		pass
		
	####################################################################

	def matriz(self, x,y) :
		m = []
		for i in range(x):
			m.append([0.0]*y)
		return m

	####################################################################

	def sigmoide(self,x):
		return math.tanh(x)

	####################################################################

	def dsigmoide(self,x):
		return 1.0 - x**2

	####################################################################

	def iniciar_perceptron(self):
		## global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
		## global act_ent, act_ocu, act_sal, log
		random.seed(0)
		
		self.nodos_ent += 1
		self.act_ent = [1.0] * self.nodos_ent
		self.act_ocu = [1.0] * self.nodos_ocu
		self.act_sal = [1.0] * self.nodos_sal
		
		self.pesos_ent = self.matriz(self.nodos_ent, self.nodos_ocu)
		self.pesos_sal = self.matriz(self.nodos_ocu, self.nodos_sal)
		
		for i in range(self.nodos_ent):
			for j in range(self.nodos_ocu):
				self.pesos_ent[i][j] = random.uniform(-0.5, 0.5)
		
		for j in range(self.nodos_ocu):
			for k in range(self.nodos_sal):
				self.pesos_sal[j][k] = random.uniform(-0.5, 0.5)

	####################################################################

	def actualiza_nodos(self, entradas):  
		self.addLog('actualiza_nodos('+str(entradas)+')')  
		
		if len(entradas) != self.nodos_ent -1:
			raise ValueError('Numero de nodos de entrada incorrecto')
		
		for i in range(self.nodos_ent -1):
			self.act_ent[i] = float(entradas[i])
			
		for j in range(self.nodos_ocu):
			sum = 0.0
			for i in range(self.nodos_ent):
				sum = sum + self.pesos_ent[i][j] * self.act_ent[i]
			self.act_ocu[j] = self.sigmoide(sum)
		   
		for k in range(self.nodos_sal):
			sum = 0.0
			for j in range(self.nodos_ocu):
				sum = sum + self.pesos_sal[j][k] * self.act_ocu[j]
			self.act_sal[k] = self.sigmoide(sum)

		return self.act_sal[:]

	####################################################################

	def retropropagacion(self, objetivo):
		self.addLog('retropropagacion('+str(objetivo)+','+str(self.l)+')')  
		## global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
		## global act_ent, act_ocu, act_sal, log
		if len(objetivo) != self.nodos_sal:
			raise ValueError('numero de objetivos incorrecto')
		
		delta_salida = [0.0] * self.nodos_sal
		for k in range(self.nodos_sal):
			error = objetivo[k] - self.act_sal[k]
			delta_salida[k] = self.dsigmoide(self.act_sal[k]) * error
			
		delta_oculto = [0.0] * self.nodos_ocu
		for j in range(self.nodos_ocu):
			error = 0.0
			for k in range(self.nodos_sal):
				error = error + delta_salida[k] * self.pesos_sal[j][k]
			delta_oculto[j] = self.dsigmoide(self.act_ocu[j]) * error
			
		for j in range(self.nodos_ocu):
			for k in range(self.nodos_sal):
				cambio = delta_salida[k] * self.act_ocu[j]
				self.pesos_sal[j][k] = self.pesos_sal[j][k] + self.l * cambio
				
		for i in range(self.nodos_ent):
			for j in range(self.nodos_ocu):
				cambio = delta_oculto[j] * self.act_ent[i]
				self.pesos_ent[i][j] = self.pesos_ent[i][j] + self.l * cambio
				
		error = 0.0
		for k in range(len(objetivo)):
			error = error + 0.5*(objetivo[k] - self.act_sal[k])**2
			
		self.addLog({'error':str(error), 'delta_salida':str(delta_salida), 'delta_oculto':str(delta_oculto), 'pesos_sal':str(self.pesos_sal), 'pesos_ent':str(self.pesos_ent)})
		return error

	####################################################################

	def clasificar(self, patron):
		for p in patron:
			print '%s -> %s' % (p[0], self.actualiza_nodos(p[0]))
			
	####################################################################

	def entrenar_perceptron(self, patron, max_iter=1000):
		self.setData(patron)
		
		for i in range(max_iter):
			self.addLog(str(i)+'.----------------')
			error = 0.0
			for p in patron:
				entradas = p[0]
				objetivo = p[1]
				self.actualiza_nodos(entradas)
				error = error + self.retropropagacion(objetivo)
			
			if error < self.threshold:
				break
			
	####################################################################

	def addLog(self,str):
		if self.debug:
			self.log.append(str)        
    


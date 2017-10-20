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

import zlib
import numpy as np
import subprocess as sp
import os
import re
from ANN import *

class Classify:
	def __init__(self):
		self.net = ANN(2, 3, 1)
		self.filter = None
		self.fromFile = 'loadFromFile.sh'
		self.fromWeb = 'loadFromWeb.sh'
		self.path = os.getcwd()
		#self.command = "links -dump %s | tr -sc 'A-Za-z' '\n' | tr 'A-Z' 'a-z' | sort | uniq -c"
		self.text = ""
		self.trainData = None
		pass

	def getCRC(self, text):
		maxValue = 0xffffffff * 1.0
		crc = zlib.crc32(text) % (1<<32)
		return crc/maxValue

	def loadFilter(self, file):
		self.filter = ANN(1, 3, 1)
		self.filter.load(file)

	def trainFilter(self, file):
		self.loadFromFile(file)
		self.filter = ANN(1, 3, 1)

		list = self.text.split("\n")
		reg = re.compile('(\d+)\s+(\w+)')
		words = []
		trainData = []

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				crc = self.getCRC(word)
				#print "[%s] [%s] [%f]" % (n, word, crc)
				words.append(crc)

		for i in xrange(len(words)):
			word = words[i]
			trainData.append([[word], [1]])

		self.filter.iniciar_perceptron();
		self.filter.entrenar_perceptron(trainData)
		output = "%s/%s.json" % (self.path, file)
		self.filter.save(output)

	def saveNet(self,file):
		self.net.save(file)

	def loadFromFile(self,source):
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromFile), source])

	def loadFromWeb(self,source):
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromWeb), source])

	def process(self):
		list = self.text.split("\n")
		reg = re.compile('(\d+)\s+(\w+)')
		counts = []
		words = []
		trainData = []
		maxVal = 1

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				val = int(n)
				crc = self.getCRC(word)
				eval = self.filter.actualiza_nodos([crc]) if self.filter else [0.0]

				if eval[0] > 0.5:
					continue

				print "[%d] [%s] [%f] [%f]" % (int(n), word, crc, eval[0])
				counts.append(val)
				words.append(crc)
				maxVal = val if val > maxVal else maxVal

		for i in xrange(len(words)):
			val = 1.0 * counts[i]/maxVal
			word = words[i]
			trainData.append([[val,word], [1]])

		#print trainData

		self.net.iniciar_perceptron();
		self.net.entrenar_perceptron(trainData)
		#self.net.clasificar(trainData)


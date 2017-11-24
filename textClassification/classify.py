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
import subprocess as sp
import os
import re
from ANN import *
from random import randint
from math import log
import tensorflow as tf

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
		self.sess = None
		pass

	def getCRC(self, text):
		#maxValue = 0xffffffff * 1.0
		crc = zlib.crc32(text) % (1<<32)
		return log(crc) #crc/maxValue

	def loadFilter(self, file):
		# self.filter = ANN(3, 3, 1)
		# self.filter.load(file)
		path = '%s/%s' % (self.path,file)
		with tf.Session() as self.filter:
			saver = tf.train.import_meta_graph(path+'.meta')
			saver.restore(self.filter, path)

	def trainFilter(self, file):
		self.loadFromFile(file)
		self.filter = ANN(3, 3, 1)

		list = self.text.split("\n")
		reg = re.compile('(\d+)\s+(\w+)')
		words = []
		trainData = []
		expect = []

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				crc = self.getCRC(word) / len(word)
				print "[%s] [%s] [%f] [%d]" % (n, word, crc, len(word))
				words.append([crc, len(word)])

		for i in xrange(len(words)):
			(crc, lenw) = words[i]
			#trainData.append([[1, crc, lenw], [0]])
			trainData.append([1, crc, lenw])
			expect.append([0])

			if i%5 == 0:
				wrd = self.wordGenerate()
				gen = self.getCRC(wrd) / len(wrd)
				#trainData.append([[0, gen, len(wrd)], [1]])
				trainData.append([0, gen, len(wrd)])
				expect.append([1])

		# self.filter.iniciar_perceptron()
		# self.filter.entrenar_perceptron(trainData)
		# self.filter.clasificar(trainData)
		# output = "%s/%s.json" % (self.path, file)
		# self.filter.save(output)

		self.filter = self.prepareTensor(trainData, expect)

		saver = tf.train.Saver()
		saver.save(self.filter, self.path+'/'+file+'.tfdb',
		           global_step=None,
		           latest_filename=None,
		           meta_graph_suffix='meta',
		           write_meta_graph=True)

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

		self.defineFilterVariables()
		self.y = self.defineTensorFilter()

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				val = int(n)
				crc = self.getCRC(word) / len(word)
				#eval = self.filter.actualiza_nodos([val, crc, len(word)]) if self.filter else [0.0]
				eval = self.filter.run(self.y, feed_dict={self.x: [val, crc, len(word)]}) if self.filter else [0.0, 0.0]

				if abs(eval[0]) > 0.5:
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

	def wordGenerate(self):
		n = randint(2,5)
		vocals = ['a','e','i','o','u']
		word = chr(randint(97, 122))
		for i in xrange(0,n):
			ascii = randint(97,122)
			word = word + vocals[randint(0,4)] + chr(ascii)
			#word = word + chr(ascii)

		return word
		
	def defineFilterVariables(self):
		self.HIDDEN_NODES = 3
		self.x = tf.placeholder("float", [None, 3], name="x")
		self.y_ = tf.placeholder("float", [None, 1], name="y_")
		self.W = tf.Variable(tf.random_uniform([3, self.HIDDEN_NODES], -.01, .01), name="W")
		self.b = tf.Variable(tf.random_uniform([self.HIDDEN_NODES], -.01, .01), name="b")
		self.W2 = tf.Variable(tf.random_uniform([self.HIDDEN_NODES, 2], -.1, .1), name="W2")
		self.b2 = tf.Variable(tf.zeros([2]), name="b2")
		pass

	def defineTensorFilter(self):
		return tf.nn.softmax(tf.matmul(tf.nn.relu(tf.matmul(self.x,self.W) + self.b), self.W2))

	def prepareTensor(self, xTrain, yTrain):

		sess = tf.InteractiveSession()		
		self.defineFilterVariables()
		self.y = self.defineTensorFilter()
		#y = tf.nn.tanh(hidden2)

		cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y))
		train_step = tf.train.GradientDescentOptimizer(0.2).minimize(cross_entropy)

		tf.global_variables_initializer().run()
		#tf.initialize_all_variables().run()
		for step in range(1000):
			feed_dict = {self.x: xTrain, self.y_: yTrain}  # feed the net with our inputs and desired outputs.
			e, a = sess.run([cross_entropy, train_step], feed_dict)
			if e < 1: break  # early stopping yay

		#print "%s => %s" % (xTrain, yTrain)
		correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))  # argmax along dim-1
		accuracy = tf.reduce_mean(
			tf.cast(correct_prediction, "float"))  # [True, False, True, True] -> [1,0,1,1] -> 0.75.

		print "accuracy %s" % (accuracy.eval({self.x: xTrain, self.y_: yTrain}))

		#learned_output = tf.argmax(y, 1)
		#print learned_output.eval({self.x: xTrain})
		print sess.run(self.y, feed_dict={self.x: xTrain})

		return sess
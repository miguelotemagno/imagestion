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

	##########################################################################		           
	
	def getCRC(self, text):
		#maxValue = 0xffffffff * 1.0
		crc = zlib.crc32(text) % (1<<32)
		return log(crc) #crc/maxValue

	##########################################################################		           
	
	def saveFilter(self,file):
		saver = tf.train.Saver()
		saver.save(self.sess, self.path+'/'+file+'.tfdb',
	           global_step=None,
	           latest_filename=None,
	           meta_graph_suffix='meta',
	           write_meta_graph=True)
		           
	##########################################################################		           
	
	def loadFilter(self, file):
		print "=> loadFilter (%s)\n" % (file)
		# self.filter = ANN(3, 3, 1)
		# self.filter.load(file)
		path = '%s/%s' % (self.path,file)
		#self.defineFilterModel()
		#init = tf.global_variables_initializer()
		#self.filter.run(init)				
		
		tf.reset_default_graph()
		
		HIDDEN_NODES = 3
		self.x = tf.placeholder("float", [None, 3], name="x")
		self.y_ = tf.placeholder("float", [None, 1], name="y_")		
		
		W = tf.get_variable("W", shape=[3, HIDDEN_NODES]) #, initializer = tf.zeros_initializer)
		b = tf.get_variable("b", shape=[HIDDEN_NODES]) #, initializer = tf.zeros_initializer)
		W2 = tf.get_variable("W2", shape=[HIDDEN_NODES,2]) #, initializer = tf.zeros_initializer)
		b2 = tf.get_variable("b2", shape=[2]) #, initializer = tf.zeros_initializer)
		
		self.y = tf.nn.softmax( tf.matmul( tf.nn.relu( tf.matmul(self.x,W) + b), W2))		
		
		
		self.filter = tf.Session()
		#self.defineFilterModel()
		#init = tf.global_variables_initializer()
		#self.filter.run(init)
		saver = tf.train.Saver()
		
		#W.initializer.run(session=self.filter)
		#b.initializer.run(session=self.filter)
		#W2.initializer.run(session=self.filter)
		#b2.initializer.run(session=self.filter)
		
		saver.restore(self.filter, path)
						
	##########################################################################		           
		
	def defineFilterModel(self):
		print "=> defineFilterModel\n"
		HIDDEN_NODES = 3
		self.x = tf.placeholder("float", [None, 3], name="x")
		self.y_ = tf.placeholder("float", [None, 1], name="y_")
		W = tf.Variable(tf.random_uniform([3, HIDDEN_NODES], -.01, .01), name="W")
		b = tf.Variable(tf.random_uniform([HIDDEN_NODES], -.01, .01), name="b")
		W2 = tf.Variable(tf.random_uniform([HIDDEN_NODES, 2], -.1, .1), name="W2")
		b2 = tf.Variable(tf.zeros([2]), name="b2")
		self.y = tf.nn.softmax( tf.matmul( tf.nn.relu( tf.matmul(self.x,W) + b), W2))

		self.cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y))
		return tf.train.GradientDescentOptimizer(0.2).minimize(self.cross_entropy)		

	##########################################################################		           
	
	def trainFilter(self, file):
		print "=> trainFilter (%s)\n" % (file)
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
				#print "[%s] [%s] [%f] [%d]" % (word, n, crc, len(word))
				words.append([crc, len(word)])

		for i in xrange(len(words)):
			(crc, lenw) = words[i]
			data = [1.0, crc, 1.0*lenw]
			#trainData.append([data, [0]])
			trainData.append(data)
			expect.append([0.0])

			if i%5 == 0:
				wrd = self.wordGenerate()
				gen = self.getCRC(wrd) / len(wrd)
				data = [0.0, gen, 1.0*len(wrd)]
				#trainData.append([data, [1]])
				trainData.append(data)
				expect.append([1.0])

		with tf.Session() as self.sess:
			self.prepareTensor(trainData, expect)
			self.saveFilter(file)

	##########################################################################		           
	
	def saveNet(self,file):
		self.net.save(file)

	##########################################################################		           

	def loadFromFile(self,source):
		print "=> loadFromFile (%s)\n" % (source)
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromFile), source])

	##########################################################################		           

	def loadFromWeb(self,source):
		print "=> loadFromWeb (%s)\n" % (source)
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromWeb), source])

	##########################################################################		           

	def process(self):
		print "=> process\n"
		list = self.text.split("\n")
		reg = re.compile('(\d+)\s+(\w+)')
		counts = []
		words = []
		trainData = []
		maxVal = 1.0

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				val = int(n)
				maxVal = 1.0 * val if val > maxVal else maxVal

		print "maxval:%f\n" % (maxVal)
		
		with tf.Session() as filter:			
			for line in list:
				expr = reg.search(line)
				if expr:
					(n, word) = expr.group(1,2)
					val = (1.0 * int(n)) / maxVal
					crc = 1.0 * (self.getCRC(word) / len(word))
					data = [val, crc, 1.0*len(word)]
	
					#eval = self.filter.actualiza_nodos(data) if self.filter else [0.0]
					#eval = self.filter.run(self.y_, feed_dict={self.x: [data]}) if self.filter else [0.0, 0.0]
					#feed_dict = {self.x: xTrain, self.y_: yTrain}  # feed the net with our inputs and desired outputs.
					#e, a = self.filter.run([self.cross_entropy, train_step], feed_dict)
	
					#data = [1.0, crc, 1.0*lenw]
					eval = self.filter.run(self.y, feed_dict={self.x: [data]})
					
					if abs(eval[0][0]) < 0.5:
						print "--------------------------> [%s] [%f] [%f] => [%f]" % (word, val, crc, eval[0][0])
						continue
					else:
						print "%s: [%f] [%f] [%f] => [%f]" % (word,data[0],data[1],data[2], eval[0][0])
								
					counts.append(1.0 * val)
					words.append(crc)

		for i in xrange(len(words)):
			val = counts[i]
			word = words[i]
			trainData.append([[val,word], [1.0]])

		#print trainData

		self.net.iniciar_perceptron();
		self.net.entrenar_perceptron(trainData)
		#self.net.clasificar(trainData)

	##########################################################################		           

	def wordGenerate(self):
		n = randint(2,5)
		vocals = ['a','e','i','o','u']
		word = chr(randint(97, 122))
		for i in xrange(0,n):
			ascii = randint(97,122)
			word = word + vocals[randint(0,4)] + chr(ascii)
			#word = word + chr(ascii)

		return word

	##########################################################################		           

	def prepareTensor(self, xTrain, yTrain):
		print "=> prepareTensor\n"
		train_step = self.defineFilterModel();
		init = tf.global_variables_initializer()

		self.sess.run(init)
		for step in range(1000):
			feed_dict = {self.x: xTrain, self.y_: yTrain}  # feed the net with our inputs and desired outputs.
			e, a = self.sess.run([self.cross_entropy, train_step], feed_dict)
			if e < 1: break  # early stopping yay

		#print "%s => %s" % (xTrain, yTrain)
		print self.sess.run(self.y, feed_dict={self.x: xTrain})
		#print sess.run(self.y, feed_dict={self.x: [[2.0, 10.711832, 2.0]]})

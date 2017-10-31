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
		pass

	def getCRC(self, text):
		#maxValue = 0xffffffff * 1.0
		crc = zlib.crc32(text) % (1<<32)
		return log(crc) #crc/maxValue

	def loadFilter(self, file):
		self.filter = ANN(3, 3, 1)
		self.filter.load(file)

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

			if i%15 == 0:
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

		sess = self.prepareTensor(trainData, expect)

		saver = tf.train.Saver()
		saver.save(sess, self.path+'/'+file+'.tfdb',
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

		for line in list:
			expr = reg.search(line)
			if expr:
				(n, word) = expr.group(1,2)
				val = int(n)
				crc = self.getCRC(word) / len(word)
				eval = self.filter.actualiza_nodos([val, crc, len(word)]) if self.filter else [0.0]

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

	def prepareTensor(self, xTrain, yTrain):
		HIDDEN_NODES = 3

		x = tf.placeholder(tf.float32, [None, 3])
		W_hidden = tf.Variable(tf.truncated_normal([3, HIDDEN_NODES], stddev=1. / math.sqrt(3)))
		b_hidden = tf.Variable(tf.zeros([HIDDEN_NODES]))
		hidden = tf.nn.relu(tf.matmul(x, W_hidden) + b_hidden)

		W_logits = tf.Variable(tf.truncated_normal([HIDDEN_NODES, 2], stddev=1. / math.sqrt(HIDDEN_NODES)))
		b_logits = tf.Variable(tf.zeros([2]))
		logits = tf.matmul(hidden, W_logits) + b_logits

		y = tf.nn.softmax(logits)
		#y = tf.nn.tanh(logits)

		y_input = tf.placeholder(tf.float32, [None, 1])

		cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, y_input)
		loss = tf.reduce_mean(cross_entropy)

		train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
		init_op = tf.initialize_all_variables()

		sess = tf.Session()
		sess.run(init_op)

		print xTrain
		print yTrain

		for i in xrange(1000):
			_, loss_val = sess.run([train_op, loss], feed_dict={x: xTrain, y_input: yTrain})

			if i % 10 == 0:
				print "Step:", i, "Current loss:", loss_val
				for x_input in [xTrain]:
					result = sess.run(y, feed_dict={x: [x_input]})
					print "%s => %s" % (x_input, result)

		return sess
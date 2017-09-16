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

import numpy as np

class Image2Vector(object):
	def __init__(self, points):
		self.exist = np.zeros(shape=points.shape, dtype=np.bool)
		self.lCord = []
		self.points = points
		pass

	def linearRegression(self,Y, X):
		mY = np.mean(Y)
		mX = np.mean(X)
		mXY = np.mean(Y * X)
		sqrX = [i ** 2 for i in X]
		m = (mX * mY - mXY) / (mX ** 2 - np.mean(sqrX))
		b = mY - m * mX
		return [m, b]

	def linearEcuation(self,m, x, b):
		return m * x + b

	def calcSlope(y, x, y0, x0):
		d = 0 if x != x0  else 0.0000000001
		m = (y - y0) / (x - x0 + d)
		return m

	def calcAngle(self,slope):
		angle = np.arctan(slope)
		return 180 - (180 * angle) / np.pi

	def getPointsPath(self, y, x):
		#  y, x: coords in points[y,x]
		#  points: reduced picture
		#  exist: matrix with true/false each point existence
		#  LP: List coordinates for each point
		data = self.points[y, x]
		mask = 0L

		mask |= 0b100000000 if self.points[y][x] & 8 != 0 else mask
		mask |= 0b010000000 if self.points[y][x] & 4 != 0 else mask
		mask |= 0b000100000 if self.points[y][x] & 2 != 0 else mask
		mask |= 0b000010000 if self.points[y][x] & 1 != 0 else mask
		mask |= 0b001000000 if self.points[y][x + 1] & 4 != 0 else mask
		mask |= 0b000001000 if self.points[y][x + 1] & 1 != 0 else mask
		mask |= 0b000000100 if self.points[y + 1][x] & 2 != 0 else mask
		mask |= 0b000000010 if self.points[y + 1][x] & 1 != 0 else mask
		mask |= 0b000000001 if self.points[y + 1][x + 1] & 1 != 0 else mask

		(N, NE, E, SE, S, SW, W, NW) = (
			0b010010000,  ## [[0,1,0], [0,1,0], [0,0,0]]
			0b001010000,  ## [[0,0,1], [0,1,0], [0,0,0]]
			0b000011000,  ## [[0,0,0], [0,1,1], [0,0,0]]
			0b000010001,  ## [[0,0,0], [0,1,0], [0,0,1]]
			0b000010010,  ## [[0,0,0], [0,1,0], [0,1,0]]
			0b000010100,  ## [[0,0,0], [0,1,0], [1,0,0]]
			0b000110000,  ## [[0,0,0], [1,1,0], [0,0,0]]
			0b100010000   ## [[1,0,0], [0,1,0], [0,0,0]]
		)

		vectorize = {
			0b000000000: nothing,  ## [[0,0,0], [0,0,0], [0,0,0]]
			0b000010000: alone,    ## [[0,0,0], [0,1,0], [0,0,0]]
			0b010010000: goN,      ## [[0,1,0], [0,1,0], [0,0,0]]
			0b001010000: goNE,     ## [[0,0,1], [0,1,0], [0,0,0]]
			0b000011000: goE,      ## [[0,0,0], [0,1,1], [0,0,0]]
			0b000010001: goSE,     ## [[0,0,0], [0,1,0], [0,0,1]]
			0b000010010: goS,      ## [[0,0,0], [0,1,0], [0,1,0]]
			0b000010100: goSW,     ## [[0,0,0], [0,1,0], [1,0,0]]
			0b000110000: goW,      ## [[0,0,0], [1,1,0], [0,0,0]]
			0b100010000: goNW,     ## [[1,0,0], [0,1,0], [0,0,0]]

			0b010010010: goN2S,    ## [[0,1,0], [0,1,0], [0,1,0]]
			0b000111000: goW2E,    ## [[0,0,0], [1,1,1], [0,0,0]]
			0b100010001: goSW2NE,  ## [[1,0,0], [0,1,0], [0,0,1]]
			0b001010100: goNW2SE,  ## [[0,0,1], [0,1,0], [1,0,0]]

			0b001010010: goS2NE,   ## [[0,0,1], [0,1,0], [0,1,0]]
			0b100010010: goS2NW,   ## [[1,0,0], [0,1,0], [0,1,0]]
			0b010010001: goN2SE,   ## [[0,1,0], [0,1,0], [0,0,1]]
			0b010010100: goSW2N,   ## [[0,1,0], [0,1,0], [1,0,0]]
			0b000110001: goSE2W,   ## [[0,0,0], [1,1,0], [0,0,1]]
			0b001110000: goNE2W,   ## [[0,0,1], [1,1,0], [0,0,0]]
			0b000011010: goNW2E,   ## [[1,0,0], [0,1,1], [0,0,0]]
			0b000011100: goSW2E,   ## [[0,0,0], [0,1,1], [1,0,0]]

			# 0b110110000: goN2W2NW  ## [[1,1,0], [1,1,0], [0,0,0]]
		}

		coords = []
		self.exist[y, x] = True

		if mask in vectorize:
			coords = vectorize[mask](y, x, self)
			print "%s -> %s\n%s" % (bin(data), bin(mask), str(coords))
			self.lCord.append(coords)

		else:
			# TODO ver como generar nuevas listas al encontrar angulos
			print "%s --> Not found!\n" % (bin(mask))
			lN = lNE = lE = lSE = lS = lSW = lW = lNW = []

			if mask & N:
				lN = vectorize[N](y, x, self)
				# print 'N '+str(lN)
			if mask & NE:
				lNE = vectorize[NE](y, x, self)
				# print 'NE '+str(lNE)
			if mask & E:
				lE = vectorize[E](y, x, self)
				# print 'E '+str(lE)
			if mask & SE:
				lSE = vectorize[SE](y, x, self)
				# print 'SE '+str(lSE)
			if mask & S:
				lS = vectorize[S](y, x, self)
				# print 'S '+str(lS)
			if mask & SW:
				lSW = vectorize[SW](y, x, self)
				# print 'SW '+str(lSW)
			if mask & W:
				lW = vectorize[W](y, x, self)
				# print 'W '+str(lW)
			if mask & NW:
				lNW = vectorize[NW](y, x, self)
				# print 'NW '+str(lNW)

			coords = coords if not(lN)  else coords + lN
			coords = coords if not(lNE)  else coords + lNE
			coords = coords if not(lE)  else coords + lE
			coords = coords if not(lSE) else coords + lSE
			coords = coords if not(lS)  else coords + lS
			coords = coords if not(lSW)  else coords + lSW
			coords = coords if not(lW)  else coords + lW
			coords = coords if not(lNW)  else coords + lNW
			print coords
			self.lCord.append(coords)

		return coords


def alone(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,0,0]]
	return []

def nothing(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,0,0]]
	return [[y,x]]

def goN(y, x, inst):
	# [[0,1,0],
	# [0,1,0],
	# [0,0,0]]
	if inst.exist[y - 1][x] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y - 1, x))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goNE(y, x, inst):
	# [[0,0,1],
	#  [0,1,0],
	#  [0,0,0]]
	if inst.exist[y - 1][x + 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y - 1, x + 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goE(y, x, inst):
	# [[0,0,0],
	#  [0,1,1],
	#  [0,0,0]]
	if inst.exist[y][x + 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y, x + 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goSE(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,0,1]]
	if inst.exist[y + 1][x + 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y + 1, x + 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goS(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,1,0]]
	if inst.exist[y + 1][x] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y + 1, x))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goSW(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [1,0,0]]
	if inst.exist[y + 1][x - 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y + 1, x - 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goW(y, x, inst):
	# [[0,0,0],
	#  [1,1,0],
	#  [0,0,0]]
	if inst.exist[y][x - 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y, x - 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goNW(y, x, inst):
	# [[1,0,0],
	#  [0,1,0],
	#  [0,0,0]]
	if inst.exist[y - 1][x - 1] == True:
		return []
	else:
		lCoords = [[y,x]]
		coords = inst.lCord.append(inst.getPointsPath(y - 1, x - 1))
		lCoords = lCoords if not coords else lCoords + coords
		return lCoords

def goN2S(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [0,1,0]]
	lCoords = []
	l1 = goN(y, x, inst)
	l2 = goS(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goW2E(y, x, inst):
	# [[0,0,0],
	#  [1,1,1],
	#  [0,0,0]]
	lCoords = []
	l1 = goW(y, x, inst)
	l2 = goE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goSW2NE(y, x, inst):
	# [[1,0,0],
	#  [0,1,0],
	#  [0,0,1]]
	lCoords = []
	l1 = goSW(y, x, inst)
	l2 = goNE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goNW2SE(y, x, inst):
	# [[0,0,1],
	#  [0,1,0],
	#  [1,0,0]]
	lCoords = []
	l1 = goNW(y, x, inst)
	l2 = goSE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goS2NE(y, x, inst):
	# [[0,0,1],
	#  [0,1,0],
	#  [0,1,0]]
	lCoords = []
	l1 = goN(y, x, inst)
	l2 = goNE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goS2NW(y, x, inst):
	# [[1,0,0],
	#  [0,1,0],
	#  [0,1,0]]
	lCoords = []
	l1 = goNW(y, x, inst)
	l2 = goS(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goN2SE(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [0,0,1]]
	lCoords = []
	l1 = goN(y, x, inst)
	l2 = goSE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goSW2N(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [1,0,0]]
	lCoords = []
	l1 = goN(y, x, inst)
	l2 = goSW(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goSE2W(y, x, inst):
	# [[0,0,0],
	#  [1,1,0],
	#  [0,0,1]]
	lCoords = []
	l1 = goW(y, x, inst)
	l2 = goSE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goNE2W(y, x, inst):
	# [[0,0,1],
	#  [1,1,0],
	#  [0,0,0]]
	lCoords = []
	l1 = goW(y, x, inst)
	l2 = goNE(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goNW2E(y, x, inst):
	# [[1,0,0],
	#  [0,1,1],
	#  [0,0,0]]
	lCoords = []
	l1 = goE(y, x, inst)
	l2 = goNW(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

def goSW2E(y, x, inst):
	# [[0,0,0],
	#  [0,1,1],
	#  [1,0,0]]
	lCoords = []
	l1 = goE(y, x, inst)
	l2 = goSW(y, x, inst)
	lCoords = lCoords if not l1 else lCoords + l1
	lCoords = lCoords if not l2 else lCoords + l2
	return lCoords

# def goN2W2NW(y, x, inst):
# 	# [[1,1,0],
# 	#  [1,1,0],
# 	#  [0,0,0]]
# 	goN(y, x, inst)
# 	goW(y, x, inst)
# 	goNW(y, x, inst)
# 	pass

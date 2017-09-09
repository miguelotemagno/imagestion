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

		vectorize = {
			0b000010000: alone,  ## [[0,0,0], [0,1,0], [0,0,0]]
			0b010010000: goN,  ## [[0,1,0], [0,1,0], [0,0,0]]
			0b001010000: goNE,  ## [[0,0,1], [0,1,0], [0,0,0]]
			0b000011000: goE,  ## [[0,0,0], [0,1,1], [0,0,0]]
			0b000010001: goSE,  ## [[0,0,0], [0,1,0], [0,0,1]]
			0b000010010: goS,  ## [[0,0,0], [0,1,0], [0,1,0]]
			0b000010100: goSW,  ## [[0,0,0], [0,1,0], [1,0,0]]
			0b000110000: goW,  ## [[0,0,0], [1,1,0], [0,0,0]]
			0b100010000: goNW,  ## [[1,0,0], [0,1,0], [0,0,0]]
			0b010010010: goN2S,  ## [[0,1,0], [0,1,0], [0,1,0]]
			0b000111000: goW2E,  ## [[0,0,0], [1,1,1], [0,0,0]]
			0b100010001: goSW2NE,  ## [[1,0,0], [0,1,0], [0,0,1]]
			0b001010100: goNW2SE  ## [[0,0,1], [0,1,0], [1,0,0]]
		}

		turn = {
			0b011010000: goN2NE,  ## [[0,1,1], [0,1,0], [0,0,0]]
			0b010011000: goN2E,  ## [[0,1,0], [0,1,1], [0,0,0]]
			0b010010001: goN2SE,  ## [[0,1,0], [0,1,0], [0,0,1]]
			0b010010100: goN2SW,  ## [[0,1,0], [0,1,0], [1,0,0]]
			0b010110000: goN2W,  ## [[0,1,0], [1,1,0], [0,0,0]]
			0b110010100: goN2NW,  ## [[0,1,0], [1,1,0], [0,0,0]]
		}

		self.lCord.append([y, x])
		self.exist[y, x] = True

		if data in vectorize:
			vectorize[data](y, x, self)
		else:
			# TODO ver como generar nuevas listas al encontrar angulos
			# turn[data](y, x, self)
			pass

		return self.lCord


def alone(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,0,0]]
	pass

def goN(y, x, inst):
	# [[0,1,0],
	# [0,1,0],
	# [0,0,0]]
	if inst.exist[y - 1][x] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y - 1, x))

def goNE(y, x, inst):
	# [[0,0,1],
	#  [0,1,0],
	#  [0,0,0]]
	if inst.exist[y - 1][x + 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y - 1, x + 1))

def goE(y, x, inst):
	# [[0,0,0],
	#  [0,1,1],
	#  [0,0,0]]
	if inst.exist[y][x + 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y, x + 1))

def goSE(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,0,1]]
	if inst.exist[y + 1][x + 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y + 1, x + 1))

def goS(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [0,1,0]]
	if inst.exist[y + 1][x] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y + 1, x))

def goSW(y, x, inst):
	# [[0,0,0],
	#  [0,1,0],
	#  [1,0,0]]
	if inst.exist[y + 1][x - 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y + 1, x - 1))

def goW(y, x, inst):
	# [[0,0,0],
	#  [1,1,0],
	#  [0,0,0]]
	if inst.exist[y][x - 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y, x - 1))

def goNW(y, x, inst):
	# [[1,0,0],
	#  [0,1,0],
	#  [0,0,0]]
	if inst.exist[y - 1][x - 1] == True:
		pass
	else:
		inst.lCord.append(inst.getPointsPath(y - 1, x - 1))

def goN2S(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [0,1,0]]
	goN(y, x, inst)
	goS(y, x, inst)

def goW2E(y, x, inst):
	# [[0,0,0],
	#  [1,1,1],
	#  [0,0,0]]
	goW(y, x, inst)
	goE(y, x, inst)

def goSW2NE(y, x, inst):
	# [[1,0,0],
	#  [0,1,0],
	#  [0,0,1]]
	goSW(y, x, inst)
	goNE(y, x, inst)

def goNW2SE(y, x, inst):
	# [[0,0,1],
	#  [0,1,0],
	#  [1,0,0]]
	goNW(y, x, inst)
	goSE(y, x, inst)

def goN2NE(y, x, inst):
	# [[0,1,1],
	#  [0,1,0],
	#  [0,0,0]]
	pass

def goN2E(y, x, inst):
	# [[0,1,0],
	#  [0,1,1],
	#  [0,0,0]]
	pass

def goN2SE(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [0,0,1]]
	pass

def goN2SW(y, x, inst):
	# [[0,1,0],
	#  [0,1,0],
	#  [1,0,0]]
	pass

def goN2W(y, x, inst):
	# [[0,1,0],
	#  [1,1,0],
	#  [0,0,0]]
	pass

def goN2NW(y, x, inst):
	# [[1,1,0],
	#  [0,1,0],
	#  [0,0,0]]
	pass



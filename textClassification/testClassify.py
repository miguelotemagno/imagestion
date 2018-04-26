from classify import *
import numpy as np
#import matplotlib                 ##
#matplotlib.use('Agg')             ##
#import matplotlib.mlab as mlab    ## sudo apt-get install python-matplotlib
#import matplotlib.pyplot as plt   ##
import sys

def plotHistogram(arr, b, file): # b = bins => max value of arr[i]
    hist, bins = np.histogram(arr, bins=b)
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center')
    #plt.show()
    plt.savefig(file)

c = Classify()
x = []
y = []

if sys.argv[1] == 'train' or sys.argv[1] == 'all':
	print "train\n"
	c.trainFilter2x2('preposiciones.txt', {
		#'adverbios.txt'        : [1.0, 0.0],
		#'articulos.txt'     : [1.0, 0.0],
		#'preposiciones.txt' : [1, 0],
		'sustantivos.txt'   : [1, 0],
		'pronombres.txt'    : [0, 1]
		})
	
	for i in c.data:
		x.append(i[0])
		y.append(i[1])
	
	#plotHistogram(x, 200, 'x.png')
	#plotHistogram(y, 200, 'y.png')

if sys.argv[1] == 'test' or sys.argv[1] == 'all':
	#c.loadFilter('filtro.txt.tfdb')
	c.loadFilter('preposiciones.txt.tfdb')
	
	print "filter\n"
	c.loadFromWeb('http://conjugador.reverso.net/conjugacion-espanol.html?verb=abrir')    ## sudo apt-get install links
	#c.loadFromFile('libro.txt')
	c.process()

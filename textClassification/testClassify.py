from classify import *
import sys

c = Classify()

if sys.argv[1] == 'train' or sys.argv[1] == 'all':
	print "train\n"
	c.trainFilter('filtro.txt')

if sys.argv[1] == 'test' or sys.argv[1] == 'all':
	c.loadFilter('filtro.txt.tfdb')
	
	print "filter\n"
	#c.loadFromWeb('www.emol.cl')
	c.loadFromFile('libro.txt')
	c.process()

from classify import *

c = Classify()

print "train\n"
#c.trainFilter('filtro.txt')
c.loadFilter('filtro.txt.json')

print "filter\n"
c.loadFromWeb('www.emol.cl')
#c.loadFromFile('libro.txt')
c.process()
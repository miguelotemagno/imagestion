from classify import *

c = Classify()

c.loadFilter('filtro.txt.json')
c.loadFromWeb('www.emol.cl')
c.process()
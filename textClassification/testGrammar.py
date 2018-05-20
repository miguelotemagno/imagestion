import sys
import re
from grammarRules import *

g = GrammarRules()

if sys.argv[1] == 'web':
	url = 'https://raw.githubusercontent.com/miguelotemagno/imagestion/imagestion_1.0/textClassification/grammarTest.txt'
	if sys.argv[2] != '':
		url = sys.argv[2]

	g.loadFromWeb(url)
	print g.text

	tokens = g.word_tokenize(g.text)
	#print tokens
	list = g.pos_tag(tokens)
	print list

if sys.argv[1] == 'file':
	file = "libro.txt"
	if sys.argv[2] != '':
		file = sys.argv[2]

	g.loadFromFile(file)
	tokens = g.word_tokenize(g.text)
	list = g.pos_tag(tokens)
	print list


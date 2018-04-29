import re
import json
import sys


class GrammarRules:
	def jsonLoad(self, dbFile):
		f = open(dbFile, 'r')
		jsRules = f.read();
		f.close()
		return json.loads(jsRules)
		
	####################################################################
	
	def __init__(self):
		self.rules = self.jsonLoad("spanishRules.json")

	####################################################################
	
	def isVerb(self):
		#return re.compile('^(\w+[ae]r|\w*ir|\w+(mos|is|[sn]|ron|[ni]do))$')
		return re.compile(self.rules['verb'])

	####################################################################
	
	def isArticle(self):
		return re.compile(self.rules['article'])

	####################################################################
	
	def isAdjetive(self):
		return re.compile(self.rules['adjetive'])

	####################################################################
	
	def isSustantive(self):
		return re.compile(self.rules['sustantive'])

	####################################################################
	
	def isPreposition(self):
		return re.compile(self.rules['preposition'])

	####################################################################
	
	def isAdverb(self):
		return re.compile(self.rules['adverb'])

	####################################################################
	
	def isPronom(self):
		return re.compile(self.rules['pronom'])

	####################################################################
	
	def getVerb(self, text):
		char = text[0]
		if char in self.rules:
			for verb, hash in self.rules[char].iteritems():
				expr = '^('+'|'.join(hash.values())+')$'
				eval = re.compile(expr)
				if eval.match(text):
					return verb

		return None
        
	####################################################################
		

	
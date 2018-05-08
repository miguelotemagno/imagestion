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
		items = self.rules['verb']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isDeterminer(self,text):
		for type, list in self.rules['determiner'].iteritems():
			expr = '^('+'|'.join(list)+')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None


	####################################################################
	
	def isAdjetive(self):
		items = self.rules['adjetive']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isSustantive(self):
		items = self.rules['sustantive']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isPreposition(self):
		items = self.rules['preposition']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isAdverb(self):
		items = self.rules['adverb']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isPronom(self):
		items = self.rules['pronom']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################

	def isInterjection(self):
		items = self.rules['interjection']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################

	def isConjunction(self, text):
		for type, list in self.rules['conjunction'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

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
		

	
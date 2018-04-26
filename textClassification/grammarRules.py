import re
import json
from sys import *

class GrammarRules:
	def jsonLoad(self, dbFile):
		f = open(dbFile, 'r')
		jsRules = f.read();
		f.close()
		return json.loads(jsRules)
		
	####################################################################
	
	def __init__(self):
		self.rules = self.jsonLoad("spanishRules.json")
		self.verbs = {
			'comer' : '^com(o|e[sn]?|mos)$',
			'ir' : '^(v(oy|a(mos|[sn])?)$',
			'escribir' : '^escrib(o|e[sn]?|imos)$',
			'tomar' : '^tom(o|a([sn]|mos)?)$',
			'conocer' : '^cono(zco|ce([sn]|mos)?)$',
			'jugar' : '^ju(gamos|eg[oa][sn]?)$',
			'volver' : '^v(olvemos|uelv(o|e[sn]?))$',
			'leer' : '^le(o|e(mos|[sn])?)$',
			'estudiar' : '^estudi(o|a(mos|[sn])?)$',
			'recorrer' : '^recorr(o|[ae](mos|[sn])?)$'
		}

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
			for hash, verb in self.rules[char].iteritems():
				expr = '^('+'|'.join(hash.values())+')$'
				eval = re.compile(expr)
				if eval.match(text):
					return verb

		return None
        
	####################################################################
		

	
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

import re
import json
import subprocess as sp
import os

class GrammarRules:
	def jsonLoad(self, dbFile):
		f = open(dbFile, 'r')
		jsRules = f.read();
		f.close()
		return json.loads(jsRules)
		
	####################################################################
	
	def __init__(self):
		self.rules = self.jsonLoad("spanishRules.json")
		self.fromFile = 'loadFromFile2.sh'
		self.fromWeb = 'loadFromWeb3.sh'
		self.path = os.getcwd()
		self.text = ""


	####################################################################
	
	def isVerb(self):
		items = self.rules['verb']
		expr = '^(' + '|'.join(items) + ')$'
		return re.compile(expr)

	####################################################################
	
	def isDeterminer(self, text):
		for type, list in self.rules['determiner'].iteritems():
			expr = '^('+'|'.join(list)+')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################
	
	def isAdjetive(self, text):
		for type, list in self.rules['adjetive'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################
	
	def isSustantive(self, text):
		for type, list in self.rules['sustantive'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################
	
	def isPreposition(self, text):
		for type, list in self.rules['preposition'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################
	
	def isAdverb(self, text):
		for type, list in self.rules['adverb'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################
	
	def isPronom(self, text):
		for type, list in self.rules['pronom'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

	####################################################################

	def isInterjection(self, text):
		for type, list in self.rules['interjection'].iteritems():
			expr = '^(' + '|'.join(list) + ')$'
			eval = re.compile(expr)
			if eval.match(text):
				return type

		return None

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
		if text != "":
			char = text[0]
			if char in self.rules:
				for verb, hash in self.rules[char].iteritems():
					expr = '^('+'|'.join(hash.values())+')$'
					eval = re.compile(expr)
					if eval.match(text):
						return verb

		return None

	####################################################################
		
	def getVerbTense(self, verb, text):
		char = text[0]
		isIn = re.compile('^(ger|par|i([cpf]|nf|pi|pps?)|sp[i]?[2]?|sf)$')
		
		if char in self.rules:
			for tense, hash in self.rules[char][verb].iteritems():
				if isIn.match(tense):
					expr = '^'+hash+'$'
					eval = re.compile(expr)
					if eval.match(text):
						return tense
		
		return None

	####################################################################
		
	def getVerbPron(self, verb, text):
		char = text[0]
		isIn = re.compile('^(yo|tu|el_la|nos|uds|ellos)$')
		
		if char in self.rules:
			for pron, hash in self.rules[char][verb].iteritems():
				if isIn.match(pron):
					expr = '^'+hash+'$'
					eval = re.compile(expr)
					if eval.match(text):
						return pron
		
		return None
		
	####################################################################

	def getNltkType(self, idx):
		type = None
		try:
			type = self.rules["NLTK"][idx] if idx in self.rules["NLTK"] else '??'
		except ValueError:
			type = "??"
		
		return type 

	##########################################################################

	def loadFromFile(self,source):
		print "=> loadFromFile (%s)\n" % (source)
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromFile), source])

	##########################################################################

	def loadFromWeb(self,source):
		print "=> loadFromWeb (%s)\n" % (source)
		self.text = sp.check_output(['sh', "%s/%s" % (self.path,self.fromWeb), source])

	##########################################################################

	def word_tokenize(self, text):
		tokens = re.split('\s+', text)
		return tokens

	##########################################################################

	def pos_tag(self, tokens):
		list = []

		for token in tokens:
			tags = []
			type = "??"

			verb = self.getVerb(token)
			if verb is not None:
				type = self.getVerbTense(verb, token)
				if type is not None and self.getNltkType(type) is not None:
					tags.append(self.getNltkType(type))

			pron = self.isPronom(token)
			if pron is not None:
				tags.append(self.getNltkType(pron))

			adj = self.isAdjetive(token)
			if adj is not None:
				tags.append(self.getNltkType(adj))

			adv = self.isAdverb(token)
			if adv is not None:
				tags.append(self.getNltkType(adv))

			prep = self.isPreposition(token)
			if prep is not None:
				tags.append(self.getNltkType(prep))

			sust = self.isSustantive(token)
			if sust is not None:
				tags.append(self.getNltkType(sust))

			conj = self.isConjunction(token)
			if conj is not None:
				tags.append(self.getNltkType(conj))

			det = self.isDeterminer(token)
			if det is not None:
				tags.append(self.getNltkType(det))

			intj = self.isInterjection(token)
			if intj is not None:
				tags.append(self.getNltkType(intj))

			if len(tags) > 0:
				type = '|'.join(tags)

			list.append((token, type))

		return list
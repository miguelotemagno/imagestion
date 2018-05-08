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
		

	
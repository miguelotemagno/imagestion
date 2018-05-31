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

import json as js


class Function:
    def __init__(self, parent):
        # ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
        self.names = {
            'null':   self.null,
            'isVerb': self.isVerb,
            'isAdv':  self.isAdverb,
            'isNoun': self.isNoun,
            'isPrep': self.isPreposition,
            'isDet':  self.isDeterminant,
            'isConj': self.isConjunction,
            'isPron': self.isPronoun,
            'isAdj':  self.isAdjetive,
            'isIntj': self.isInterjection,
            'isNum':  self.isNumber,
            'isPunc': self.isPunctuation,
            'setNuc': self.setNucleous
        }

        self.dictionary = {
            'DET':  'isDet',
            'NOUN': 'isNoun',
            'ADJ':  'isAdj',
            'PREP': 'isPrep',
            'VERB': 'isVerb',
            'ADV':  'isAdv',
            'PRON': 'isPron',
            'INTJ': 'isIntj',
            'CONJ': 'isConj',
            'NUM':  'isNum',
            'PUNC': 'isPunc'
        }

        self.parent = parent

    ####################################################################

    def __str__(self):
        json = self.getJson()
        return js.dumps(json, sort_keys=True, indent=4, separators=(',', ': '))

    ####################################################################

    def getJson(self):
        return self.names.keys()

    ####################################################################

    def isVerb(self, args=None):
        try:
            if args['type'] == 'VERB':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isAdverb(self, args=None):
        try:
            if args['type'] == 'ADV':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isNoun(self, args=None):
        try:
            if args['type'] == 'NOUN':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isPreposition(self, args=None):
        try:
            if args['type'] == 'PREP':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isDeterminant(self, args=None):
        try:
            if args['type'] == 'DET':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isConjunction(self, args=None):
        try:
            if args['type'] == 'CONJ':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isPronoun(self, args=None):
        try:
            if args['type'] == 'PRON':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isAdjetive(self, args=None):
        try:
            if args['type'] == 'ADJ':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isInterjection(self, args=None):
        try:
            if args['type'] == 'INTJ':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isNumber(self, args=None):
        try:
            if args['type'] == 'NUM':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def isPunctuation(self, args=None):
        try:
            if args['type'] == 'PUNC':
                return args['node']
        except ValueError:
            return None

    ####################################################################

    def setNucleous(self, args=None):
        return None

    ####################################################################

    def null(self, args=None):
        return None

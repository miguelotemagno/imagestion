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

import numpy as np
import json as js
from GrammarRules import *
from Graph import *
import re

class SemanticNetwork:

    def __init__(self):
        self.rules = GrammarRules()
        self.grammarTypes = ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
        self.workflow = Graph(name='workflow', nodeNames=self.grammarTypes)
        self.connects = None
        pass

    ####################################################################

    def train(self, text, nucleous):
        self.connects = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        self.rules.setText(text)
        tokens = self.rules.pos_tag(self.rules.word_tokenize(text), False)
        length = len(tokens)
        i = 0

        for token in tokens:
            i += 1
            type = token[1]
            nextType = tokens[i][1] if i < length else None
            nextType = self.validType(nextType, tokens[i+1][1] if i+1 < length else None)
            type = self.validType(type, nextType)

            if nextType is not None and type is not None:
                # TODO corregir valor escalar asignado a x,y
                y = self.grammarTypes.index(type)
                x = self.grammarTypes.index(nextType)
                self.connects[y, x] += 1
                print "m[%s:%d,%s:%d] = %f" % (type,y,nextType,x,self.connects[y, x])

        return self.connects

    ####################################################################

    def validType(self, type, nextType=None):
        if type is None:
            return None

        if '|' in type:
            if nextType == 'NOUN' and 'DET' in type:
                type = 'DET'
            elif nextType == 'NOUN' and 'PREP' in type:
                type = 'PREP'
            elif nextType == 'NOUN' and 'PREP' in type:
                type = 'PREP'
            else:
                type = re.sub('([|]\w+)+', '', type)
        elif '??' in type:
            type = 'NOUN'

        return type

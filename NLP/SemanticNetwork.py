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
    """
            "inf"  : "infinitivo",
            "ger"  : "gerundio",
            "par"  : "participio",
            "ip"   : "indicativo presente" ,
            "ipi"  : "indicativo preterito imperfecto" ,
            "if"   : "indicativo futuro" ,
            "ic"   : "indicativo condicional",
            "ipps" : "indicativo preterito perfecto simple",
            "i"    : "imperativo" ,
            "sp"   : "subjuntivo presente" ,
            "spi"  : "subjuntivo preterito imperfecto" ,
            "spi2" : "subjuntivo preterito imperfecto 2" ,
            "sf"   : "subjuntivo futuro"
    """
    def __init__(self):
        self.rules = GrammarRules()
        self.grammarTypes = ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
        self.verbTenses = ['inf', 'ger', 'par', 'ip', 'ipi', 'if', 'ic', 'ipps', 'i', 'sp', 'spi', 'spi2', 'sf']
        self.pronouns = ['yo', 'tu', 'el_la', 'nos', 'uds', 'ellos']
        self.nouns = ['sustPropio', 'sustSimple', 'sustCompuesto', 'sustDespectivo', 'sustDisminutivo', 
                      'sustDerivado', 'sustAbstract', 'sustColectivo', 'sustAll', 'undefined']
        self.workflow = Graph(name='workflow', nodeNames=self.grammarTypes)
        self.nucleous = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        self.prevVerb = np.zeros((len(self.grammarTypes), len(self.verbTenses)),   dtype=float)
        self.postVerb = np.zeros((len(self.verbTenses),   len(self.grammarTypes)), dtype=float)
        self.pronVerb = np.zeros((len(self.verbTenses),   len(self.pronouns)),     dtype=float)
        self.nounVerb = np.zeros((len(self.verbTenses),   len(self.nouns)),        dtype=float)
        
        self.factVerb = 0
        self.factPreVerb = 0
        self.factPosVerb = 0
        self.factPronVrb = 0
        self.factNounVrb = 0        
        self.fileDb = None
        #self.load('semanticNet.json')
        pass

    ####################################################################

    def train(self, text, root):
        connects = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        finnish  = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        nucleous = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        prevVerb = np.zeros((len(self.grammarTypes), len(self.verbTenses)),   dtype=float)
        postVerb = np.zeros((len(self.verbTenses),   len(self.grammarTypes)), dtype=float)
        pronVerb = np.zeros((len(self.verbTenses),   len(self.pronouns)),     dtype=float)
        nounVerb = np.zeros((len(self.verbTenses),   len(self.nouns)),        dtype=float)

        self.rules.setText(text)
        tokens = self.rules.pos_tag(self.rules.word_tokenize(text), False)
        length = len(tokens)
        i = 0

        verb = self.rules.getVerb(root)
        tense = self.rules.getVerbTense(verb, root)
        pron = self.rules.getVerbPron(verb, root)
        z = self.verbTenses.index(tense)
        w = self.pronouns.index(pron)

        for token in tokens:
            i += 1
            word = token[0]
            type = token[1]
            nextWord = tokens[i][0] if i < length else None
            nextType = tokens[i][1] if i < length else None
            nextType = self.validType(nextType, tokens[i+1][1] if i+1 < length else None)
            type = self.validType(type, nextType)

            if nextType is not None and type is not None:
                print "m[%s,%s]" % (type, nextType)
                y = self.grammarTypes.index(type)
                x = self.grammarTypes.index(nextType)
                
                connects[y, x] += 1

                if word == root:
                    print "[%s,%s][%d,%d,%d,%d] -> %s {%s %s: %s}" % (type, nextType, x, y, z, w, root, tense, verb, self.rules.rules['_comment'][tense])
                    nucleous[y, x] += 1
                    prevVerb[y, z] += 1
                    pronVerb[z, w] += 1
                elif nextWord == root:
                    print "[%s,%s][%d,%d,%d,%d] -> %s {%s %s: %s}" % (type, nextType, x, y, z, w, root, tense, verb, self.rules.rules['_comment'][tense])
                    nucleous[y, x] += 1
                    postVerb[z, x] += 1
                elif type == 'NOUN':
                    noun = self.rules.isSustantive(word)
                    noun = 'undefined' if noun is None else noun
                    v = self.nouns.index(noun)
                    print "[%s,%s][%d,%d] -> %s {%s: %s %s}" % (tense, type, z, v, root, verb, self.rules.rules['_comment'][tense], noun)
                    nounVerb[z, v] += 1
                    
        listCnt = np.concatenate((connects.sum(axis=1), connects.sum(axis=0)), axis=0)
        listFin = np.concatenate((finnish.sum(axis=1),  finnish.sum(axis=0)),  axis=0)
        listNuc = np.concatenate((nucleous.sum(axis=1), nucleous.sum(axis=0)), axis=0)
        listPsV = np.concatenate((postVerb.sum(axis=1), postVerb.sum(axis=0)), axis=0)
        listPrV = np.concatenate((prevVerb.sum(axis=1), prevVerb.sum(axis=0)), axis=0)
        listPrn = np.concatenate((pronVerb.sum(axis=1), pronVerb.sum(axis=0)), axis=0)
        listNnV = np.concatenate((nounVerb.sum(axis=1), nounVerb.sum(axis=0)), axis=0)

        maxCnt = listCnt.max()
        maxFin = listFin.max()
        maxNuc = listNuc.max()
        maxPsV = listPsV.max()
        maxPrV = listPrV.max()
        maxPrn = listPrn.max()
        maxNnV = listNnV.max()

        newMatrixCnt = connects/maxCnt if maxCnt > 0 else connects
        newMatrixFin = finnish/maxFin if maxFin > 0 else finnish
        newMatrixNuc = nucleous/maxNuc if maxNuc > 0 else nucleous
        newPrevVerb  = prevVerb/maxPrV if maxPrV > 0 else prevVerb
        newPostVerb  = postVerb/maxPsV if maxPsV > 0 else postVerb
        newPronVerb  = pronVerb/maxPrn if maxPrn > 0 else pronVerb
        newNounVerb  = nounVerb/maxPrn if maxNnV > 0 else nounVerb

        oldMatrixCnt = self.workflow.connects
        oldMatrixFin = self.workflow.finnish
        oldMatrixNuc = self.nucleous
        oldPrevVerb  = self.prevVerb
        oldPostVerb  = self.postVerb
        oldPronVerb  = self.pronVerb
        oldNounVerb  = self.nounVerb
        oldFactorCnt = self.workflow.factor
        oldFactorFin = self.workflow.factFinnish
        oldFactorNuc = self.factVerb
        oldFactorPrV = self.factPreVerb
        oldFactorPsV = self.factPosVerb
        oldFactPrnVrb = self.factPronVrb
        oldFactNnVrb = self.factNounVrb

        if oldMatrixCnt.max() == 0:
            newFactorCnt = maxCnt
            newFactorFin = maxFin
            newFactorNuc = maxNuc
            newFactorPrV = maxPrV
            newFactorPsV = maxPsV
            newFactPrnVrb = maxPrn
            newFactNnVrb = maxNnV
        else:
            newFactorCnt  = maxCnt + oldFactorCnt
            newFactorFin  = maxFin + oldFactorFin
            newFactorNuc  = maxNuc + oldFactorNuc
            newFactorPrV  = maxPrV + oldFactorPrV
            newFactorPsV  = maxPsV + oldFactorPsV
            newFactPrnVrb = maxPrn + oldFactPrnVrb
            newFactNnVrb  = maxNnV + oldFactNnVrb

            newMatrixCnt = (oldMatrixCnt * oldFactorCnt) + connects
            newMatrixFin = (oldMatrixFin * oldFactorFin) + finnish
            newMatrixNuc = (oldMatrixNuc * oldFactorNuc) + nucleous
            newPrevVerb  = (oldPrevVerb * oldFactorPrV)  + prevVerb
            newPostVerb  = (oldPostVerb * oldFactorPsV)  + postVerb
            newPronVerb  = (oldPronVerb * oldFactPrnVrb) + pronVerb
            newNounVerb  = (oldNounVerb * oldFactNnVrb)  + nounVerb

            newMatrixCnt = newMatrixCnt/newFactorCnt if newFactorCnt > 0  else newMatrixCnt
            newMatrixFin = newMatrixFin/newFactorFin if newFactorFin > 0  else newMatrixFin
            newMatrixNuc = newMatrixNuc/newFactorNuc if newFactorNuc > 0  else newMatrixNuc
            newPrevVerb  = newPrevVerb/newFactorPrV  if newFactorPrV > 0  else newPrevVerb
            newPostVerb  = newPostVerb/newFactorPsV  if newFactorPsV > 0  else newPostVerb
            newPronVerb  = newPronVerb/newFactPrnVrb if newFactPrnVrb > 0 else newPronVerb
            newNounVerb  = newNounVerb/newFactNnVrb  if newFactNnVrb > 0  else newNounVerb

        self.workflow.iterations += 1
        self.workflow.connects = newMatrixCnt
        self.workflow.finnish = newMatrixFin
        self.nucleous = newMatrixNuc
        self.prevVerb = newPrevVerb
        self.postVerb = newPostVerb
        self.pronVerb = newPronVerb
        self.nounVerb = newNounVerb
        self.workflow.factor = newFactorCnt
        self.workflow.factFinnish = newFactorFin
        self.factVerb = newFactorNuc
        self.factPreVerb = newFactorPrV
        self.factPosVerb = newFactorPsV
        self.factPronVrb = newFactPrnVrb
        self.factNounVrb = newFactNnVrb

        if self.fileDb is not None:
            self.save(self.fileDb)

        return nounVerb

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

    ####################################################################

    def getJson(self):
        json = {
            'workflow': self.workflow.getJson(),
            'nucleous': self.nucleous.tolist(),
            'prevVerb': self.prevVerb.tolist(),
            'postVerb': self.postVerb.tolist(),
            'pronVerb': self.pronVerb.tolist(),
            'nounVerb': self.nounVerb.tolist(),
            'factVerb': self.factVerb,
            'factPreVerb': self.factPreVerb,
            'factPosVerb': self.factPosVerb,
            'factPronVrb': self.factPronVrb,
            'factNounVrb': self.factNounVrb
        }

        return json

    ####################################################################

    def __str__(self):
        return js.dumps(self.getJson(), sort_keys=True, indent=4, separators=(',', ': '))

    ####################################################################

    def save(self, dbFile):
        with open(dbFile, "w") as text_file:
            text_file.write(self.__str__())

    ####################################################################

    def importJSON(self, json):
        data = js.loads(json)
        self.workflow.importData(data['workflow'])
        self.factVerb = data['factVerb']
        self.factPreVerb = data['factPreVerb']
        self.factPosVerb = data['factPosVerb']
        self.factPronVrb = data['factPronVrb']
        self.factNounVrb = data['factNounVrb']
        self.nucleous = np.array(data['nucleous'], dtype=float)
        self.prevVerb = np.array(data['prevVerb'], dtype=float)
        self.postVerb = np.array(data['postVerb'], dtype=float)
        self.pronVerb = np.array(data['pronVerb'], dtype=float)
        self.nounVerb = np.array(data['nounVerb'], dtype=float)

    ####################################################################

    def load(self, dbFile):
        self.fileDb = dbFile
        f = open(self.fileDb, 'r')
        json = f.read()
        f.close()
        self.importJSON(json)

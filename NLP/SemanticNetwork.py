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
        self.endCondition = {}
        
        self.factVerb = 0
        self.factPreVerb = 0
        self.factPosVerb = 0
        self.factPronVrb = 0
        self.factNounVrb = 0
        self.factCondition = 0
        self.fileDb = None
        #self.load('semanticNet.json')
        pass

    ####################################################################
    # TODO se pretende implementar mismas funcionalidades aplicando librerias NLP de Google
    # TODO actualizar pip para python a la version 10.0.1 (pip install --upgrade pip)
    #      luego:   pip install --upgrade google-cloud-language


    def train(self, text, root):
        connects = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        finnish  = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        start    = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        nucleous = np.zeros((len(self.grammarTypes), len(self.grammarTypes)), dtype=float)
        prevVerb = np.zeros((len(self.grammarTypes), len(self.verbTenses)),   dtype=float)
        postVerb = np.zeros((len(self.verbTenses),   len(self.grammarTypes)), dtype=float)
        pronVerb = np.zeros((len(self.verbTenses),   len(self.pronouns)),     dtype=float)
        nounVerb = np.zeros((len(self.verbTenses),   len(self.nouns)),        dtype=float)
        endCondition = {}

        self.rules.setText(text)
        tokens = self.rules.normalize(self.rules.getSyntax(text))
        length = len(tokens)
        i = 0

        verb = self.rules.getVerb(root)
        tense = self.rules.getVerbTense(verb, root)
        pron = self.rules.getVerbPron(verb, root)
        z = self.getIndexof(tense, self.verbTenses)
        w = self.getIndexof(pron, self.pronouns)
        prevType = None
        lastType = None
        prevWord = None
        lastWord = None

        for token in tokens:
            i += 1
            word = token[0]
            type = token[1]
            nextWord = tokens[i][0] if i < length else None
            nextType = tokens[i][1] if i < length else None
            #nextType = self.rules.validType(nextType, tokens[i+1][1] if i+1 < length else None)
            #type = self.rules.validType(type, nextType)

            if nextType is not None and type is not None:
                print "m[%s,%s]   \t\t{ %s (%s), %s (%s) }" % (type, nextType, word, self.getIndexFromType(type, word), nextWord, self.getIndexFromType(nextType, nextWord))
                y = self.getIndexof(type, self.grammarTypes)
                x = self.getIndexof(nextType, self.grammarTypes)
                prevType = type
                lastType = nextType
                prevWord = word
                lastWord = nextWord

                connects[y, x] += 1

                if i == 1:
                    start[y, x] += 1

                if word == root:
                    print "postVerb[%s,%s] -> %s {%s, %s(%s: %s)}" % (type, nextType, root, type, tense, verb, self.rules.rules['_comment'][tense])
                    nucleous[y, x] += 1
                    postVerb[x, z] += 1
                    pronVerb[z, w] += 1
                elif nextWord == root:
                    print "prevVerb[%s,%s] -> %s {%s(%s: %s), %s}" % (type, nextType, root, tense, verb, self.rules.rules['_comment'][tense], nextType)
                    nucleous[y, x] += 1
                    prevVerb[z, y] += 1
                elif type == 'NOUN':
                    noun = self.rules.isNoun(word)
                    noun = 'undefined' if noun is None else noun
                    v = self.getIndexof(noun, self.nouns)
                    print "noun[%s,%s] -> %s {%s: %s}" % (tense, noun, root, verb, self.rules.rules['_comment'][tense])
                    nounVerb[z, v] += 1

        #print "[%s,%s]" % (prevType,lastType)
        if prevType is not None and lastType is not None:
            y = self.getIndexof(prevType, self.grammarTypes)
            x = self.getIndexof(lastType, self.grammarTypes)
            finnish[y, x] += 1

            idY = self.getIndexFromType(prevType, prevWord)
            idX = self.getIndexFromType(lastType, lastWord)
            key = "%s_%s" % (idY, idX)
            endCondition[key] = endCondition[key] + 1.0 if key in endCondition else 1.0

        listCnt = np.concatenate((connects.sum(axis=1), connects.sum(axis=0)), axis=0)
        listFin = np.concatenate((finnish.sum(axis=1),  finnish.sum(axis=0)),  axis=0)
        listStr = np.concatenate((start.sum(axis=1),    start.sum(axis=0)),    axis=0)
        listNuc = np.concatenate((nucleous.sum(axis=1), nucleous.sum(axis=0)), axis=0)
        listPsV = np.concatenate((postVerb.sum(axis=1), postVerb.sum(axis=0)), axis=0)
        listPrV = np.concatenate((prevVerb.sum(axis=1), prevVerb.sum(axis=0)), axis=0)
        listPrn = np.concatenate((pronVerb.sum(axis=1), pronVerb.sum(axis=0)), axis=0)
        listNnV = np.concatenate((nounVerb.sum(axis=1), nounVerb.sum(axis=0)), axis=0)
        listEnd = np.array(endCondition.values())

        maxCnt = listCnt.max()
        maxFin = listFin.max()
        maxStr = listStr.max()
        maxNuc = listNuc.max()
        maxPsV = listPsV.max()
        maxPrV = listPrV.max()
        maxPrn = listPrn.max()
        maxNnV = listNnV.max()
        maxEnd = listEnd.max()

        newMatrixCnt = connects/maxCnt if maxCnt > 0 else connects
        newMatrixFin = finnish/maxFin  if maxFin > 0 else finnish
        newMatrixStr = start/maxStr    if maxStr > 0 else start
        newMatrixNuc = nucleous/maxNuc if maxNuc > 0 else nucleous
        newPrevVerb  = prevVerb/maxPrV if maxPrV > 0 else prevVerb
        newPostVerb  = postVerb/maxPsV if maxPsV > 0 else postVerb
        newPronVerb  = pronVerb/maxPrn if maxPrn > 0 else pronVerb
        newNounVerb  = nounVerb/maxNnV if maxNnV > 0 else nounVerb
        newCondition = endCondition

        if maxEnd > 0:
            for idx in endCondition.keys():
                newCondition[idx] = endCondition[idx]/maxEnd

        oldMatrixCnt = self.workflow.connects
        oldMatrixFin = self.workflow.finnish
        oldMatrixStr = self.workflow.start
        oldMatrixNuc = self.nucleous
        oldPrevVerb  = self.prevVerb
        oldPostVerb  = self.postVerb
        oldPronVerb  = self.pronVerb
        oldCondition = self.endCondition

        oldNounVerb  = self.nounVerb
        oldFactorCnt = self.workflow.factor
        oldFactorFin = self.workflow.factFinnish
        oldFactorStr = self.workflow.factStart
        oldFactorNuc = self.factVerb
        oldFactorPrV = self.factPreVerb
        oldFactorPsV = self.factPosVerb
        oldFactPrnVrb = self.factPronVrb
        oldFactNnVrb = self.factNounVrb
        oldFactCondition = self.factCondition

        if oldMatrixCnt.max() == 0:
            newFactorCnt = maxCnt
            newFactorFin = maxFin
            newFactorStr = maxStr
            newFactorNuc = maxNuc
            newFactorPrV = maxPrV
            newFactorPsV = maxPsV
            newFactPrnVrb = maxPrn
            newFactNnVrb = maxNnV
            newFactCondition = maxEnd
        else:
            newFactorCnt  = maxCnt + oldFactorCnt
            newFactorFin  = maxFin + oldFactorFin
            newFactorStr  = maxFin + oldFactorStr
            newFactorNuc  = maxNuc + oldFactorNuc
            newFactorPrV  = maxPrV + oldFactorPrV
            newFactorPsV  = maxPsV + oldFactorPsV
            newFactPrnVrb = maxPrn + oldFactPrnVrb
            newFactNnVrb  = maxNnV + oldFactNnVrb
            newFactCondition = maxEnd + oldFactCondition

            newMatrixCnt = (oldMatrixCnt * oldFactorCnt) + connects
            newMatrixFin = (oldMatrixFin * oldFactorFin) + finnish
            newMatrixStr = (oldMatrixStr * oldFactorStr) + start
            newMatrixNuc = (oldMatrixNuc * oldFactorNuc) + nucleous
            newPrevVerb  = (oldPrevVerb * oldFactorPrV)  + prevVerb
            newPostVerb  = (oldPostVerb * oldFactorPsV)  + postVerb
            newPronVerb  = (oldPronVerb * oldFactPrnVrb) + pronVerb
            newNounVerb  = (oldNounVerb * oldFactNnVrb)  + nounVerb

            for idx in oldCondition.keys():
                oldValue = oldCondition[idx] if idx in oldCondition.keys() else 0.0
                newValue = endCondition[idx] if idx in endCondition.keys() else 0.0
                newCondition[idx] = oldValue * oldFactCondition + newValue
                newCondition[idx] = newCondition[idx]/newFactCondition if newFactCondition > 0 else newCondition[idx]

            newMatrixCnt = newMatrixCnt/newFactorCnt if newFactorCnt > 0  else newMatrixCnt
            newMatrixFin = newMatrixFin/newFactorFin if newFactorFin > 0  else newMatrixFin
            newMatrixStr = newMatrixStr/newFactorStr if newFactorStr > 0  else newMatrixStr
            newMatrixNuc = newMatrixNuc/newFactorNuc if newFactorNuc > 0  else newMatrixNuc
            newPrevVerb  = newPrevVerb/newFactorPrV  if newFactorPrV > 0  else newPrevVerb
            newPostVerb  = newPostVerb/newFactorPsV  if newFactorPsV > 0  else newPostVerb
            newPronVerb  = newPronVerb/newFactPrnVrb if newFactPrnVrb > 0 else newPronVerb
            newNounVerb  = newNounVerb/newFactNnVrb  if newFactNnVrb > 0  else newNounVerb

        self.workflow.iterations += 1
        self.workflow.connects = newMatrixCnt
        self.workflow.finnish = newMatrixFin
        self.workflow.start = newMatrixStr
        self.nucleous = newMatrixNuc
        self.prevVerb = newPrevVerb
        self.postVerb = newPostVerb
        self.pronVerb = newPronVerb
        self.nounVerb = newNounVerb
        self.endCondition = newCondition
        self.workflow.factor = newFactorCnt
        self.workflow.factFinnish = newFactorFin
        self.workflow.factStart = newFactorStr
        self.factVerb = newFactorNuc
        self.factPreVerb = newFactorPrV
        self.factPosVerb = newFactorPsV
        self.factPronVrb = newFactPrnVrb
        self.factNounVrb = newFactNnVrb
        self.factCondition = newFactCondition

        if self.fileDb is not None:
            self.save(self.fileDb)

        return finnish

    ####################################################################

    def getIndexFromType(self, type, word):
        types = {
            'DET':  self.rules.isDeterminer,  #(word),
            'NOUN': self.rules.isNoun,        #(word),
            'ADJ':  self.rules.isAdjetive,    #(word),
            'PREP': self.rules.isPreposition, #(word),
            'VERB': self.rules.getVerbTense,  #(verb, word),
            'ADV':  self.rules.isAdverb,      #(word),
            'PRON': self.rules.isPronom,      #(word),
            'INTJ': self.rules.isInterjection,#(word),
            'CONJ': self.rules.isConjunction, #(word),
            'NUM':  self.rules.isNumber,      #(word),
            'PUNC': self.rules.isPunctuation  #(word),
        }

        if type == 'VERB':
            verb = self.rules.getVerb(word)
            return types[type](verb, word) if verb is not None else None
        else:
            return types[type](word)


    ####################################################################

    def getJson(self):
        json = {
            'workflow': self.workflow.getJson(),
            'nucleous': self.nucleous.tolist(),
            'prevVerb': self.prevVerb.tolist(),
            'postVerb': self.postVerb.tolist(),
            'pronVerb': self.pronVerb.tolist(),
            'nounVerb': self.nounVerb.tolist(),
            'endCondition': self.endCondition,
            'factVerb': self.factVerb,
            'factPreVerb': self.factPreVerb,
            'factPosVerb': self.factPosVerb,
            'factPronVrb': self.factPronVrb,
            'factNounVrb': self.factNounVrb,
            'factCondition': self.factCondition
        }

        return json

    ####################################################################

    def __str__(self):
        return js.dumps(self.getJson(), sort_keys=True, indent=4, separators=(',', ': '))

    ####################################################################
    def printJson(self, var):
        return js.dumps(var, sort_keys=True, indent=4, separators=(',', ': '))

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
        self.factCondition = data['factCondition']
        self.nucleous = np.array(data['nucleous'], dtype=float)
        self.prevVerb = np.array(data['prevVerb'], dtype=float)
        self.postVerb = np.array(data['postVerb'], dtype=float)
        self.pronVerb = np.array(data['pronVerb'], dtype=float)
        self.nounVerb = np.array(data['nounVerb'], dtype=float)
        self.endCondition = data['endCondition']

    ####################################################################

    def load(self, dbFile):
        self.fileDb = dbFile
        f = open(self.fileDb, 'r')
        json = f.read()
        f.close()
        self.importJSON(json)

    ####################################################################

    def analize(self, text):
        expr = re.compile(r'(.+[.])')
        list = expr.findall(text)
        out = []

        if len(list) > 0:
            for txt in list:
                tokens = self.rules.normalize(self.rules.getSyntax(txt))
                struct = self.getSyntaxStruct(txt, tokens)
                #print self.printJson(struct)
                out.append(struct)
        else:
            tokens = self.rules.normalize(self.rules.getSyntax(text))
            struct = self.getSyntaxStruct(text, tokens)
            #print self.printJson(struct)
            out.append(struct)

        return out

    ####################################################################

    def isNucleous(self, typePrev, typeNext):
        y = self.workflow.getIndexof(typePrev)
        x = self.workflow.getIndexof(typeNext)

        if x is not None and y is not None:
            if self.nucleous[y, x] > 0.0:
                return True

        return False

    ####################################################################

    def isPreVerb(self, type, tense):
        y = self.getIndexof(type, self.grammarTypes)
        x = self.getIndexof(tense, self.verbTenses)

        if x is not None and y is not None:
            if self.prevVerb[y, x] > 0.0:
                return True

        return False
        #value = self.getPreVerb(type, tense)
        #return True if value is not None and value > 0.0 else False

    ####################################################################

    def setPreVerb(self, type, tense, n):
        y = self.getIndexof(type, self.grammarTypes)
        x = self.getIndexof(tense, self.verbTenses)

        if x is not None and y is not None:
            self.prevVerb[y, x] = n

    ####################################################################

    def getPreVerb(self, type, tense):
        x = self.getIndexof(type, self.grammarTypes)
        y = self.getIndexof(tense, self.verbTenses)

        return self.prevVerb[y, x] if x is not None and y is not None else None

    ####################################################################

    def isPostVerb(self, tense, type):
        y = self.getIndexof(type, self.grammarTypes)
        x = self.getIndexof(tense, self.verbTenses)

        if x is not None and y is not None:
            if self.postVerb[y, x] > 0.0:
                return True

        return False
        #value = self.getPostVerb(type, tense)
        #return True if value is not None and value > 0.0 else False

    ####################################################################

    def setPostVerb(self, type, tense, n):
        y = self.getIndexof(tense, self.verbTenses)
        x = self.getIndexof(type, self.grammarTypes)

        if x is not None and y is not None:
            self.postVerb[y, x] = n

    ####################################################################

    def getPostVerb(self, type, tense):
        y = self.getIndexof(tense, self.verbTenses)
        x = self.getIndexof(type, self.grammarTypes)

        return self.postVerb[y, x] if x is not None and y is not None else None

    ####################################################################

    def isFinnish(self, typePrev, typeNext):
        value = self.getFinnish(typePrev, typeNext)
        return True if value is not None and value > 0.0 else False

    ####################################################################

    def getFinnish(self, typePrev, typeNext):
        y = self.getIndexof(typePrev, self.grammarTypes)
        x = self.getIndexof(typeNext, self.grammarTypes)

        if x is not None and y is not None:
            return self.workflow.getFinnish(y, x)

        return None

    ####################################################################

    def setFinnish(self, typePrev, typeNext, n):
        y = self.getIndexof(typePrev, self.grammarTypes)
        x = self.getIndexof(typeNext, self.grammarTypes)

        if x is not None and y is not None:
            self.workflow.setFinnish(y, x, n)

    ####################################################################

    def getIndexof(self, type, arr):
        try:
            idx = arr.index(type)
        except ValueError:
            idx = None

        return idx

    ####################################################################

    def getSyntaxStruct(self, text, tokens):
        structs = []
        lenght = len(tokens)
        instances = []
        limit = 10
        prev = None
        post = None
        prevToken = None
        postToken = None
        i = 0
        idx = 0

        for token in tokens:
            # TODO hacer ciclo que recorra token por token buscando probabilidad de que un flujo de proseso se cumpla
            #      y abrir mas de una instancia de proceso en caso de que un patron de inicio se detecte y descartar el
            #      resto cuando una instancia respete un flujo completo. Construir estructura y retornarla.
            post = token[1]
            word = token[0]

            if i > 0:
                beyond = tokens[i+1][1] if i+1 < lenght else None
                prev = self.rules.validType(prev, post)
                post = self.rules.validType(post, beyond)
                isStart = self.workflow.isStart(prev, post)
                postToken = token

                if isStart and idx < limit:
                    newGraph = Graph()
                    newGraph.importData(self.workflow.getJson())
                    newGraph.id = i
                    newGraph.setInit(prev)
                    newGraph.data = {
                        'text': text,
                        'root': '',
                        'subject': [prevToken],
                        'predicate': []
                    }
                    instances.append(newGraph)
                    idx = lenght

                for flow in instances:
                    isNext = flow.isNext(prev, post)
                    isFinnish = flow.isFinnish(prev, post)

                    if isNext:
                        flow.setNext(post)
                        if flow.data is not None:
                            if flow.data['root'] == '':
                                flow.data['subject'].append(token)
                            else:
                                flow.data['predicate'].append(token)

                        precondition = self.isNucleous(prev, post)
                        postcondition = self.isNucleous(post, beyond)

                        if precondition and postcondition:  # isNucleous
                            verb = self.rules.getVerb(word)
                            if verb is not None and flow.data is not None:
                                tense = self.rules.getVerbTense(verb, word)
                                pron = self.rules.getVerbPron(verb, word)
                                preVerb = self.getPreVerb(prev, tense)
                                postVerb = self.getPostVerb(beyond, tense)

                                # TODO agregar condiciones de noun x verb para identificar el nucleo
                                if preVerb > 0 and postVerb > 0:
                                    flow.data['root'] = word
                            pass

                        elif isFinnish:
                            axisX = self.workflow.finnish.sum(axis=1)
                            xMax = axisX.max()
                            value = flow.isFinnish(prev, post)
                            prevWord = prevToken[0]
                            postWord = postToken[0]
                            idY = self.getIndexFromType(prev, prevWord)
                            idX = self.getIndexFromType(post, postWord)
                            key = "%s_%s" % (idY, idX)
                            isCondition = self.endCondition[key] if key in self.endCondition.keys() else 0

                            if flow.data is not None and flow.data['root'] != '' and value >= xMax and isCondition > 0:
                                structs.append(flow.data)
                                for f in instances:
                                    f.reset()
                    else:
                        flow.reset()
                        if flow.isStart(prev, post):
                            flow.setInit(prev)
                            flow.setNext(post)
                            flow.data = {
                                'text': text,
                                'root': '',
                                'subject': [prevToken, token],
                                'predicate': []
                            }
                    pass
                pass

            instances = [flow for flow in instances if flow.data is not None]

            i += 1
            prev = post
            prevToken = token

        return structs

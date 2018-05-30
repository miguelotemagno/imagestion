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
from json import dumps, loads
from Node import *
from Function import *

class Graph:
    # node names example: nodeNames = ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
    def __init__(self, name='', nodes=0, id='', nodeNames=[], firstNode=0):
        n = len(nodeNames) if len(nodeNames) > 0 else nodes
        self.name = name
        self.id = id
        self.nodeNames = ["Node%d" % (x) for x in range(n)] if n > 0 else []
        self.nodeNames = [x for x in range(len(self.nodeNames))] if len(self.nodeNames) > 0 else self.nodeNames
        self.nodes = [Node(id=x, name="%s" % (self.nodeNames[x])) for x in range(len(self.nodeNames))] if len(self.nodeNames) > 0 else []
        self.firstNode = firstNode
        self.connects = np.zeros(n,n)
        self.markovPrc = np.zeros(n,n)
        self.functions = Function()

    ####################################################################

    def load(self, dbFile):
        f = open(dbFile, 'r')
        jsNet = f.read();
        f.close()
        self.importJSON(jsNet)
        pass

    ####################################################################

    def save(self, dbFile):
        with open(dbFile, "w") as text_file:
            text_file.write(dumps(self.__str__(), sort_keys=True, indent=4, separators=(',', ': ')))
        pass

    ####################################################################

    def importJSON(self, js):
        data = loads(js)
        self.name = data['name']

    ####################################################################

    def __str__(self):
        js = self.getJson()
        return dumps(js, sort_keys=True,indent=4, separators=(',', ': '))

    ####################################################################

    def getJson(self):
        js = {
            'graph' : {
                'id': self.id,
                'name': self.name,
                'first': self.firstNode,
                'nodes' : [node.id for node in self.nodes]
            },
            'nodes' : [node.getJson() for node in self.nodes],
            'functions' : [self.functions.getJson()],
            'connects' : [self.connects.tolist()],
            'markovPrc' : [self.markovPrc.tolist()]
        }
        return js

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
from Node import *
from Function import *


class Graph:
    # node names example: nodeNames = ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
    def __init__(self, name='', nodes=0, id='', nodeNames=[], firstNode=0):
        n = len(nodeNames) if len(nodeNames) > 0 else nodes
        self.functions = Function(self)
        self.name = name
        self.id = id
        self.nodeNames = ["Node%d" % (x) for x in range(n)] if n > 0 else []
        self.nodeNames = nodeNames if len(nodeNames) > 0 else self.nodeNames

        self.nodes = [Node(self, id=x,
                           name="%s" % (self.nodeNames[x]),
                           function=self.getFunctionName(self.nodeNames[x]))
                      for x in range(len(self.nodeNames))] if len(self.nodeNames) > 0 else []

        self.firstNode = firstNode
        self.iterations = 0
        self.factor = 0
        self.connects = np.zeros((n, n), dtype=float)
        self.nucleous = np.zeros((n, n), dtype=float)

    ####################################################################

    def getFunctionName(self, x):
        try:
            idx = self.nodeNames.index(x)
        except ValueError:
            idx = -1

        return self.functions.dictionary[self.nodeNames[idx]] if idx is not None else 'null'

    ####################################################################

    def getIndexof(self, type):
        try:
            idx = self.functions.dictionary.keys().index(type)
        except ValueError:
            idx = None

        return idx

    ####################################################################

    def start(self, type):
        idx = self.getIndexof(type)
        node = self.nodes[self.firstNode] if idx is not None else None
        return node.isMyself(type) if node is not None else None

    ####################################################################

    def load(self, dbFile):
        f = open(dbFile, 'r')
        json = f.read()
        f.close()
        self.importJSON(json)
        pass

    ####################################################################

    def save(self, dbFile):
        with open(dbFile, "w") as text_file:
            text_file.write(self.__str__())
        pass

    ####################################################################

    def __str__(self):
        json = self.getJson()
        return js.dumps(json, sort_keys=True, indent=4, separators=(',', ': '))

    ####################################################################

    def getConnection(self, y, x):
        return self.connects.item((y, x))

    ####################################################################

    def setConnection(self, y, x, val):
        self.connects.itemset((y, x), val)

    ####################################################################

    def getConnectRow(self, y):
        return self.connects[y, :]

    ####################################################################

    def getConnectColumn(self, x):
        return self.connects[:, x]

    ####################################################################

    def getNuleous(self, y, x):
        return self.nucleous.item((y, x))

    ####################################################################

    def getNucleousRow(self, y):
        return self.nucleous[y, :]

    ####################################################################

    def getNucleousColumn(self, x):
        return self.nucleous[:, x]

    ####################################################################

    def setNucleous(self, y, x, val):
        self.nucleous.itemset((y, x), val)

    ####################################################################

    def getConnectionsNode(self, node):
        col = self.getConnectColumn(node.id)
        nodes = []

        for i in xrange(col):
            if col[i] > 0:
                nodes.append(self.nodes[i])

        return nodes

    ####################################################################

    def getEntriesNode(self, node):
        row = self.getConnectRow(node.id)
        nodes = []

        for i in xrange(row):
            if row[i] > 0:
                nodes.append(self.nodes[i])

        return nodes

    ####################################################################

    def getJson(self):
        json = {
            'graph': {
                'id': self.id,
                'name': self.name,
                'first': self.firstNode,
                'factor': self.factor,
                'iterations': self.iterations,
                'width': len(self.nodeNames),
                'height': len(self.nodeNames),
                'connects': [self.connects.tolist()],
                'nucleous': [self.nucleous.tolist()],
                'nodes': [node.id for node in self.nodes]
            },
            'functions': [self.functions.getJson()],
            'nodes': [node.getJson() for node in self.nodes]
        }
        return json

    ####################################################################

    def importJSON(self, json):
        data = js.loads(json)
        self.id = data['graph']['id']
        self.name = data['graph']['name']
        self.firstNode = data['graph']['first']
        self.iterations = data['graph']['iterations']
        self.factor = data['graph']['factor']
        width = data['graph']['width']
        height = data['graph']['height']

        for y in xrange(height):
            for x in xrange(width):
                self.connects[y][x] = data['graph']['connects'][y][x]
                self.nucleous[y][x] = data['graph']['nucleous'][y][x]


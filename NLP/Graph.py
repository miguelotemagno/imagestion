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

import json
from Node import *

class Graph:
    # node names example: nodeNames = ['DET', 'NOUN', 'ADJ', 'PREP', 'VERB', 'ADV', 'PRON', 'INTJ', 'CONJ', 'NUM', 'PUNC']
    def __init__(self, name='', nodes=0, id='', nodeNames=[]):
        self.name = name
        self.id = id
        self.nodeNames = ["Node%d" % (x) for x in range(nodes)] if nodes > 0 else []
        self.nodeNames = [nodeNames[x] % (x) for x in range(len(nodeNames))] if len(nodeNames) > 0 else self.nodeNames
        self.nodes = [Node(id=x, name="%s" % (self.nodeNames[x])) for x in range(len(self.nodeNames))] if len(self.nodeNames) > 0 else []

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
            text_file.write(json.dumps(self.exportJSON(), sort_keys=True, indent=4, separators=(',', ': ')))
        pass

    ####################################################################

    def importJSON(self, js):
        data = json.loads(js)
        self.name = data['name']

    ####################################################################

    def exportJSON(self):
        json = { }
        #    'id': self.nodos_ent,
        #    'name': self.nodos_sal,
        #    'nodes': [
        #        self.nodes[x] for x in range(self.nodes)
        #    ]
        #}
        return json

    ####################################################################
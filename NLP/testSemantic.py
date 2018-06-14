import sys
import re
from SemanticNetwork import *

s = SemanticNetwork()

if sys.argv[1] == 'web':
    pass


if sys.argv[1] == 'train':
    train = sys.argv[2] if sys.argv[2] is not None and sys.argv[2] != '' else 'semanticTrainer.txt'
    dbFile = sys.argv[3] if sys.argv[3] is not None and sys.argv[3] != '' else 'semanticNet.json'

    s.load(dbFile)
    text = sp.check_output(['sh', "%s/%s" % (s.rules.path, s.rules.fromFile), train])
    patterns = re.compile('((\w+|[ ,.;?()])+\S)\s+\((\w+)\)')
    list = text.split("\n")

    for line in list:
        expr = patterns.search(line)
        if expr:
            (frase, verb) = expr.group(1, 3)
            print "\n%s => [%s]" % (frase, verb)
            try:
                tokens = s.rules.word_tokenize(frase)
                syntax = s.rules.pos_tag(tokens, False)
                print(syntax)
                s.train(frase, verb)
            except ValueError:
                print(ValueError)
                continue

if sys.argv[1] == 'web':
    url = 'https://raw.githubusercontent.com/miguelotemagno/imagestion/imagestion_1.0/NLP/grammarTest.txt'
    if sys.argv[2] != '':
        url = sys.argv[2]

    s.rules.loadFromWeb(url)
    print s.rules.text
    list = s.analize(s.rules.text)
    print list

if sys.argv[1] == 'file':
    file = "grammarTest.txt"
    if sys.argv[2] != '':
        file = sys.argv[2]

    s.rules.loadFromFile(file)
    list = s.analize(s.rules.text)
    print list



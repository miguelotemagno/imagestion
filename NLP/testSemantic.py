import sys
import re
from SemanticNetwork import *

s = SemanticNetwork()

if sys.argv[1] == 'train':
    train = sys.argv[2] if sys.argv[2] is not None and sys.argv[2] != '' else 'semanticTrainer.txt'
    dbFile = sys.argv[3] if sys.argv[3] is not None and sys.argv[3] != '' else 'semanticNet.json'

    s.load(dbFile)
    text = sp.check_output(['sh', "%s/%s" % (s.rules.path, s.rules.fromFile), train])
    patterns = re.compile('((\w+|[ ,.;?()"])+\S)\s+\((\w+)\)')
    list = text.split("\n")

    for line in list:
        expr = patterns.search(line)
        if expr:
            (frase, verb) = expr.group(1, 3)
            print "\n%s => [%s]" % (frase, verb)
            try:
                syntax = s.rules.normalize(s.rules.getSyntax(frase))
                print(syntax)
                s.train(frase, verb)
            except ValueError:
                print(ValueError)
                continue

if sys.argv[1] == 'web':
    url = 'https://raw.githubusercontent.com/miguelotemagno/imagestion/imagestion_1.0/NLP/grammarTest.txt'
    if sys.argv[2] != '':
        url = sys.argv[2]

    dbFile = sys.argv[3] if sys.argv[3] is not None and sys.argv[3] != '' else 'semanticNet.json'
    s.load(dbFile)

    s.rules.loadFromWeb(url)
    #print s.rules.getSyntax(s.rules.text)
    list = s.analize(s.rules.text)
    for y in xrange(0, len(list)-1):
        if len(list[y]) > 0:
            print "nucleo:%s\nsujeto:{%s}\npredicado:{%s}\n" % (list[y][0]['root'], str(list[y][0]['subject']), str(list[y][0]['predicate']))

if sys.argv[1] == 'file':
    file = "grammarTest.txt"
    if sys.argv[2] != '':
        file = sys.argv[2]

    dbFile = sys.argv[3] if sys.argv[3] is not None and sys.argv[3] != '' else 'semanticNet.json'
    s.load(dbFile)

    s.rules.loadFromFile(file)
    list = s.analize(s.rules.text)
    for x in list:
        print "nucleo:%s\nsujeto:{%s}\npredicado:{%s}\n" % (x[0]['root'], str(x[0]['subject']), str(x[0]['predicate']))



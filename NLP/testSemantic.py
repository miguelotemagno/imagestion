import sys
import re
import multiprocessing
import time

from SemanticNetwork import *

start_time = time.time()

s = SemanticNetwork()

# ejemplo: python testSemantic.py train '' ''
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
            print "\nRAW: %s => [%s]" % (frase, verb)
            try:
                tokens = s.rules.getSyntax(frase)
                syntax = s.rules.normalize(tokens)
                print "1) tokens: %s" % str(tokens)
                print "2) syntax: %s" % str(syntax)
                print "3) train:"
                s.train(frase, verb)
                list = s.analize(frase)
                print "4) test: %s\n" % str(list)
                for item in list[0]:
                    print "%03d) texto:%s\n     nucleo:%s\n     sujeto:{%s}\n     predicado:{%s}\n" % (
                    0, item['text'], item['root'], str(item['subject']), str(item['predicate']))

            except ValueError:
                print(ValueError)
                continue

# ejemplo: python testSemantic.py web https://definicion.de/taoismo ''
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
            for item in list[y]:
                print "%03d) texto:%s\n     nucleo:%s\n     sujeto:{%s}\n     predicado:{%s}\n     tokens:{%s}\n" % (y, item['text'], item['root'], str(item['subject']), str(item['predicate']), str(item['tokens']))

# ejemplo: python testSemantic.py file serotoninaTrainTest.txt ''
if sys.argv[1] == 'file':
    file = "grammarTest.txt"
    if sys.argv[2] != '':
        file = sys.argv[2]

    dbFile = sys.argv[3] if sys.argv[3] is not None and sys.argv[3] != '' else 'semanticNet.json'
    s.load(dbFile)

    s.rules.loadFromFile(file)
    print s.rules.getSyntax(s.rules.text)
    list = s.analize(s.rules.text)

    for y in xrange(0, len(list)-1):
        if len(list[y]) > 0:
            for item in list[y]:
                print "%03d) texto:%s\n     nucleo:%s\n     sujeto:{%s}\n     predicado:{%s}\n     tokens:{%s}\n" % (y, item['text'], item['root'], str(item['subject']), str(item['predicate']), str(item['tokens']))


if sys.argv[1] == 'clean':
    dbFile = sys.argv[2] if sys.argv[2] is not None and sys.argv[2] != '' else 'semanticNet.json'
    s.save(dbFile)

print 'Done! Time taken: %f sec for %d CPUs' % (time.time() - start_time, multiprocessing.cpu_count())

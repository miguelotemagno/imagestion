from Red import *
import json

O = 0 #+0.000001
I = 1 #-0.000001

# Net(entradas,salidas,[nodos,...],[funciones])
net = Net(2,1,[2,2,1],['TANSIG','TANSIG','TANSIG'])
#net = Net(2,1,[2,2,1],['LOGSIG','LOGSIG','LOGSIG'])
net.debug = True
#net.min   = -1
#net.max   = 1

print ""
print 'NET   : Net(2,1,'+str(net.capas)+','+str(net.transferencias)+')'
print 'PESOS : '+str(net.getPesos())
print 'DELTA : '+str(net.getDeltas())
print 'ERROR : '+str(net.getErrores())
print ""

print "0 SIMULAR"
print str([O,O]) + ' => ' + str(net.feedForward([O,O]))
print str([O,I]) + ' => ' + str(net.feedForward([O,I]))
print str([I,O]) + ' => ' + str(net.feedForward([I,O]))
print str([I,I]) + ' => ' + str(net.feedForward([I,I]))
print ""

#f = open('neural-network.json', 'r')
f = open('referencia.json', 'r')
jsNet = f.read();
f.close()
net.setConfiguracion(jsNet)
 
print "1 SIMULAR"
print str([O,O]) + ' => ' + str(net.feedForward([O,O]))
print str([O,I]) + ' => ' + str(net.feedForward([O,I]))
print str([I,O]) + ' => ' + str(net.feedForward([I,O]))
print str([I,I]) + ' => ' + str(net.feedForward([I,I]))
print ""

print 'NET   : Net(2,1,'+str(net.capas)+','+str(net.transferencias)+')'
print 'PESOS : '+str(net.getPesos())
print 'DELTA : '+str(net.getDeltas())
print 'ERROR : '+str(net.getErrores())
print ""

print "print CONFIGURACION:"
print net.getConfiguracion();
#print dumps(net.getConfiguracion(), sort_keys=True,indent=4, separators=(',', ': '))
print ""
    
if net.panic:
    print "print LOG"
    print net.printLog()
    


#prueba 2

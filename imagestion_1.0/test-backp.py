from Red import *
import json
import time
import math

O = 0 #+ 0.000001
I = 1 #- 0.000001

# Net(entradas,salidas,[capa1,capa2,...],[funciones])
net = Net(2,1,[2,1],['TANSIG','TANSIG'])
#net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])
#net = Net(2,1,[2,1],['LOGSIG','TANSIG'])
net.debug = True

print ('NET      : Net(2,1,'+str(net.capas)+','+str(net.transferencias)+')')
print ('PESOS    : '+str(net.getPesos()))
print ('DELTA    : '+str(net.getDeltas()))
print ('LIST_ERR : '+str(net.getErrores()))

print ("0 SIMULAR")
print (str([O,O]) + ' => ' + str(net.feedForward([O,O])))
print (str([O,I]) + ' => ' + str(net.feedForward([O,I])))
print (str([I,O]) + ' => ' + str(net.feedForward([I,O])))
print (str([I,I]) + ' => ' + str(net.feedForward([I,I])))

for x in range(1):
    print (str(x+1)+" ENTRENAR")
    net.rate   = 0.5
    net.epochs = 1000
    #net.min    = -0.5
    #net.max    = 0.5
    net.umbralError = 0.001
    inputs  = [[O,O], [O,I], [I,O], [I,I]]
    outputs = [ [O],   [I],   [I],   [O] ]
    error = 1
    tryAgain = True

    while tryAgain:
        net.trainUntilConverge (inputs,outputs)
        
        OO = net.feedForward([0,0])
        OI = net.feedForward([0,1])
        IO = net.feedForward([1,0])
        II = net.feedForward([1,1])
        
        print([OO,OI,IO,II])
        
#        if math.fabs(OO[0]) < 0.5 and math.fabs(OI[0]) > 0.5 and math.fabs(IO[0]) > 0.5 and math.fabs(II[0]) < 0.5 :
#            tryAgain = False
#        else:
#            net.reInit()
#            
#        time.sleep(5)

        tryAgain = False    
        
    print (str(x+1)+" SIMULAR")
    print (str([O,O]) + ' => ' + str(net.feedForward([O,O])))
    print (str([O,I]) + ' => ' + str(net.feedForward([O,I])))
    print (str([I,O]) + ' => ' + str(net.feedForward([I,O])))
    print (str([I,I]) + ' => ' + str(net.feedForward([I,I])))

    print ('PESOS    : '+str(net.getPesos()))
    print ('DELTA    : '+str(net.getDeltas()))
    print ('LIST_ERR : '+str(net.getErrores()))
    print ('CUAD_ERR : '+str(net.error))


print ("\nprint CONFIGURACION:")
print (net.getConfiguracion())
 

with open("neural-network.json", "w") as text_file:
    text_file.write(dumps(net.getConfiguracion(), sort_keys=True,indent=4, separators=(',', ': ')))

print ("\nprint HISTORIAL:"+str(net.getHistorialLenght()))
#print (net.getHistorial())


#net.panic = True
    
if net.panic:
    print ("print LOG")
    print (net.printLog())
    

from Red import *
import json

O = 0 #0.000001
I = 1 #0.999999

# Net(entradas,salidas,[capa1,capa2,...],[funciones])
net = Net(2,1,[2,1],['TANSIG','TANSIG'])
#net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])
#net = Net(2,1,[2,2,1],['LOGSIG','TANSIG','TANSIG'])
net.debug = True

print ('NET   : Net(2,1,'+str(net.capas)+','+str(net.transferencias)+')')
print ('PESOS : '+str(net.getPesos()))
print ('DELTA : '+str(net.getDeltas()))
print ('ERROR : '+str(net.getErrores()))

print ("0 SIMULAR")
print (str([O,O]) + ' => ' + str(net.feedForward([O,O])))
print (str([O,I]) + ' => ' + str(net.feedForward([O,I])))
print (str([I,O]) + ' => ' + str(net.feedForward([I,O])))
print (str([I,I]) + ' => ' + str(net.feedForward([I,I])))

for x in range(1):
    print (str(x+1)+" ENTRENAR")
    net.rate   = 0.8
    net.epochs = 10
    #net.min    = -0.5
    #net.max    = 0.5
    #net.umbralError = 0.0001

    net.trainUntilConverge ([
            [O,O], [O,I], [I,O], [I,I]
        ],[
             [I],   [O],   [O],   [I]
        ])

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
print (net.getHistorial())


net.panic = True
    
if net.panic:
    print ("print LOG")
    print (net.printLog())
    

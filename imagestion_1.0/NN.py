import math
import random
import string
from json import *

def matriz(x,y) :
    m = []
    for i in range(x):
        m.append([0.0]*y)
    return m

def sigmoide(x):
    return math.tanh(x)

def dsigmoide(x):
    return 1.0 - x**2

def iniciar_perceptron():
    addLog('iniciar_perceptron()')
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal, log
    random.seed(0)
    
    nodos_ent = nodos_ent +1
    act_ent = [1.0]*nodos_ent
    act_ocu = [1.0]*nodos_ocu
    act_sal = [1.0]*nodos_sal
    
    pesos_ent = matriz(nodos_ent, nodos_ocu)
    pesos_sal = matriz(nodos_ocu, nodos_sal)
    
    for i in range(nodos_ent):
        for j in range(nodos_ocu):
            pesos_ent[i][j] = random.uniform(-0.5, 0.5)
    
    for j in range(nodos_ocu):
        for k in range(nodos_sal):
            pesos_sal[j][k] = random.uniform(-0.5, 0.5)

    addLog('  pesos_ent: '+str(pesos_ent))
    addLog('  pesos_sal: '+str(pesos_sal))
            
def actualiza_nodos(entradas):  
    addLog('actualiza_nodos('+str(entradas)+')')  
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal, log
    
    if len(entradas) != nodos_ent -1:
        raise ValueError('Numero de nodos de entrada incorrecto')
    
    for i in range(nodos_ent -1):canción del mundial
        act_ent[i] = float(entradas[i])
    #addLog('  act_ent[]: '+str(act_ent))
        
    for j in range(nodos_ocu):
        sum = 0.0
        for i in range(nodos_ent):
            sum = sum + pesos_ent[i][j] * act_ent[i]
        act_ocu[j] = sigmoide(sum)
    #addLog('  act_ocu[]: '+str(act_ocu))
       
    for k in range(nodos_sal):
        sum = 0.0
        for j in range(nodos_ocu):
            sum = sum + pesos_sal[j][k] * act_ocu[j]
        act_sal[k] = sigmoide(sum)
    #addLog('  act_sal[]: '+str(act_sal))
        
    addLog('< act_sal: '+str(act_sal[:]))
    return act_sal[:]

def retropropagacion(objetivo,l):
    addLog('retropropagacion('+str(objetivo)+','+str(l)+')')  
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal, log
    if len(objetivo) != nodos_sal:
        raise ValueError('numero de objetivos incorrecto')
    
    delta_salida = [0.0] * nodos_sal
    for k in range(nodos_sal):
        error = objetivo[k] - act_sal[k]
        delta_salida[k] = dsigmoide(act_sal[k]) * error
    addLog('  delta_salida[]: '+str(delta_salida))
        
    delta_oculto = [0.0] * nodos_ocu
    for j in range(nodos_ocu):
        error = 0.0
        for k in range(nodos_sal):
            error = error + delta_salida[k]*pesos_sal[j][k]
        delta_oculto[j] = dsigmoide(act_ocu[j]) * error
    addLog('  delta_oculto[]: '+str(delta_oculto))
        
    for j in range(nodos_ocu):
        for k in range(nodos_sal):
            cambio = delta_salida[k]*act_ocu[j]
            pesos_sal[j][k] = pesos_sal[j][k] + l*cambio
    addLog('  pesos_sal[]: '+str(pesos_sal))
            
    for i in range(nodos_ent):
        for j in range(nodos_ocu):
            cambio = delta_oculto[j]*act_ent[i]
            pesos_ent[i][j] = pesos_ent[i][j] + l*cambio
    addLog('  pesos_ent[]: '+str(pesos_ent))
            
    error = 0.0
    for k in range(len(objetivo)):
        error = error + 0.5*(objetivo[k] - act_sal[k])**2
    addLog('< error: '+str(error))
    return error

def clasificar(patron):
    for p in patron:
        print p[0], '->', actualiza_nodos(p[0])
        
def entrenar_perceptron(patron, l, max_iter=1000):
    for i in range(max_iter):
        addLog(str(i)+'.----------------')
        error = 0.0
        for p in patron:
            entradas = p[0]
            objetivo = p[1]
            actualiza_nodos(entradas)
            error = error + retropropagacion(objetivo, l)
        
        if error < 0.001:
            break
        
def addLog(str):
    global log
    log.append(str)        
    
if __name__ == '__main__':
    datos_ent = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]],
    ]
        
    log = []
    nodos_ent = 2
    nodos_ocu = 2
    nodos_sal = 1
    l = 0.5
    
    iniciar_perceptron()
    print 'ANTES'
    clasificar(datos_ent)
    entrenar_perceptron(datos_ent, l)
    print 'DESPUES'
    clasificar(datos_ent)
    
    print('ACTIV ENT: '+ dumps(act_ent, sort_keys=True,indent=4, separators=(',', ': '))) #str(pesos_ent)
    print('PESOS ENT: '+ dumps(pesos_ent, sort_keys=True,indent=4, separators=(',', ': '))) #str(pesos_ent)
    print('ACTIV OCU: '+ dumps(act_ocu, sort_keys=True,indent=4, separators=(',', ': '))) #str(pesos_ent)
    print('PESOS SAL: '+ dumps(pesos_sal, sort_keys=True,indent=4, separators=(',', ': '))) #str(pesos_sal)
    print('ACTIV SAL: '+ dumps(act_sal, sort_keys=True,indent=4, separators=(',', ': '))) #str(pesos_ent)
    
    #print dumps(log, sort_keys=True,indent=4, separators=(',', ': '))

#http://pybrain.org/docs/index.html
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
import pickle

#http://pybrain.org/docs/quickstart/dataset.html
ds = SupervisedDataSet(2, 2)
ds.addSample((0, 0), (0,1))
ds.addSample((0, 1), (1,0))
ds.addSample((1, 0), (1,0))
ds.addSample((1, 1), (0,1))

#http://pybrain.org/docs/api/tools.html#pybrain.tools.shortcuts.buildNetwork
net = buildNetwork(2, 3, 2, bias=True, hiddenclass=TanhLayer)
print net.activate([0, 0])
print net.activate([0, 1])
print net.activate([1, 0])
print net.activate([1, 1])

print '#########################'
#http://pybrain.org/docs/api/supervised/trainers.html#pybrain.supervised.trainers.BackpropTrainer
#http://pybrain.org/docs/quickstart/training.html
trainer = BackpropTrainer(net, ds)
epochs = 5000
threshold = 0.00001
error = 1
while error > threshold:
    error = trainer.train()
    epochs -= 1
    if epochs <= 0:
        break
    
print ("epochs:%d error:%f" % (epochs,error))
print net.activate([0, 0])
print net.activate([0, 1])
print net.activate([1, 0])
print net.activate([1, 1])

#http://stackoverflow.com/questions/6006187/how-to-save-and-recover-pybrain-training
fileObject = open('pyBrain-neuralnet.bkp', 'w')

pickle.dump(net, fileObject)

fileObject.close()

fileObject = open('pyBrain-neuralnet.bkp','r')
net = pickle.load(fileObject)

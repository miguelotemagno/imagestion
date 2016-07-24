from numpy import concatenate as con
from numpy import ones,mean,sign
from numpy.random import randn
from shogun.Features import Labels,RealFeatures
from shogun.Kernel import GaussianKernel
from shogun.Classifier import LibSVM

# http://www.shogun-toolbox.org/doc/en/3.0.0/modular_tutorial.html

num=1000; dist=1; width=2.1; C=1.0
traindata_real=con((randn(2,num)-dist,
randn(2,num)+dist), axis=1)
testdata_real=con((randn(2,num)-dist,
randn(2,num)+dist), axis=1)
trainlab=con((-ones(num), ones(num)))
testlab=con((-ones(num), ones(num)))

feats_train=RealFeatures(traindata_real)
kernel=GaussianKernel(feats_train, feats_train, width)
labels=Labels(trainlab)
svm=LibSVM(C, kernel, labels)
svm.train()
out=svm.classify(RealFeatures(testdata_real)).get_labels()
testerr=mean(sign(out)!=testlab)

print testerr

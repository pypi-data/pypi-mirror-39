import numpy as np
import matplotlib.pyplot as plt
from .PyNet.NeuralNetwork import NeuralNetwork as pNetwork

from . import Globals
from .Tools.BoxCox import BoxCoxNormalize

from .MNIST import GetMNISTData


def ReadCancerData():
	fname = Globals.DATA_PATH+'/breast-cancer/wdbc.data'
	f = open(fname,'r')
	lines = f.readlines()
	f.close()
	
	m = np.size(lines)
	for i in range(0,m):
		s = lines[i].strip().split(',')
		if i == 0:
			n = np.size(s)-2
			y = np.zeros(m,dtype='int32')
			X = np.zeros((m,n),dtype='float32')
		if s[1] == 'M':
			y[i] = 2
		else:
			y[i] = 1
		X[i] = np.float32(s[2:])
	return X,y


	


def GetCancerNN(Layers=[None,20,2],L1=0.0,L2=0.0,Normalize='BC',nSigma=1.0,Split=0.8,ActFuncs='sigmoid',CostFunction='cross-entropy'):
	
	X,y = ReadCancerData()
	n = X.shape[1]
	
	if Normalize is 'BC':
		for i in range(0,n):
			X[:,i],_,_,_,_ = BoxCoxNormalize(X[:,i],nSigma)
	elif Normalize in ['normal','gaussian']:
		for i in range(0,n):
			mu = np.mean(X[:,i])
			sig = np.std(X[:,i])*nSigma
			X[:,i] = (X[:,i] - mu)/sig
	elif Normalize is 'range':
		for i in range(0,n):
			r0 = np.min(X[:,i])
			r1 = np.max(X[:,i])
			X[:,i] = (X[:,i]-r0)/(r1-r0)		
	else:
		pass
		
#	ind = np.arange(y.size)
#	np.random.shuffle(ind)
#	
#	X = X[ind,:]
#	y = y[ind]
	
	
	
	Layers[0] = n
	
	net = pNetwork(Layers,L1,L2,ActFuncs=ActFuncs,CostFunction=CostFunction)
	
	net.StoreInputData(X,y,Split)
	net.InputStoredData()
	return net




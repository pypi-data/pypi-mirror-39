import numpy as np
from . import Globals

def _CreateNetwork(nN,Layers,Lambda,ThetaRange):
	L = np.zeros(len(Layers),dtype='int32')
	for i in range(0,nN):
		L[i] = np.size(Layers[i])
		
	s = np.zeros(np.sum(L),dtype='int32')
	n = 0
	for i in range(0,nN):
		s[n:n+np.size(Layers[i])] = Layers[i]
		n+=L[i]
	
	lam = np.array(Lambda).astype('float32')
	rnge = np.array(ThetaRange).astype('float32')
	
	nn = np.int32(nN)
	
	ins = Globals._CppCreateNetwork(nn,L,s,lam,rnge)
	return ins

def _DestroyNetwork(instance):
	ins = np.int32(instance)
	Globals._CppDestroyNetwork(ins)
	
def _LoadNetwork(n,fname):
	nn = np.int32(n)
	Fname = fname.encode('utf-8')
	ins = Globals._CppLoadNetwork(nn,Fname)
	s = []
	for i in range(0,n):
		s.append(_Gets(ins,i))
	return s,ins
	
def _SaveNetwork(instance,fname):
	ins = np.int32(instance)
	Fname = fname.encode('utf-8')
	Globals._CppSaveNetwork(ins,Fname)
	
def _InputTrainingData(instance,i,Xin,yin,verb):
	nN = len(Xin)
	
	ins = np.int32(instance)
	x = np.array(Xin).astype('float32')
	xshape = np.array(x.shape).astype('int32')
	x = x.flatten()
	y = np.array(yin).astype('int32')
	ylen = np.int32(y.size)
	I = np.int32(i)
	verb = np.bool(verb)
	Globals._CppInputTrainingData(ins,I,xshape,x,ylen,y,verb)
	
def _InputCrossValidationData(instance,i,Xin,yin,verb):
	ins = np.int32(instance)
	x = np.array(Xin).astype('float32')
	xshape = np.array(x.shape).astype('int32')
	x = x.flatten()
	y = np.array(yin).astype('int32')
	ylen = np.int32(y.size)
	I = np.int32(i)
	verb = np.bool(verb)
	Globals._CppInputCrossValidationData(ins,I,xshape,x,ylen,y,verb)


def _TrainGradientDescent(instance,MaxIter, Alpha,verb):
	ins = np.int32(instance)
	maxiter = np.int32(MaxIter)
	alpha = np.float32(Alpha)
	verb = np.bool(verb)
	Globals._CppTrainGradientDescent(ins,maxiter,alpha,verb)
	
def _TrainGradientDescentSingle(instance,i,MaxIter, Alpha,verb):
	ins = np.int32(instance)
	I = np.int32(i)
	maxiter = np.int32(MaxIter)
	alpha = np.float32(Alpha)
	verb = np.bool(verb)
	Globals._CppTrainGradientDescentSingle(ins,I,maxiter,alpha,verb)
	
def _GetnSteps(instance,nN):
	ins = np.int32(instance)
	nSteps = np.zeros(nN,dtype='int32')
	Globals._CppGetnSteps(ins,nSteps)
	
	return nSteps
	
def _GetTrainingProgress(instance,i,nN):
	ins = np.int32(instance)
	n = _GetnSteps(instance,nN)
	J = np.zeros(n[i],dtype='float32')
	Acc = np.zeros(n[i],dtype='float32')
	I = np.int32(i)
	Globals._CppGetTrainingProgress(ins,I,J,Acc)
	
	return J,Acc
	
def _GetCrossValidationProgress(instance,i,nN):
	ins = np.int32(instance)
	n = _GetnSteps(instance,nN)
	J = np.zeros(n[i],dtype='float32')
	Acc = np.zeros(n[i],dtype='float32')
	I = np.int32(i)
	Globals._CppGetCrossValidationProgress(ins,I,J,Acc)
	
	return J,Acc


def _ClassifyData(instance,i,Xin,k):
	ins = np.int32(instance)
	x = np.array(Xin).astype('float32')
	xshape = np.array(x.shape).astype('int32')
	m = np.int32(xshape[0])
	x = x.flatten()	
	y = np.zeros(m,dtype='int32')
	sm = np.zeros(m*k,dtype='float32')
	I = np.int32(i)
	Globals._CppClassifyData(ins,i,xshape,x,m,y,sm)
	sm = sm.reshape((m,k))
	return y,sm

def _GetL(instance,i):
	ins = np.int32(instance)
	I = np.int32(i)
	L = Globals._CppGetL(ins,I)
	return L
	
def _Gets(instance,i):
	ins = np.int32(instance)
	I = np.int32(i)
	L = _GetL(instance,i)
	s = np.zeros(L,dtype='int32')
	Globals._CppGets(ins,I,s)
	return s	

def _CreateEvolutionaryNetwork(nNetworks,nInput,nOutput,nTop,nCrap,nHrange,lwrange,lambdarange,alpharange):
	nN = np.int32(nNetworks)
	nIn = np.int32(nInput)
	nOut = np.int32(nOutput)
	nT = np.int32(nTop)
	nC = np.int32(nCrap)
	nHr = np.array(nHrange).astype('int32')
	lwr = np.array(lwrange).astype('int32')
	lmr = np.array(lambdarange).astype('float32')
	alr = np.array(alpharange).astype('float32')
	Globals._CppCreateEvolutionaryNetwork(nN,nIn,nOut,nT,nC,nHr,lwr,lmr,alr)
	

def _DestroyEvolutionaryNetwork():
	Globals._CppDestroyEvolutionaryNetwork()
	
def _EvolutionaryNetworkInputData(Xin,yin,FractionTrain):
	x = np.array(Xin).astype('float32')
	xshape = np.array(x.shape).astype('int32')
	x = x.flatten()
	y = np.array(yin).astype('int32')
	m = np.int32(y.size)
	f = np.float32(FractionTrain)
	Globals._CppEvolutionaryNetworkInputData(x,m,y,f)
	
def _EvolutionaryNetworkEvolve(nGens,MaxIter,Pmutate,MaxMutateSize,verb):
	
	ng = np.int32(nGens)
	mi = np.int32(MaxIter)
	pm = np.float32(Pmutate)
	ms = np.float32(MaxMutateSize)
	v = np.bool(verb)
	
	Globals._CppEvolutionaryNetworkEvolve(ng,mi,pm,ms,v)
	

import numpy as np
import time
import matplotlib.pyplot as plt
import os
import copy
from .. import Globals
from ..CostFunctions.MeanSquareCost import MeanSquareCost,MeanSquareDelta
from ..CostFunctions.CrossEntropyCost import CrossEntropyCost,CrossEntropyDelta
from ..ActivationFunctions.Softmax import Softmax
from ..Tools.MultiProgressBar import MultiProgressBar
from ColorString import ColorString

set_GD = {			'nEpoch':100,
					'MiniBatchSize':10,
					'Alpha':1.0,
					'gTol':0.0,
					'gTolEpochs':10,
					'gTolMinEpochs':10,
					'EarlyStop':True,
					'Momentum':0.0,
					'LocalGain':False,
					'GainLimits':[0.01,100.0],
					'GainSteps':[0.95,0.05],
					'Decay':0.9}

set_Nesterov = {	'nEpoch':100,
					'MiniBatchSize':10,
					'Alpha':1.0,
					'gTol':0.0,
					'gTolEpochs':10,
					'gTolMinEpochs':10,
					'EarlyStop':True,
					'Momentum':0.5,
					'LocalGain':False,
					'GainLimits':[0.01,100.0],
					'GainSteps':[0.95,0.05],
					'Decay':0.9}

set_RProp = {		'nEpoch':100,
					'MiniBatchSize':None,
					'Alpha':1.0,
					'gTol':0.0,
					'gTolEpochs':10,
					'gTolMinEpochs':10,
					'EarlyStop':False,
					'Momentum':0.0,
					'LocalGain':True,
					'GainLimits':[0.000001,50.0],
					'GainSteps':[0.5,1.2],
					'Decay':0.9}

set_RMSProp = {		'nEpoch':100,
					'MiniBatchSize':10,
					'Alpha':0.001,
					'gTol':0.0,
					'gTolEpochs':10,
					'gTolMinEpochs':10,
					'EarlyStop':False,
					'Momentum':0.0,
					'LocalGain':True,
					'GainLimits':[0.000001,50.0],
					'GainSteps':[0.5,1.2],
					'Decay':0.9}
			




class NeuralNetwork (object):
	def __init__(self,Layers,L1=0.0,L2=0.0,Ind=0,FT=False,ActFuncs='sigmoid',CostFunction='cross-entropy'):
		if isinstance(Layers,str):
			#load network
			self.LoadNetwork(Layers)
		else:
			self.Trained = False
			self.L = np.size(Layers)
			self.s = np.array(Layers)
			self.L1 = L1
			self.L2 = L2
			
			self.ActFuncs = ActFuncs
			self._PopulateActFuncs()
			self._SetCostFunction(CostFunction)

			#is this a forward-thinking NN?
			self.FT = FT
			
			#random initialization of Theta
			self.ResetWeights()
			
			#initialize some accuracy variables (Training and Cross-Validation)
			self.At = np.array([0],dtype='float32')
			self.Ac = np.array([0],dtype='float32')
			self.Atest = np.array([0],dtype='float32')
			
			#initialize cost
			self.Jt = np.array([0],dtype='float32')
			self.JtClass = np.array([0],dtype='float32')
			self.Jc = np.array([0],dtype='float32')
			self.Jtest = np.array([0],dtype='float32')
			
			#initialize datasets
			self.m = 0
			self.mt = 0
			self.mc = 0
			self.mtest = 0
			self.X = np.array([],dtype='float64')
			self.y = np.array([],dtype='float64')
			self.Xt = np.array([],dtype='float64')
			self.yt = np.array([],dtype='float64')
			self.Xc = np.array([],dtype='float64')
			self.yc = np.array([],dtype='float64')
			self.Xtest = np.array([],dtype='float64')
			self.ytest = np.array([],dtype='float64')
						
			self.TData = False
			self.CData = False
			self.TestData = False
			self.nSteps = 0
	
	def _SetCostFunction(self,CostFunction):
		self.CostFunction = CostFunction
		#select cost function to use
		if CostFunction == 'mean-squared':
			self.CF = MeanSquareCost
			self.CFDelta = MeanSquareDelta
		else:
			self.CF = CrossEntropyCost
			self.CFDelta = CrossEntropyDelta			
	
	def _PopulateActFuncs(self):
		#list activation functions and gradients
		if self.ActFuncs is None:
			self.AFname = np.array(['sigmoid']*(self.L-1))
		elif isinstance(self.ActFuncs,str):
			self.AFname = np.array([self.ActFuncs]*(self.L-1))
		else:
			afn = []
			for i in range(0,self.L-1):
				if i < np.size(self.ActFuncs):
					afn.append(self.ActFuncs[i])
				else:
					afn.append('sigmoid')
			self.AFname = np.array(afn)
				
		self.AF = np.zeros(self.L-1,dtype='object')
		self.AFgrad = np.zeros(self.L-1,dtype='object')
			
		for i in range(0,self.L-1):
			self.AF[i],self.AFgrad[i] = Globals.ActFuncs[self.AFname[i].lower()]
		
	
	def ResetNetwork(self,DeleteData=False):
		#random initialization of Theta
		self.ResetWeights()
			
		#initialize some accuracy variables (Training and Cross-Validation)
		self.At = np.array([0],dtype='float32')
		self.Ac = np.array([0],dtype='float32')
		self.Atest = np.array([0],dtype='float32')
			
		#initialize cost
		self.Jt = np.array([0],dtype='float32')
		self.JtClass = np.array([0],dtype='float32')
		self.Jc = np.array([0],dtype='float32')
		self.Jtest = np.array([0],dtype='float32')
		self.nSteps = 0	
			
		if DeleteData:
			#initialize datasets
			self.m = 0
			self.mt = 0
			self.mc = 0
			self.X = np.array([],dtype='float64')
			self.y = np.array([],dtype='float64')
			self.Xt = np.array([],dtype='float64')
			self.yt = np.array([],dtype='float64')
			self.Xc = np.array([],dtype='float64')
			self.yc = np.array([],dtype='float64')
			
			self.TData = False
			self.CData = False
				
	
	def ResetWeights(self):
		self.ThetaW = []
		self.ThetaB = []
		self.TrainLayers = np.ones(self.L-1,dtype='bool')
		for j in range(0,self.L-1):
			self.ThetaW.append(np.random.randn(self.s[j],self.s[j+1]).astype('float64')/np.sqrt(self.s[j]))
			self.ThetaB.append(np.random.randn(1,self.s[j+1]).astype('float64'))

	def ChangeNetworkArchitecture(self,Layers):
		#input and output layers are not to be changed
		s = np.copy(self.s)
		Layers[0] = self.s[0]
		Layers[-1] = self.s[-1]
		
		self.Trained = False
		self.L = np.size(Layers)
		self.s = np.array(Layers)
		self.ResetWeights()	
		
		olds = '['
		for i in range(0,s.size):
			if i > 0:
				olds += ','
			olds += '{:4d}'.format(s[i])
		olds += ']'
		
		news = '['
		for i in range(0,self.s.size):
			if i > 0:
				news += ','
			news += '{:4d}'.format(self.s[i])
		news += ']'

		#almost forgot - change propagation arrays
		if self.TData:
			self._zt,self._at = self._GetPropagationArrays(self.Xt)
		if self.CData:
			self._zc,self._ac = self._GetPropagationArrays(self.Xc)
		
		print(len(self.AF))
		self._PopulateActFuncs()
		print(len(self.AF))
		print('!!!!! Changed NN architecture from {:s} to {:s} !!!!!'.format(olds,news))
		print('Please retrain me!!!!')


	def InsertHiddenLayer(self,N):
		'''
		This will add a single layer of size N between the last hidden layer and the output layer
		for use with forward thinking DNNs
		'''

		olds = '['
		for i in range(0,self.s.size):
			if i > 0:
				olds += ','
			olds += '{:4d}'.format(self.s[i])
		olds += ']'
		
		#firstly - copy weights
		ThetaW = copy.deepcopy(self.ThetaW)
		ThetaB = copy.deepcopy(self.ThetaB)
		
		#secondly - create new L and s
		self.L+=1
		self.s = np.concatenate((self.s[:-1],[N],[self.s[-1]]))

		news = '['
		for i in range(0,self.s.size):
			if i > 0:
				news += ','
			news += '{:4d}'.format(self.s[i])
		news += ']'

		#thirdly - create new weight arrays
		self.ResetWeights()
		if self.FT:
			self.TrainLayers[:-2] = False
		
		#finally - insert old weights where the network hasn't changed
		for i in range(0,self.L-3):
			self.ThetaW[i] = ThetaW[i]
			self.ThetaB[i] = ThetaB[i]
		print('!!!!! Changed NN architecture from {:s} to {:s} !!!!!'.format(olds,news))
		
		#almost forgot - change propagation arrays
		if self.TData:
			self._zt,self._at = self._GetPropagationArrays(self.Xt)
		if self.CData:
			self._zc,self._ac = self._GetPropagationArrays(self.Xc)
		
		self._PopulateActFuncs()
		

	def StoreInputData(self,Xin,yin,Split=0.8):
		#store data to be split up into training and cross validation sets later
		self.X = Xin
		self.y = yin
		self.m = self.X.shape[0]
		self.Split = Split
		
	def InputStoredData(self):
		
		#start by counting the number of unique y values
		if self.y.ndim == 1:
			ytmp = np.copy(self.y)
			yunq = np.unique(ytmp)
			nu = yunq.size
		else:
			nu = self.y.shape[1]
			ytmp = np.zeros(self.y.shape[0],dtype='int32')
			yunq = np.arange(nu,dtype='int32') + 1
			for i in range(0,nu):
				use = np.where(self.y[:,i] == 1)[0]
				ytmp[use] = i + 1
		Xtmp = np.copy(self.X) 	

		#calculate the split for each y value
		mts = np.zeros(nu,dtype='int32')
		mcs = np.zeros(nu,dtype='int32')
		for i in range(0,nu):
			use = np.where(ytmp == i+1)[0]
			mts[i] = np.int32(self.Split*use.size)
			mcs[i] = use.size - mts[i]
		mt = np.sum(mts)
		mc = np.sum(mcs)


		
		#create empty arrays
		Xt = np.zeros((mt,self.X.shape[1]),dtype='float64')
		yt = np.zeros(mt,dtype='int32')
		Xc = np.zeros((mc,self.X.shape[1]),dtype='float64')
		yc = np.zeros(mc,dtype='int32')
		
		
		#split data 
		pt = 0
		pc = 0
		for i in range(0,nu):
			use = np.where(ytmp == i + 1)[0]
			np.random.shuffle(use)
			uset = use[:mts[i]]
			usec = use[mts[i]:]
			
			
			Xt[pt:pt+uset.size] = Xtmp[uset]
			yt[pt:pt+uset.size] = ytmp[uset]
			Xc[pc:pc+usec.size] = Xtmp[usec]
			yc[pc:pc+usec.size] = ytmp[usec]	
			pt+=uset.size
			pc+=usec.size
				
		self.InputTrainingData(Xt,yt)
		self.InputCrossValidationData(Xc,yc)

	def _GetOneHotClassLabels(self,y):
		m = np.size(y)
		k = self.s[-1]
		ind_offset = np.arange(m)*k
		yout = np.zeros((m,k))
		yout.flat[np.int32(ind_offset + y.ravel()-1)] = 1
		return yout		

	def LoadNetwork(self,FileName):
		if os.path.isfile(FileName+'.nn') == False:
			print('file not found')
			return None

	
		f = open(FileName+'.nn','rb')
		#firstly load some architecture information
		self.Trained = self._ScalarFromFile('bool8',f)
		self.L = self._ScalarFromFile('int32',f)
		self.s = self._ArrayFromFile('int32',f)
		self.L1 = self._ScalarFromFile('float32',f)
		self.L2 = self._ScalarFromFile('float32',f)
		self.FT = self._ScalarFromFile('float32',f)
		self.ActFuncs = self._StringsFromFile(f)
		self.CostFunction = self._StringsFromFile(f)
		self._PopulateActFuncs()
		self._SetCostFunction(self.CostFunction)
		
		#next load training data
		self.TData = self._ScalarFromFile('bool8',f)
		self.mt = self._ScalarFromFile('bool8',f)
		if self.TData:
			self.Xt = self._ArrayFromFile('float64',f)
			self.yt0 = self._ArrayFromFile('float64',f)
			self.InputTrainingData(self.Xt,self.yt0)
		

		#next load training data
		self.CData = self._ScalarFromFile('bool8',f)
		self.mc = self._ScalarFromFile('bool8',f)
		if self.CData:
			self.Xc = self._ArrayFromFile('float64',f)
			self.yc0 = self._ArrayFromFile('float64',f)
			self.InputCrossValidationData(self.Xc,self.yc0)

		#next load training data
		self.TestData = self._ScalarFromFile('bool8',f)
		self.mtest = self._ScalarFromFile('bool8',f)
		if self.TestData:
			self.Xtest = self._ArrayFromFile('float64',f)
			self.ytest0 = self._ArrayFromFile('float64',f)	
			self.InputTestData(self.Xtest,self.ytest0)
		
		#load any training information
		self.nSteps = self._ScalarFromFile('int32',f)
		self.Jt = self._ArrayFromFile('float32',f)
		self.JtClass = self._ArrayFromFile('float32',f)
		self.Jc = self._ArrayFromFile('float32',f)
		self.Jtest = self._ArrayFromFile('float32',f)
		self.At = self._ArrayFromFile('float32',f)
		self.Ac = self._ArrayFromFile('float32',f)
		self.Atest = self._ArrayFromFile('float32',f)
		self.TrainLayers = self._ArrayFromFile('bool8',f)
		
		#load weights and biases
		self.ThetaW = self._ListArrayFromFile('float64',f)
		self.ThetaB = self._ListArrayFromFile('float64',f)
		
		#if there is a best set of weights then load those too
		hasbest = self._ScalarFromFile('bool8',f)
		if hasbest:
			self.BestCVScore = self._ScalarFromFile('float32',f)
			self.BestThetaW = self._ListArrayFromFile('float64',f)
			self.BestThetaB = self._ListArrayFromFile('float64',f)
		f.close()
		print('Finished loading: '+FileName)


	def InputTrainingData(self,Xin,yin,verb=True):
		txsize = Xin.shape
		tysize = yin.shape
		if txsize[1] != self.s[0]:
			print('Xin needs to have the dimensions (m,s1), where m is the number of training samples and s1 is equal to the number of units in the input layer of the network')
			return
		self.mt = txsize[0]
		if (tysize[0] != self.mt):
			print('yin must have the dimensions (m,), where m is the number of training samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs')
			return
		self.Xt = np.zeros((self.mt,self.s[0]),dtype='float64')
		self.Xt[:] = np.array(Xin)
		self.yt0 = np.array(yin)

		if np.size(tysize) == 1:
			self.yt = self._GetOneHotClassLabels(self.yt0)
		else:
			self.yt = self.yt0

		self._zt,self._at = self._GetPropagationArrays(self.Xt)
		
		self.TData = True
	
	def InputTestData(self,Xin,yin,verb=True):
		txsize = Xin.shape
		tysize = yin.shape
		if txsize[1] != self.s[0]:
			print('Xin needs to have the dimensions (m,s1), where m is the number of training samples and s1 is equal to the number of units in the input layer of the network')
			return
		self.mtest = txsize[0]
		if (tysize[0] != self.mtest):
			print('yin must have the dimensions (m,), where m is the number of training samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs')
			return
		self.Xtest = np.zeros((self.mtest,self.s[0]),dtype='float64')
		self.Xtest[:] = np.array(Xin)
		self.ytest0 = np.array(yin)

		if np.size(tysize) == 1:
			self.ytest = self._GetOneHotClassLabels(self.ytest0)
		else:
			self.ytest = self.ytest0

		self._ztest,self._atest = self._GetPropagationArrays(self.Xtest)
		
		self.TestData = True

		
	def InputCrossValidationData(self,Xin,yin,verb=True):
		txsize = Xin.shape
		tysize = yin.shape
		if txsize[1] != self.s[0]:
			print('Xin needs to have the dimensions (m,s1), where m is the number of CV samples and s1 is equal to the number of units in the input layer of the network')
			return
		self.mc = txsize[0]
		if (tysize[0] != self.mc):
			print('yin must have the dimensions (m,), where m is the number of CV samples, and the value stored in yin should represent the output unit index')
			return
		self.Xc = np.zeros((self.mc,self.s[0]),dtype='float64')
		self.Xc[:] = np.array(Xin)
		self.yc0 = np.array(yin)		
		
		if np.size(tysize) == 1:
			self.yc = self._GetOneHotClassLabels(self.yc0)
		else:
			self.yc = self.yc0
		
		self._zc,self._ac = self._GetPropagationArrays(self.Xc)
		
		self.CData = True

	
	def _GetPropagationArrays(self,x):
		a = []
		z = []
		a.append(x)
		m = x.shape[0]
		for i in range(0,self.L-1):
			zt = np.zeros((m,self.s[i+1]),dtype='float64')
			z.append(zt)
			a.append(zt)
		return z,a
	
	def _ForwardPropagate(self,z,a,ThetaW=None,ThetaB=None):
		if ThetaW is None:
			ThetaW = self.ThetaW
		if ThetaB is None:
			ThetaB = self.ThetaB
			 
		for i in range(0,self.L-1):
			z[i] = np.dot(a[i],ThetaW[i]) + ThetaB[i]
			a[i+1] = self.AF[i](z[i])
	
	
	def _L1Reg(self,L1,m):
		Reg = 0.0
		for i in range(0,self.L-1):
			T = self.ThetaW[i]
			Reg += L1/(2.0*m) * np.sum(np.abs(T))		
		return Reg
	
	def _L2Reg(self,L2,m):
		Reg = 0.0
		for i in range(0,self.L-1):
			T = self.ThetaW[i]
			Reg += L2/(2.0*m) * np.sum(T**2.0)	
		return Reg
	
	
	def _L1RegGrad(self,L1,i,m):
		T = self.ThetaW[i]
		mask = ((T >= 0.0)*1.0) + ((T < 0.0)*-1.0) # this is d|w|/dw			
		Reg = L1/(2.0*m) * mask			
		return Reg
	
	def _L2RegGrad(self,L2,i,m):
		T = self.ThetaW[i]
		Reg = L2/(m) * T	
		return Reg
			
	def _CostFunction(self,a,y,L1=None,L2=None):

		J = 0.0
		h = a[-1]
		m = a[0].shape[0]

		if self.s[-1] > 1:
			for k in range(0,self.s[-1]):
				#select the training 
				yk = np.float32(y == k+1)
				hk = h[:,k]
				J +=  (1.0/m)*np.sum(-yk*np.log(hk.clip(min=1e-40)) - (1.0 - yk)*np.log((1.0 - hk).clip(min=1e-40)))		
		else:
			yk = np.float32(y - 1)
			hk = h[:,0]
			J +=  (1.0/m)*np.sum(-yk*np.log(hk.clip(min=1e-40)) - (1.0 - yk)*np.log((1.0 - hk).clip(min=1e-40)))		


		if L1 is None:
			L1 = self.L1
		
		if L2 is None:
			L2 = self.L2

		#Regularization
		L1Reg = self._L1Reg(L1,m)
		L2Reg = self._L2Reg(L2,m)

		J += L1Reg + L2Reg
	
		return J
	
	def _BackPropagate(self,a,y,m,n,L1=None,L2=None):
		if L1 is None:
			L1 = self.L1
		
		if L2 is None:
			L2 = self.L2
		

		ThetaWGrad = []
		ThetaBGrad = []
		
		for i in range(0,self.L-1):
			ThetaWGrad.append(np.zeros(self.ThetaW[i].shape))
			ThetaBGrad.append(np.zeros(self.ThetaB[i].shape))

		
		#Calculate for final layer first
#		dl = np.zeros((m,self.s[-1]),dtype='float64')
#		if self.s[-1] > 1:
#			for k in range(0,self.s[-1]):
#				yk = np.float32(y == k+1)
#				dl[:,k] = a[-1][:,k] - yk
#		else:
#			yk = np.float32(y-1)
#			#dl[:,0] = a[-1][:,0] - yk
		dl = self.CFDelta(a[-1],y,self.AFgrad[-1])
		
		for i in range(self.L-2,-1,-1):
			ThetaBGrad[i][:] = np.dot(np.ones((1,m)),dl)/m
			ThetaWGrad[i][:] = np.dot(a[i].T,dl)/m + self._L1RegGrad(self.L1,i,n) + self._L2RegGrad(self.L2,i,n)#+ (L2/n)*self.ThetaW[i] + (L1/n)*np.sign(self.ThetaW[i])
			
			#dl = np.dot(dl,self.ThetaW[i].T)*a[i]*(1-a[i])	
			dl = np.dot(dl,self.ThetaW[i].T)*self.AFgrad[i](a[i])	
		
		return ThetaWGrad,ThetaBGrad
				
	def _CalculateStep(self,X,y,Alpha,m,n):
		
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)
		
		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)

		#back propagate errors in order to get weight and bias gradients
		WGrad,BGrad = self._BackPropagate(a,y,m,n)
		
		if not self.Momentum is None:
			if self.VW is None:
				self.VW = []
				self.VB = []
				for i in range(0,self.L-1):
					self.VW.append(Alpha*WGrad[i])
					self.VB.append(Alpha*BGrad[i])
			else:
				for i in range(0,self.L-1):
					self.VW[i] = self.Momentum*self.VW[i] + Alpha*WGrad[i]
					self.VB[i] = self.Momentum*self.VB[i] + Alpha*BGrad[i]
		else:
			if self.VW is None:
				self.VW = []
				self.VB = []
				for i in range(0,self.L-1):
					self.VW.append(Alpha*WGrad[i])
					self.VB.append(Alpha*BGrad[i])
			else:
				for i in range(0,self.L-1):
					self.VW[i] = Alpha*WGrad[i]
					self.VB[i] = Alpha*BGrad[i]		
		#update weights and gradients
		for i in range(0,self.L-1):
			if self.TrainLayers[i]:
				self.ThetaW[i] = self.ThetaW[i] - self.VW[i]
				self.ThetaB[i] = self.ThetaB[i] - self.VB[i]
				
				
	def _ParallelCalculateStep(self,X,y,Alpha,m,n,ThetaW0,ThetaB0,ThetaW,ThetaB):			
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)
		
		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)
		
		#back propagate errors in order to get weight and bias gradients
		WGrad,BGrad = self._BackPropagate(a,y,m,n)

		#update weights and gradients for each alpha
		for a in range(0,3):
			for i in range(0,self.L-1):
				if self.TrainLayers[i]:
					ThetaW[a][i] = ThetaW0[i] - Alpha[a]*WGrad[i]
					ThetaB[a][i] = ThetaB0[i] - Alpha[a]*BGrad[i]	
						
	def Predict(self,X):
		txsize = X.shape
		if txsize[1] != self.s[0]:
			print('X needs to have the dimensions (m,s1), where m is the number of samples and s1 is equal to the number of units in the input layer of the network')
			return
					
		z,a = self._GetPropagationArrays(X)
		self._ForwardPropagate(z,a)
		return a[-1]					
						
	def Classify(self,X):
		txsize = X.shape
		if txsize[1] != self.s[0]:
			print('X needs to have the dimensions (m,s1), where m is the number of samples and s1 is equal to the number of units in the input layer of the network')
			return
					
		z,a = self._GetPropagationArrays(X)
		self._ForwardPropagate(z,a)
		if self.s[-1] > 1:
			Class = np.argmax(a[-1],1)+1
			Prob = Softmax(z[-1])
	
		else:
			Class = np.int32(np.round(a[-1][:,0])) +1
			Prob = a[-1][:,0]
		return Class,Prob
		
	def GetAccuracy(self,X,y):
		
		Class,Prob = self.Classify(X)
		good = Class == y
		return 100.0*np.sum(good)/good.size #percentage
		
	def _CheckCostGradient(self,nSteps,J,gTol,gTolEpochs,gTolMinEpochs):
		
		if nSteps < gTolMinEpochs or nSteps < gTolEpochs:
			return False
			
		J0 = J[nSteps - gTolEpochs]
		J1 = J[nSteps - 1]
		
		grad = (J0 - J1)/gTolEpochs
		
		if grad < gTol:
			return True
		

	def ParallelTrainNetwork(self,nEpoch=100,MiniBatchSize=10,Alpha=1.0,gTol=0.0,gTolEpochs=10,gTolMinEpochs=10,AlphaTestEpochs=1,AlphaRange=[1e-5,10.0]):

		#set up full Alpha array
		alpha = Alpha*np.array([0.1,1.0,10.0],dtype='float64')
		Alphas = np.zeros((nEpoch,3),dtype='float32')
		

		#check for data
		if self.TData is False:
			print('Please insert training data before trining!')
			return
		
		
		#calculate number of mini batches
		n = self.mt
		if MiniBatchSize is None:
			nb = 1
			MiniBatchSize = n
		else:
			nb = np.int32(np.ceil(n/MiniBatchSize))
		#create arrays to store costs for final output
		Jt = np.zeros(nEpoch,dtype='float32')
		Jc = np.zeros(nEpoch,dtype='float32')
		At = np.zeros(nEpoch,dtype='float32')
		Ac = np.zeros(nEpoch,dtype='float32')	
		#and for temporary use (different Alpha)
		tmpJt = np.zeros((nEpoch,3),dtype='float32')
		tmpJc = np.zeros((nEpoch,3),dtype='float32')
		tmpAt = np.zeros((nEpoch,3),dtype='float32')
		tmpAc = np.zeros((nEpoch,3),dtype='float32')	
		
		#create temporary propagation arrays
		_at = copy.deepcopy(self._at)
		_zt = copy.deepcopy(self._zt)
		
		#create weight arrays
		tmpTW = []
		tmpTB = []
		for i in range(0,3):
			tmpTW.append(copy.deepcopy(self.ThetaW))
			tmpTB.append(copy.deepcopy(self.ThetaB))
		
			
		#Get initial cost if there have been no steps
		if self.nSteps == 0:
			self._ForwardPropagate(self._zt,self._at)
			self.Jt[0] = self.CF(self._at[-1],self.yt,self.ThetaW,0.0,0.0)
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)	
				self.Jc[0] = self.CF(self._ac[-1],self.yc,self.ThetaW,0.0,0.0)
			else:
				self.Jc[0] = np.nan
			self.nSteps = 1
		
		nSteps = 0
		StoppedLearning = False
		#loop through each epoch
		for i in range(0,nEpoch):
			

			#take a step for each mini batch
			for j in range(0,nb):
				X = self.Xt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				y = self.yt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				m = y.size
				self._ParallelCalculateStep(X,y,alpha,m,n,self.ThetaW,self.ThetaB,tmpTW,tmpTB)
			
			for a in range(0,3):	
				#once each batch has done, get cost functions
				self._ForwardPropagate(_zt,_at,tmpTW[a],tmpTB[a])
				tmpJt[i,a] = self.CF(_at[-1],self.yt,self.ThetaW,0.0)
			
			#pick best cost
			Jt[i] = np.nanmin(tmpJt[i,:])
			ind = np.where(tmpJt[i] == Jt[i])[0][0]
			
			#copy best Theta to self.Theta
			self.ThetaW = copy.deepcopy(tmpTW[ind])
			self.ThetaB = copy.deepcopy(tmpTB[ind])
			
			#change Alpha accordingly
			if i > AlphaTestEpochs:
				diff = tmpJt[i-AlphaTestEpochs] - tmpJt[i]
				best = np.where(diff == np.nanmax(diff))[0][0]
#				print()
#				print(alpha)
#				print(diff,best)
				
				if best == 0 and alpha[0]/3 >= AlphaRange[0]:
					alpha = alpha/3.0
#					print('down')
				elif best == 2 and alpha[2]*3 <= AlphaRange[1]:
					alpha = alpha*3.0
#					print('up')
					
			self._ForwardPropagate(self._zt,self._at)
			At[i] = self.GetTrainingSetAccuracy()
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)
				Jc[i] = self.CF(self._ac[-1],self.yc,self.ThetaW,0.0)
				Ac[i] = self.GetCVSetAccuracy()
			else:
				Jc[i] = np.nan
				Ac[i] = np.nan

			outstr = '\rEpoch {:5d}, Alpha: ~{:10.7f}, Training: Cost {:6.4f}, Acc. {:6.2f}'.format(i + self.nSteps,alpha[1],Jt[i],At[i])
			if self.CData:
				outstr += ', CV: Cost {:6.4f}, Acc. {:6.2f}'.format(Jc[i],Ac[i])		
			print(outstr,end='')
			nSteps += 1
			
			if self.CData:
				StoppedLearning = self._CheckCostGradient(nSteps,Jc,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
			else:
				StoppedLearning = self._CheckCostGradient(nSteps,Jt,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
			if StoppedLearning:
				break
			
		print()
		if StoppedLearning:
			print('Cross-validation score has stopped improving')
		else:
			print('Reached max epoch')
		#add the costs and accuracies to the 
		self.nSteps += nSteps
		self.Jt = np.append(self.Jt,Jt[:nSteps])
		self.Jc = np.append(self.Jc,Jc[:nSteps])
		self.At = np.append(self.At,At[:nSteps])
		self.Ac = np.append(self.Ac,Ac[:nSteps])
		return tmpJt

	def _CalculateStepGD(self,X,y,Alpha,m,n):
		
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)
		
		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)

		#back propagate errors in order to get weight and bias gradients
		WGrad,BGrad = self._BackPropagate(a,y,m,n)
		
		
		#first of all, check if previous velocities exist:
		if self.VW is None:
			#if not then this step will create them
			self.VW = []
			self.VB = []
			for i in range(0,self.L-1):
				self.VW.append(-Alpha*WGrad[i])
				self.VB.append(-Alpha*BGrad[i])		
		else:
			#at this point previous velocities must exist
			#now to check if we are using momentum or
			#adaptive learning rate gains
			
			for i in range(0,self.L-1):
				self.tmpDW[i] = -Alpha*WGrad[i]
				self.tmpDB[i] = -Alpha*BGrad[i]
				
			if self.LocalGain:
				
				
				for i in range(0,self.L-1):
					#determine if current gradients have the same sign
					#as previous ones (+1) or opposite (-1)
					sgnW = np.sign(self.VW[i]*self.tmpDW[i])
					sgnB = np.sign(self.VB[i]*self.tmpDB[i])
					
					gt0W = (sgnW > 0).astype('float64')
					gt0B = (sgnB > 0).astype('float64')
					lt0W = (sgnW <= 0).astype('float64')
					lt0B = (sgnB <= 0).astype('float64')
					
					#Add small amout to gains which match
					self.GainW[i] = (self.GainW[i] + gt0W*self.GainSteps[1]).clip(max=self.GainLimits[1])
					self.GainB[i] = (self.GainB[i] + gt0B*self.GainSteps[1]).clip(max=self.GainLimits[1])

					#Reduce by small amount for gains which are unmatched
					self.GainW[i] = (self.GainW[i]*lt0W*self.GainSteps[0]).clip(min=self.GainLimits[0])
					self.GainB[i] = (self.GainB[i]*lt0B*self.GainSteps[0]).clip(min=self.GainLimits[0])
					
					
					self.tmpDW[i] = self.tmpDW[i]*self.GainW[i]
					self.tmpDB[i] = self.tmpDB[i]*self.GainB[i]		

			if self.Momentum > 0.0:
				for i in range(0,self.L-1):
					self.tmpDW[i] = self.Momentum*self.VW[i] + self.tmpDW[i]
					self.tmpDB[i] = self.Momentum*self.VB[i] + self.tmpDB[i]
					
			self.VW = copy.deepcopy(self.tmpDW)
			self.VB = copy.deepcopy(self.tmpDB)
		
		#update weights and gradients
		for i in range(0,self.L-1):
			if self.TrainLayers[i]:
				self.ThetaW[i] = self.ThetaW[i] + self.VW[i]
				self.ThetaB[i] = self.ThetaB[i] + self.VB[i]


	def _CalculateStepNesterov(self,X,y,Alpha,m,n):
		
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)
		
	
		if self.VW is None:
			#need to create an initial step
			self._ForwardPropagate(z,a)
			WGrad,BGrad = self._BackPropagate(a,y,m,n)
			self.VW = []
			self.VB = []
			for i in range(0,self.L-1):
				self.VW.append(-Alpha*WGrad[i])
				self.VB.append(-Alpha*BGrad[i])
		else:
			#move temporarily in direction of previous step
			tmpW = copy.deepcopy(self.ThetaW)
			tmpB = copy.deepcopy(self.ThetaB)
			for i in range(0,self.L-1):
				tmpW[i] = tmpW[i] + Alpha*self.Momentum*self.VW[i]
				tmpB[i] = tmpB[i] + Alpha*self.Momentum*self.VB[i]
			
			#propagate using new weights
			self._ForwardPropagate(z,a,tmpW,tmpB)
			
			#calculate next set of gradients
			WGrad,BGrad = self._BackPropagate(a,y,m,n)


			for i in range(0,self.L-1):
				self.tmpDW[i] = -Alpha*WGrad[i]
				self.tmpDB[i] = -Alpha*BGrad[i]
				
			if self.LocalGain:
				for i in range(0,self.L-1):
					#determine if current gradients have the same sign
					#as previous ones (+1) or opposite (-1)
					sgnW = np.sign(self.VW[i]*self.tmpDW[i])
					sgnB = np.sign(self.VB[i]*self.tmpDB[i])

					gt0W = np.where(sgnW > 0)
					gt0B = np.where(sgnB > 0)
					lt0W = np.where(sgnW <= 0)
					lt0B = np.where(sgnB <= 0)
						
					#Add small amout to gains which match
					self.GainW[i][gt0W] = (self.GainW[i][gt0W] + self.GainSteps[1]).clip(max=self.GainLimits[1])
					self.GainB[i][gt0B] = (self.GainB[i][gt0B] + self.GainSteps[1]).clip(max=self.GainLimits[1])

					#Reduce by small amount for gains which are unmatched
					self.GainW[i][lt0W] = (self.GainW[i][lt0W]*self.GainSteps[0]).clip(min=self.GainLimits[0])
					self.GainB[i][lt0B] = (self.GainB[i][lt0B]*self.GainSteps[0]).clip(min=self.GainLimits[0])
					
					self.tmpDW[i] = self.tmpDW[i]*self.GainW[i]
					self.tmpDB[i] = self.tmpDB[i]*self.GainB[i]	

			
			#add next velocity to previous velocity
			for i in range(0,self.L-1):
				self.VW[i] = self.Momentum*self.VW[i] + self.tmpDW[i]
				self.VB[i] = self.Momentum*self.VB[i] + self.tmpDB[i]	
					
		#update weights and gradients
		for i in range(0,self.L-1):
			if self.TrainLayers[i]:
				self.ThetaW[i] = self.ThetaW[i] + self.VW[i]
				self.ThetaB[i] = self.ThetaB[i] + self.VB[i]

	def _CalculateStepRProp(self,X,y,Alpha,m,n):
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)		


		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)

		#back propagate errors in order to get weight and bias gradients
		WGrad,BGrad = self._BackPropagate(a,y,m,n)
		
		
		#first of all, check if previous velocities exist:
		if self.VW is None:
			#if not then this step will create them
			self.VW = []
			self.VB = []
			for i in range(0,self.L-1):
				self.VW.append(-self.GainW[i]*np.sign(WGrad[i]))
				self.VB.append(-self.GainB[i]*np.sign(BGrad[i]))		

		else:
			#at this point previous velocities must exist
			#now to check if we are using momentum or
			#adaptive learning rate gains
			
			for i in range(0,self.L-1):
				self.tmpDW[i] = -np.sign(WGrad[i])
				self.tmpDB[i] = -np.sign(BGrad[i])
				
			for i in range(0,self.L-1):
				#determine if current gradients have the same sign
				#as previous ones (+1) or opposite (-1)
				sgnW = np.sign(self.VW[i]*self.tmpDW[i])
				sgnB = np.sign(self.VB[i]*self.tmpDB[i])
					
				gt0W = np.where(sgnW > 0)
				gt0B = np.where(sgnB > 0)
				lt0W = np.where(sgnW <= 0)
				lt0B = np.where(sgnB <= 0)
					
				#advance the ones which have the same sign 
				#Add small amout to gains which match
				self.GainW[i][gt0W] = (self.GainW[i][gt0W]*self.GainSteps[1]).clip(max=self.GainLimits[1])
				self.GainB[i][gt0B] = (self.GainB[i][gt0B]*self.GainSteps[1]).clip(max=self.GainLimits[1])

				self.VW[i][gt0W] = self.GainW[i][gt0W]*self.tmpDW[i][gt0W]
				self.VB[i][gt0B] = self.GainB[i][gt0B]*self.tmpDB[i][gt0B]

				#revert bad ones to previous weight
				self.ThetaW[i][lt0W] -= self.VW[i][lt0W]
				self.ThetaB[i][lt0B] -= self.VB[i][lt0B]

				#Reduce by small amount for gains which are unmatched
				self.GainW[i][lt0W] = (self.GainW[i][lt0W]*self.GainSteps[0]).clip(min=self.GainLimits[0])
				self.GainB[i][lt0B] = (self.GainB[i][lt0B]*self.GainSteps[0]).clip(min=self.GainLimits[0])

				self.VW[i][lt0W] = self.GainW[i][lt0W]*self.tmpDW[i][lt0W]
				self.VB[i][lt0B] = self.GainB[i][lt0B]*self.tmpDB[i][lt0B]					

		#update weights and gradients
		for i in range(0,self.L-1):
			if self.TrainLayers[i]:
				self.ThetaW[i] = self.ThetaW[i] + self.VW[i]
				self.ThetaB[i] = self.ThetaB[i] + self.VB[i]




	def _CalculateStepRMSProp(self,X,y,Alpha,m,n):
		
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)

		#Nesterov Momentum (I think)
		if self.Momentum > 0.0 and not self.VW is None:
			for i in range(0,self.L-1):
				if self.TrainLayers[i]:
					self.ThetaW[i] = self.ThetaW[i] + self.Momentum*self.VW[i]
					self.ThetaB[i] = self.ThetaB[i] + self.Momentum*self.VB[i]


		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)

		#back propagate errors in order to get weight and bias gradients
		WGrad,BGrad = self._BackPropagate(a,y,m,n)
		
		#calculate MeanSquare
		for i in range(0,self.L-1):
			self.MeanSqW[i] = self.Decay*self.MeanSqW[i] + (1.0-self.Decay)*WGrad[i]**2
			self.MeanSqB[i] = self.Decay*self.MeanSqB[i] + (1.0-self.Decay)*BGrad[i]**2
		
		dW = copy.deepcopy(WGrad)
		dB = copy.deepcopy(BGrad)
			
		#calculate initial step
		for i in range(0,self.L-1):
			dW[i] = -(dW[i]*Alpha)/(np.sqrt(self.MeanSqW[i]) + 1e-8)
			dB[i] = -(dB[i]*Alpha)/(np.sqrt(self.MeanSqB[i]) + 1e-8)
		
		#first of all, check if previous velocities exist:
		if self.VW is None:
			#if not then this step will create them
			self.VW = []
			self.VB = []
			for i in range(0,self.L-1):
				self.VW.append(self.GainW[i]*dW[i])
				self.VB.append(self.GainB[i]*dB[i])		
		else:
			#at this point previous velocities must exist
			#now to check if we are using momentum or
			#adaptive learning rate gains
			
			for i in range(0,self.L-1):
				self.tmpDW[i] = dW[i]
				self.tmpDB[i] = dB[i]
				
			for i in range(0,self.L-1):
				#determine if current gradients have the same sign
				#as previous ones (+1) or opposite (-1)
				sgnW = np.sign(self.VW[i]*self.tmpDW[i])
				sgnB = np.sign(self.VB[i]*self.tmpDB[i])
				
				#print()
				#print(sgnB)
					
				gt0W = (sgnW > 0).astype('float64')
				gt0B = (sgnB > 0).astype('float64')

				#print(gt0B)

				#calculate multipliers for GainW and GainB
				dgW = gt0W*self.GainSteps[1] + (1.0-gt0W)*self.GainSteps[0]
				dgB = gt0B*self.GainSteps[1] + (1.0-gt0B)*self.GainSteps[0]

				#revert bad ones to previous weight
				#self.ThetaW[i] -= self.VW[i]*(1.0-gt0W)
				#self.ThetaB[i] -= self.VB[i]*(1.0-gt0B)
					
				#print(dgB)
				#recalculate Gains
				self.GainW[i] = (self.GainW[i]*dgW).clip(min=self.GainLimits[0],max=self.GainLimits[1])
				self.GainB[i] = (self.GainB[i]*dgB).clip(min=self.GainLimits[0],max=self.GainLimits[1])
				
				self.tmpDW[i] = self.tmpDW[i]*self.GainW[i]
				self.tmpDB[i] = self.tmpDB[i]*self.GainB[i]		
					
			self.VW = copy.deepcopy(self.tmpDW)
			self.VB = copy.deepcopy(self.tmpDB)
		
		#update weights and gradients
		for i in range(0,self.L-1):
			if self.TrainLayers[i]:
				self.ThetaW[i] = self.ThetaW[i] + self.VW[i]
				self.ThetaB[i] = self.ThetaB[i] + self.VB[i]




	def Train(self,Method='gradient-descent',**kwargs):
		

				
		Methods = {	'gradient-descent':(self._CalculateStepGD,set_GD), #this one can do all simple batch,minibatch,stochastic GD
					'nesterov':(self._CalculateStepNesterov,set_Nesterov), #this will use the Nesterov momentum method - minibatches and SGD are enabled, but batch probably prefered
					'rprop':(self._CalculateStepRProp,set_RProp), #batch training using RProp method
					'rmsprop':(self._CalculateStepRMSProp,set_RMSProp)} #Stochastic/minibatch version of RProp
		
		
		
		StepFunc,settings = Methods[Method]
		keys = list(kwargs.keys())
		skeys = list(settings.keys())
		
		for k in keys:
			settings[k] = kwargs[k]

		self._TrainNetwork(StepFunc,**settings)
		
	def _TrainNetwork(self,CalculateStep,**kwargs):
		nEpoch = kwargs['nEpoch']
		MiniBatchSize = kwargs['MiniBatchSize']
		Alpha = kwargs['Alpha']
		gTol = kwargs['gTol']
		gTolEpochs = kwargs['gTolEpochs']
		gTolMinEpochs = kwargs['gTolMinEpochs']
		EarlyStop = kwargs['EarlyStop']
		self.Momentum = kwargs['Momentum']
		self.LocalGain = kwargs['LocalGain']
		self.GainLimits = kwargs['GainLimits']
		self.GainSteps = kwargs['GainSteps']
		self.Decay = kwargs['Decay']
		self.MeanSqW = []
		self.MeanSqB = []
		
		if 'quiet' in list(kwargs.keys()):
			quiet = kwargs['quiet']
		else:
			quiet = False
		for i in range(0,self.L-1):
			self.MeanSqW.append(np.ones(self.ThetaW[i].shape))
			self.MeanSqB.append(np.ones(self.ThetaB[i].shape))
			
		#set up initial gains of 1.0
		self.GainW = []
		self.GainB = []
		for i in range(0,self.L-1):
			self.GainW.append(np.ones(self.ThetaW[i].shape))
			self.GainB.append(np.ones(self.ThetaB[i].shape))
		
		#this lot is to store previous steps (velocity)
		self.VW = None
		self.VB = None
		
		#create temporary arrays for storing gradients so we don't have to reallocate during each step
		self.tmpDW = copy.deepcopy(self.ThetaW)
		self.tmpDB = copy.deepcopy(self.ThetaB)
	
		#calculate number of mini batches
		n = self.mt
		if MiniBatchSize is None:
			nb = 1
			MiniBatchSize = n
		else:
			nb = np.int32(np.ceil(n/MiniBatchSize))
		#create arrays to store costs
		Jt = np.zeros(nEpoch,dtype='float32')
		JtClass = np.zeros(nEpoch,dtype='float32')
		Jc = np.zeros(nEpoch,dtype='float32')
		Jtest = np.zeros(nEpoch,dtype='float32')
		At = np.zeros(nEpoch,dtype='float32')
		Ac = np.zeros(nEpoch,dtype='float32')	
		Atest = np.zeros(nEpoch,dtype='float32')	
			
		#Get initial cost if there have been no steps
		if self.nSteps == 0:
			self._ForwardPropagate(self._zt,self._at)
			self.Jt[0] = self.CF(self._at[-1],self.yt,self.ThetaW,self.L1,self.L2)
			self.JtClass[0] = self.CF(self._at[-1],self.yt,self.ThetaW,0.0,0.0)
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)	
				self.Jc[0] = self.CF(self._ac[-1],self.yc,self.ThetaW,0.0,0.0)
			else:
				self.Jc[0] = np.nan
			if self.TestData:
				self._ForwardPropagate(self._ztest,self._atest)	
				self.Jtest[0] = self.CF(self._atest[-1],self.ytest,self.ThetaW,0.0,0.0)
			else:
				self.Jtest[0] = np.nan
			self.nSteps = 1
			
			#save best Theta is CData exists and the kwarg 'StoreBest' is True
			if self.CData and kwargs.get('StoreBest',False):
				self.BestCVScore = 0.0#initial value
				self.BestThetaW = copy.deepcopy(self.ThetaW)
				self.BestThetaB = copy.deepcopy(self.ThetaB)
			
		outstr = ''
		nSteps = 0
		StoppedLearning = False
		
		BatchStr = ColorString('Batches:','bright green')
		EpochStr = ColorString('Epochs:','bright green')
		HeadStr = ColorString('Total Epochs','bright green') + ColorString(' {:5d}   ','yellow') + ColorString('Training: Cost ','bright red') \
					+ ColorString('{:6.4f} ({:6.4f})','yellow') + ColorString(', Acc. ','bright red') + ColorString('{:6.2f}%','yellow')
		if self.CData:
			HeadStr += ColorString(' CV: Cost ','bright blue') + ColorString('{:6.4f}','yellow') + ColorString(', Acc. ','bright blue') + ColorString('{:6.2f}%','yellow')
		if not quiet:
			mpb = MultiProgressBar(nb,nEpoch,BatchStr,EpochStr,CharDone=ColorString('=','bright magenta'),CharTodo=ColorString('-','blue'),PercColor='cyan',FracColor='yellow')
		
		#print('\n\n\n')
		
		#loop through each epoch
		for i in range(0,nEpoch):
			
			#take a step for each mini batch
			for j in range(0,nb):
				
				X = self.Xt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				y = self.yt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				m = y.shape[0]
				#ProgressBar2(j+1,nb,i+1,nEpoch,'Batch:','Epoch:',HeadStr=outstr,Final=False)
				if not quiet:
					mpb.UpdateBars(j+1,i+1,outstr)
				CalculateStep(X,y,Alpha,m,n)
			
			#once each batch has done, get cost functions
			self._ForwardPropagate(self._zt,self._at)
			Jt[i] = self.CF(self._at[-1],self.yt,self.ThetaW,self.L1,self.L2) #regularized cost function
			JtClass[i] = self.CF(self._at[-1],self.yt,self.ThetaW,0.0,0.0) #classification cost function (no regularization)
			At[i] = self.GetTrainingSetAccuracy()
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)
				Jc[i] = self.CF(self._ac[-1],self.yc,self.ThetaW,0.0,0.0) # use classification cost function here
				Ac[i] = self.GetCVSetAccuracy()
			else:
				Jc[i] = np.nan
				Ac[i] = np.nan
			if self.TestData:
				self._ForwardPropagate(self._ztest,self._atest)
				Jtest[i] = self.CF(self._atest[-1],self.ytest,self.ThetaW,0.0,0.0) #use classification cost function
				Atest[i] = self.GetTestSetAccuracy()
			else:
				Jtest[i] = np.nan
				Atest[i] = np.nan

			#outstr = 'Epoch {:5d}, Training: Cost {:6.4f}, Acc. {:6.2f}'.format(i + self.nSteps,Jt[i],At[i])
			
			if self.CData:
				outstr = HeadStr.format(i + self.nSteps,Jt[i],JtClass[i],At[i],Jc[i],Ac[i])
			else:
				outstr = HeadStr.format(i + self.nSteps,Jt[i],JtClass[i],At[i])
				#outstr += ', CV: Cost {:6.4f}, Acc. {:6.2f}'.format(Jc[i],Ac[i])			
			#ProgressBar2(j+1,nb,i+1,nEpoch,'Batch:','Epoch:',HeadStr=outstr,Final=False)
			if not quiet:
				mpb.UpdateBars(nb,i+1,outstr)
			#print(outstr,end='')
			nSteps += 1

			if self.CData and kwargs.get('StoreBest',False):
				if Ac[i] > self.BestCVScore:
					self.BestCVScore = Ac[i]
					self.BestThetaW = copy.deepcopy(self.ThetaW)
					self.BestThetaB = copy.deepcopy(self.ThetaB)
			
			if EarlyStop:
				if self.CData:
					StoppedLearning = self._CheckCostGradient(nSteps,Jc,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
				else:
					StoppedLearning = self._CheckCostGradient(nSteps,Jt,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
				if StoppedLearning:
					break
			
		if not quiet:
			if StoppedLearning:
				print('Cross-validation score has stopped improving')
			else:
				print('Reached max epoch')

		#add the costs and accuracies to the 
		self.nSteps += nSteps
		self.Jt = np.append(self.Jt,Jt[:nSteps])
		self.JtClass = np.append(self.JtClass,JtClass[:nSteps])
		self.Jc = np.append(self.Jc,Jc[:nSteps])
		self.Jtest = np.append(self.Jtest,Jtest[:nSteps])
		self.At = np.append(self.At,At[:nSteps])
		self.Ac = np.append(self.Ac,Ac[:nSteps])		
		self.Atest = np.append(self.Atest,Atest[:nSteps])		
		if self.TestData:		
			print("Final Test Score: {:6.2f}%".format(self.Atest[-1]))



	def TrainNetwork(self,nEpoch=100,MiniBatchSize=10,Alpha=1.0,gTol=0.0,gTolEpochs=10,gTolMinEpochs=10,Momentum=None):
		self.Momentum = Momentum
		self.VW = None
		self.VB = None
		
		if self.TData is False:
			print('Please insert training data before trining!')
			return
		
		
		#calculate number of mini batches
		n = self.mt
		if MiniBatchSize is None:
			nb = 1
			MiniBatchSize = n
		else:
			nb = np.int32(np.ceil(n/MiniBatchSize))
		#create arrays to store costs
		Jt = np.zeros(nEpoch,dtype='float32')
		Jc = np.zeros(nEpoch,dtype='float32')
		At = np.zeros(nEpoch,dtype='float32')
		Ac = np.zeros(nEpoch,dtype='float32')	
			
		#Get initial cost if there have been no steps
		if self.nSteps == 0:
			self._ForwardPropagate(self._zt,self._at)
			self.Jt[0] = self.CF(self._at[-1],self.yt,self.ThetaW,self.Lambda)
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)	
				self.Jc[0] = self.CF(self._ac[-1],self.yc,self.ThetaW,self.Lambda)
			else:
				self.Jc[0] = np.nan
			self.nSteps = 1
		
		nSteps = 0
		StoppedLearning = False
		#loop through each epoch
		for i in range(0,nEpoch):
			
			#take a step for each mini batch
			for j in range(0,nb):
				X = self.Xt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				y = self.yt[j*MiniBatchSize:(j+1)*MiniBatchSize]
				m = y.shape[0]
				self._CalculateStep(X,y,Alpha,m,n)
			
			#once each batch has done, get cost functions
			self._ForwardPropagate(self._zt,self._at)
			Jt[i] = self.CF(self._at[-1],self.yt,self.ThetaW,self.Lambda)
			At[i] = self.GetTrainingSetAccuracy()
			if self.CData:
				self._ForwardPropagate(self._zc,self._ac)
				Jc[i] = self.CF(self._ac[-1],self.yc,self.ThetaW,self.Lambda)
				Ac[i] = self.GetCVSetAccuracy()
			else:
				Jc[i] = np.nan
				Ac[i] = np.nan

			outstr = '\rEpoch {:5d}, Training: Cost {:6.4f}, Acc. {:6.2f}'.format(i + self.nSteps,Jt[i],At[i])
			if self.CData:
				outstr += ', CV: Cost {:6.4f}, Acc. {:6.2f}'.format(Jc[i],Ac[i])			
			print(outstr,end='')
			nSteps += 1
			
			if self.CData:
				StoppedLearning = self._CheckCostGradient(nSteps,Jc,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
			else:
				StoppedLearning = self._CheckCostGradient(nSteps,Jt,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
			if StoppedLearning:
				break
			
		print()
		if StoppedLearning:
			print('Cross-validation score has stopped improving')
		else:
			print('Reached max epoch')
		#add the costs and accuracies to the 
		self.nSteps += nSteps
		self.Jt = np.append(self.Jt,Jt[:nSteps])
		self.Jc = np.append(self.Jc,Jc[:nSteps])
		self.At = np.append(self.At,At[:nSteps])
		self.Ac = np.append(self.Ac,Ac[:nSteps])
		
		
		

	def ShowTrainingSetAccuracy(self):
		acc = self.GetTrainingSetAccuracy()
		print("Training Set Accuracy: {:6.2f}%".format(acc))

	def ShowCVSetAccuracy(self):
		acc = self.GetCVSetAccuracy()
		print("Training Set Accuracy: {:6.2f}%".format(acc))
		
	
	def GetTrainingSetAccuracy(self):
		if self.CostFunction == 'cross-entropy':
			A = self.GetAccuracy(self.Xt,self.yt0)
		else:
			A = 0.0
		return A

	def GetCVSetAccuracy(self):
		if self.CostFunction == 'cross-entropy':
			A = self.GetAccuracy(self.Xc,self.yc0)
		else:
			A = 0.0
		return A
	
	def GetTestSetAccuracy(self):
		if self.CostFunction == 'cross-entropy':
			A = self.GetAccuracy(self.Xtest,self.ytest0)
		else:
			A = 0.0
		return A
	
	def _ArrayToFile(self,x,dtype,f):
		n = np.size(x)
		np.int32(n).tofile(f)
		_x = np.array(x).astype(dtype)
		ns = np.int32(np.size(_x.shape))
		sh = np.array(_x.shape).astype('int32')
		ns.tofile(f)
		sh.tofile(f)
		_x.tofile(f)
		
	def _ArrayFromFile(self,dtype,f):
		n = np.fromfile(f,dtype='int32',count=1)[0]
		ns = np.fromfile(f,dtype='int32',count=1)[0]
		sh = np.fromfile(f,dtype='int32',count=ns)
		x = np.fromfile(f,dtype=dtype,count=n).reshape(tuple(sh))
		return x
		
	def _ScalarToFile(self,x,dtype,f):
		np.array(x).astype(dtype).tofile(f)

	def _ScalarFromFile(self,dtype,f):
		x = np.fromfile(f,dtype=dtype,count=1)[0]
		return x
		
	def _StringsToFile(self,x,f):
		n = np.size(x)
		np.int32(n).tofile(f)
		_x = np.array(x).astype('U')
		if n > 1:
			l = np.int32(str(_x.dtype)[2:])
		else:
			l = np.int32(len(x))
		l.tofile(f)
		_x.tofile(f)
		
	def _StringsFromFile(self,f):
		n = np.fromfile(f,dtype='int32',count=1)[0]
		l = np.fromfile(f,dtype='int32',count=1)[0]
		x = np.fromfile(f,dtype='U{:d}'.format(l),count=n)
		if n == 1:
			return x[0]
		else:
			return x
		
	def _ListArrayToFile(self,x,dtype,f):
		l = np.int32(len(x))	
		l.tofile(f)
		for i in range(0,l):
			self._ArrayToFile(x[i],dtype,f)
			
	def _ListArrayFromFile(self,dtype,f):
		l = np.fromfile(f,dtype='int32',count=1)[0]
		x = []
		for i in range(0,l):
			x.append(self._ArrayFromFile(dtype,f))
		return x
		
	def SaveNetwork(self,FileName=''):
		if FileName == '':
			print('Please enter valid file name')
			return

	
		f = open(FileName+'.nn','wb')
		#firstly save some architecture information
		self._ScalarToFile(self.Trained,'bool8',f)
		self._ScalarToFile(self.L,'int32',f)
		self._ArrayToFile(self.s,'int32',f)
		self._ScalarToFile(self.Lambda,'float32',f)
		self._ScalarToFile(self.FT,'float32',f)
		self._StringsToFile(self.ActFuncs,f)
		self._StringsToFile(self.CostFunction,f)

		#next save training data
		self._ScalarToFile(self.TData,'bool8',f)
		self._ScalarToFile(self.mt,'bool8',f)
		self._ArrayToFile(self.Xt,'float64',f)
		self._ArrayToFile(self.yt0,'float64',f)

		#next save training data
		self._ScalarToFile(self.CData,'bool8',f)
		self._ScalarToFile(self.mc,'bool8',f)
		self._ArrayToFile(self.Xc,'float64',f)
		self._ArrayToFile(self.yc0,'float64',f)

		#next save training data
		self._ScalarToFile(self.TestData,'bool8',f)
		self._ScalarToFile(self.mtest,'bool8',f)
		self._ArrayToFile(self.Xtest,'float64',f)
		self._ArrayToFile(self.ytest0,'float64',f)	
		
		#save any training information
		self._ScalarToFile(self.nSteps,'int32',f)
		self._ArrayToFile(self.Jt,'float32',f)
		self._ArrayToFile(self.JtClass,'float32',f)
		self._ArrayToFile(self.Jc,'float32',f)
		self._ArrayToFile(self.Jtest,'float32',f)
		self._ArrayToFile(self.At,'float32',f)
		self._ArrayToFile(self.Ac,'float32',f)
		self._ArrayToFile(self.Atest,'float32',f)
		self._ArrayToFile(self.TrainLayers,'bool8',f)
		
		#save weights and biases
		self._ListArrayToFile(self.ThetaW,'float64',f)
		self._ListArrayToFile(self.ThetaB,'float64',f)
		
		#if there is a best set of weights then save those too
		if hasattr(self,'BestCVScore'):
			self._ScalarToFile(True,'bool8',f)
			self._ScalarToFile(self.BestCVScore,'float32',f)
			self._ListArrayToFile(self.BestThetaW,'float64',f)
			self._ListArrayToFile(self.BestThetaB,'float64',f)
		else:
			self._ScalarToFile(False,'bool8',f)
		f.close()
		print('Saved: '+FileName)

	def GetTrainingSetProgress(self):
		return self.Jt,self.At

	def GetCVSetProgress(self):
		return self.Jc,self.Ac

	def PlotCost(self,fig=None,maps=[1,1,0,0],xrnge=None,yrnge=None):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		ax.plot(self.JtClass[0:self.nSteps],color=[1.0,0.0,0.0],label='Training Set Cost')
		ax.plot(self.Jc[0:self.nSteps],color=[0.0,0.0,1.0],label='Cross-validation Set Cost')
		legend = ax.legend(loc='upper right')
		#ax.axis([0,self.TrainAccuracy.size,0.0,1.0])
		if xrnge is None:
			xrnge = [0,self.nSteps]
		if yrnge is None:
			yrnge = [0,np.nanmax([self.JtClass,self.Jc])]
		
		ax.axis(np.append(xrnge,yrnge))
		fig.xlabel('Epochs')
		fig.ylabel('Cost')	
		return ax

		
	def PlotAccuracy(self,fig=None,maps=[1,1,0,0],xrnge=None,yrnge=None):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		ax.plot(self.At[0:self.nSteps],color=[1.0,0.0,0.0],label='Training Set Accuracy')
		ax.plot(self.Ac[0:self.nSteps],color=[0.0,0.0,1.0],label='Cross-validation Set Accuracy')
		legend = ax.legend(loc='lower right')
		if xrnge is None:
			xrnge = [0,self.nSteps]
		if yrnge is None:
			yrnge = [0,100]
		
		ax.axis(np.append(xrnge,yrnge))
		fig.xlabel('Epochs')
		fig.ylabel('Accuracy')	
		return ax
		


	def _CalcF1(self,y,ytest,PosClass=2):
		
		pos = y == PosClass #classified as positive manually
		pos_test = ytest == PosClass #NN clasified as positive
		
		true_pos = pos & pos_test
		false_pos = (pos == False) & pos_test
		false_neg = pos & (pos_test == False)
		
		Precision = np.sum(true_pos)/(np.sum(true_pos) + np.sum(false_pos))
		Recall = np.sum(true_pos)/(np.sum(true_pos) + np.sum(false_neg))
		
		F1 = 2.0 * (Precision*Recall)/(Precision + Recall)
		if np.isnan(F1):
			F1 = 0.0
		return F1

	def GetF1Scores(self,PosClass=2):
		Ct,_ = self.Classify(self.Xt)
		Cc,_ = self.Classify(self.Xc)
		
		F1t = self._CalcF1(Ct,self.yt,PosClass)
		F1c = self._CalcF1(Cc,self.yc,PosClass)
		
		return F1t,F1c

	def ReturnTheta(self):
		return self.ThetaW,self.ThetaB
	
	def GetCosts(self):
		return self.Jt[-1],self.Jc[-1]
	
	def GetAccuracies(self):
		return self.At[-1],self.Ac[-1]	
		
	def UseBestWeights(self):
		if hasattr(self,'BestCVScore'):
			self.ThetaW = copy.deepcopy(self.BestThetaW)
			self.ThetaB = copy.deepcopy(self.BestThetaB)
		else:
			print('Best weights were not stored during training')		
		
	def PlotArchitecture(self,fig=None,maps=[1,1,0,0],ShowTheta=True):

		if fig is None:
			fig = plt
			fig.figure()
		
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		ax.axis([0,1,0,1])
		ax.set_aspect(1.0)
		
		ax.set_xticks([0.0])
		ax.set_yticks([0.0])		
		
		#must split y direction into self.L + 1 columns (one extra for output labels)
		nL = self.L + 1
		maxS = np.max(self.s)
		maxnodes = np.max([nL,maxS])
		
		
		#aiming for a border of 0.025 either side of each layer
		dx = 0.95/(nL-1)
		x = np.arange(nL)*dx + 0.025
		#need to work out neuron positions for each layer, again with 0.0 gap above and below:
		dy = 1.0/(maxnodes-0.2)

		#now to work out the circle radius:
		R = np.min([0.4*dx,0.4*dy])
		
		#create a list of arrays of neuron positions
		y = []
		for i in range(0,self.L):
			ytmp = np.arange(self.s[i])*dy
			ygap = (1-(self.s[i]-1)*dy)/2
			y.append((ytmp + ygap)[::-1])
		
		#add in the output label layer
		y.append(y[-1])

		def Circle(ax,xc,yc,r,color):
			a = np.arange(361.0)*np.pi/180.0
			xplot = r*np.sin(a) + xc
			yplot = r*np.cos(a) + yc
			ax.plot(xplot,yplot,color=color,linestyle='-',linewidth=2,zorder=3)
			ax.fill(xplot[:-1],yplot[:-1],color=[1.0,1.0,1.0],zorder=2.0)
			
		#plot circles for sigmoid nodes
		for i in range(1,self.L):
			for j in range(0,self.s[i]):
				Circle(ax,x[i],y[i][j],R,[0.0,0.0,0.0])
				if ShowTheta:
					ax.text(x[i],y[i][j],'$\Theta_{b}^{'+'({:d})'.format(i-1)+'}$='+'\n{:5.2f}'.format(self.ThetaB[i-1][0,j]),ha='center',va='center')
		
		#show inputs
		for i in range(0,self.s[0]):
			Circle(ax,x[0],y[0][i],R*0.3,[1.0,1.0,1.0])
			ax.text(x[0],y[0][i],'$x_{:d}$'.format(i),ha='center',va='center',zorder=3.0)
		
		#show outputs
		for i in range(0,self.s[-1]):
			Circle(ax,x[-1],y[-1][i],R*0.3,[1.0,1.0,1.0])
			ax.text(x[-1],y[-1][i],'$h_{:d}$'.format(i),ha='center',va='center',zorder=3.0)
			ax.plot([x[-2],x[-1]],[y[-2][i],y[-1][i]],color=[0.0,0.0,0.0],zorder=1.0)
			
		#Plot lines connecting nodes
		for i in range(0,self.L-1):
			for j in range(0,self.s[i]):
				for k in range(0,self.s[i+1]):
					ax.plot([x[i],x[i+1]],[y[i][j],y[i+1][k]],color=[0.0,0.0,0.0],zorder=1.0)
					xthet = 0.5*(x[i]+x[i+1])
					ythet = 0.5*(y[i][j]+y[i+1][k])
					ang = np.arctan2(y[i+1][k]-y[i][j],x[i+1]-x[i])*180.0/np.pi
					if ShowTheta:
						ax.text(xthet,ythet,'$\Theta_{w}^{'+'({:d})'.format(i)+'}$='+'\n{:5.2f}'.format(self.ThetaW[i][j,k]),ha='center',va='center',rotation=ang)
		
		ax.axis('off')
							
			
class NeuralNetworkArray (object):
	def __init__(self,nN,Layers,Lambda=0.0,ThetaRange=0.12):
		if isinstance(Layers,str):
			#load network
			self.nN = nN
			self.s = []
			self.net = []
			for i in range(0,nN):
				self.net.append(NeuralNetwork(Layers,Ind=i))
				self.s.append(self.net[i].s)
		else:
			lyrs = np.array(Layers)
			if (lyrs.dtype == 'O') and (np.size(lyrs.shape) == 1):
				self.s = lyrs
				self.nN = lyrs.size
			elif np.size(lyrs.shape) == 2:
				self.s = lyrs
				self.nN = lyrs.shape[0]
			elif (np.size(lyrs.shape) == 1):
				self.s = np.array(list(lyrs)*nN).reshape(nN,np.size(lyrs))
				self.nN = nN
			else:
				print('Unknown Layers format')
				return None
				
			if np.size(Lambda) == 1:
				self.Lambda = np.zeros(self.nN)+Lambda
			elif np.size(Lambda) == self.nN:
				self.Lambda = Lambda
			else:
				print('Unexpected Lambda shape')
				return None
				
			if np.size(ThetaRange) == 1:
				self.ThetaRange = np.zeros(self.nN)+ThetaRange
			elif np.size(ThetaRange) == self.nN:
				self.ThetaRange = ThetaRange
			else:
				print('Unexpected ThetaRange shape')
				return None

			self.net = []
			for i in range(0,self.nN):
				self.net.append(NeuralNetwork(self.s[i],self.Lambda[i],self.ThetaRange[i]))



	def InputTrainingData(self,ind,Xin,yin):
		self.net[ind].InputTrainingData(Xin,yin)
		
	def InputCrossValidationData(self,ind,Xin,yin):
		self.net[ind].InputCrossValidationData(Xin,yin)	
			

	
	def GradientDescentTrain(self,MaxIter=100,Alpha=1.0,HaltOnIncrease=False):
		for i in range(0,self.nN):
			print('Training network {0} of {1}'.format(i+1,self.nN))
			self.net[i].GradientDescentTrain(MaxIter,Alpha,HaltOnIncrease)
			
	def GradientDescentTrainSingle(self,ind,MaxIter=100,Alpha=1.0,HaltOnIncrease=False):
		self.net[ind].GradientDescentTrain(MaxIter,Alpha,HaltOnIncrease)

	
			
	def TrainNetwork(self,MaxIter=10000,gtol=1e-5):
		for i in range(0,self.nN):
			print('Training network {0} of {1}'.format(i+1,self.nN))
			self.net[i].TrainNetwork(MaxIter,gtol)

	def TrainNetworkSingle(self,ind,MaxIter=10000,gtol=1e-5):
		self.net[ind].TrainNetwork(MaxIter,gtol)

	
			
	def ClassifyData(self,ind,Xin):
		return self.net[ind].ClassifyData(Xin)
		

	def SaveNetwork(self,FileName=''):
		if FileName == '':
			print('Please enter valid file name')
			return
	
		for i in range(0,self.nN):
			self.net[i].SaveNetwork(FileName,i)

	def PlotCost(self,ind,fig=None,maps=[1,1,0,0]):
		
		return self.net[ind].PlotCost(fig,maps)

		
	def PlotAccuracy(self,ind,fig=None,maps=[1,1,0,0]):
		
		return self.net[ind].PlotAccuracy(fig,maps)

import numpy as np
from . import _CppInterface as cpp
from .NeuralNetwork import NeuralNetworkArray

class EvolutionaryNeuralNetwork(object):
	def __init__(self,nNetworks,nInput,nOutput,nHrange,lwrange,lambdarange,alpharange,nTop=None,nCrap=None):
		if nTop is None:
			nTop = np.int32(0.2*nNetworks)
		if nCrap is None:
			nCrap = np.int32(0.05*nNetworks)
			if nCrap < 1:
				nCrap = 1
			
		cpp._CreateEvolutionaryNetwork(nNetworks,nInput,nOutput,nTop,nCrap,nHrange,lwrange,lambdarange,alpharange)
	
	def __del__(self):
		cpp._DestroyEvolutionaryNetwork()
		
	def InputData(self,Xin,yin,FractionTrain=0.8):
		cpp._EvolutionaryNetworkInputData(Xin,yin,FractionTrain)
		
	def Evolve(self,nGens,MaxIter=1000,Pmutate=0.25,MaxMutateSize=0.1,verb=True):
		
		cpp._EvolutionaryNetworkEvolve(nGens,MaxIter,Pmutate,MaxMutateSize,verb)


class PyEvolutionaryNeuralNetwork(object):
	def __init__(self,nNetworks,nInput,nOutput,nHrange,lwrange,lambdarange,alpharange,nTop=None,nCrap=None):
		if nTop is None:
			nTop = np.int32(0.2*nNetworks)
		if nCrap is None:
			nCrap = np.int32(0.05*nNetworks)
			if nCrap < 1:
				nCrap = 1
		
		self.N = nNetworks
		self._nIn = nInput
		self._nOut = nOutput
		self._nHrange = nHrange
		self._lwrange= lwrange
		self._lambdarange = lambdarange
		self._alpharange = alpharange
		self._Ntop = nTop
		self._Ncrap = nCrap
		self._Nkeep = nTop + nCrap
		self.nGens = 0
		self._HasData = False
		self._ParamsSet = False
		self.GenAccuracy = np.zeros((self.N),dtype='float32')
		self.GenAlpha = np.zeros((self.N),dtype='float32')
		self.GenLambda = np.zeros((self.N),dtype='float32')
		self.GenL = np.zeros((self.N),dtype='int32')
		self.Gens = np.zeros((self.N),dtype='object')
		self.GenOrder = np.zeros((self.N),dtype='int32')
		self.GenKeep = np.zeros((self.N),dtype='bool')
		
		self._CreateRandomNetworkParams()
		self._InitializeNetworks()
		
	def __del__(self):
		self._KillNetworks()
		
	def _CreateRandomNetworkParams(self):
		for i in range(0,self.N):
			if self._nHrange[0] == self._nHrange[1]:
				self.GenL[i] = self._nHrange[0]+2
			else:
				self.GenL[i] = np.random.randint(self._nHrange[0],self._nHrange[1]) + 2
			
			self.Gens[i] = np.zeros(self.GenL[i],dtype='int32')
			for j in range(1,self.GenL[i]-1):
				if self._lwrange[0] == self._lwrange[1]:
					self.Gens[i][j] = self._lwrange[0]
				else:
					self.Gens[i][j] = np.random.randint(self._lwrange[0],self._lwrange[1])
			self.Gens[i][0] = self._nIn
			self.Gens[i][-1] = self._nOut
			logA = np.log10(self._alpharange)
			logL = np.log10(self._lambdarange)
			
			self.GenAlpha[i] = 10**(np.random.ranf()*(logA[1]-logA[0]) + logA[0])
			self.GenLambda[i] = 10**(np.random.ranf()*(logL[1]-logL[0]) + logL[0])
			
	
	def _InitializeNetworks(self):
		self.nets = NeuralNetworkArray(self.N,self.Gens,self.GenLambda,0.12)
		
	def _KillNetworks(self):
		del self.nets
		

	def InputData(self,Xin,yin,FractionTrain=0.8,verb=True):
		m = np.size(yin)
		self.mt = np.int32(m*FractionTrain)
		self.mcv = m - self.mt
		
		self.Xt = Xin[0:self.mt]
		self.yt = yin[0:self.mt]
		
		
		self.Xcv = Xin[self.mt:]
		self.ycv = yin[self.mt:]
		
	def _FillData(self,verb=True):
		
		for i in range(0,self.N):
			self.nets.InputTrainingData(i,self.Xt,self.yt,verb)
			self.nets.InputCrossValidationData(i,self.Xcv,self.ycv,verb)
	
	def _TrainNetworks(self,MaxIter,verb):
		
		for i in range(0,self.N):
			self.nets.GradientDescentTrainSingle(i,MaxIter,self.GenAlpha[i],verb)
			
	def _SortAccuracy(self):
		
		for i in range(0,self.N):
			J,A = self.nets.GetCVSetProgress(i)
			self.GenAccuracy[i] = A[-1]
		
		self.GenOrder = np.argsort(self.GenAccuracy)[::-1]
		self.GenKeep[:] = False
		self.GenKeep[0:self._Ntop] = True
		self.GenKeep[np.random.randint(self._Ntop,self.N-1,self._Ncrap)] = True
		
		self.Best = {'L':self.GenL[self.GenOrder[0]],
					's':self.Gens[self.GenOrder[0]],
					'Alpha':self.GenAlpha[self.GenOrder[0]],
					'Lambda':self.GenLambda[self.GenOrder[0]]}
					
		self.KeepInds = np.where(self.GenKeep)[0]
		
	def _BreedNetworks(self):
		parents = np.zeros((2,),dtype='int32')
		
		for i in range(0,self.N):
			if not self.GenKeep[i]:
				parents[0] = self.KeepInds[np.random.randint(0,self._Nkeep-1)]
				parents[1] = parents[0]
				while (parents[1] == parents[0]):
					parents[1] = self.KeepInds[np.random.randint(0,self._Nkeep-1)]
					
				nparent = [1,1]
				parentinds = np.zeros(3,dtype='int32')
				for j in range(0,3):
					ind = 0
					while (ind == 0):
						ind = np.random.randint(-nparent[1],nparent[0])
					if ind > 0:
						parentinds[j] = 1
						nparent[1] += 1
					else:
						parentinds[j] = 0
						nparent[0] += 1
				
				self.GenAlpha[i] = self.GenAlpha[parents[parentinds[0]]]	
				self.GenLambda[i] = self.GenLambda[parents[parentinds[1]]]
				self.GenL[i] = self.GenL[parents[parentinds[2]]]
						

				nparent = [1,1]
				self.Gens[i] = np.zeros(self.GenL[i],dtype='int32')
				self.Gens[i][0] = self._nIn
				self.Gens[i][-1] = self._nOut
				for j in range(1,self.GenL[i]-1):
					ind = 0
					while (ind == 0):
						ind = np.random.randint(-nparent[1],nparent[0])
					if ind > 0:
						ind = parents[1]
						nparent[1] += 1
					else:
						ind = parents[0]
						nparent[0] += 1					
					self.Gens[i][j] = self.Gens[ind][(j % (self.GenL[ind]-2)) +1]
					
	def _MutateNetworks(self,Pmutate,MaxMutateSize):
		for i in range(0,self.N):
			if (np.random.ranf() < Pmutate):
				j = np.random.randint(0,3)
				if j == 0:
					self.GenAlpha[i] += (np.random.ranf()*2-1.0)*MaxMutateSize*self.GenAlpha[i]
					if self.GenAlpha[i] > self._alpharange[1]:
						self.GenAlpha[i] = self._alpharange[1]
					if self.GenAlpha[i] < self._alpharange[0]:
						self.GenAlpha[i] = self._alpharange[0]
				elif j == 1:
					self.GenLambda[i] += (np.random.ranf()*2-1.0)*MaxMutateSize*self.GenLambda[i]
					if self.GenLambda[i] > self._lambdarange[1]:
						self.GenLambda[i] = self._lambdarange[1]
					if self.GenLambda[i] < self._lambdarange[0]:
						self.GenLambda[i] = self._lambdarange[0]
				elif j == 2:
					newL = self.GenL[i] + np.random.randint(-1,1)
					if (newL != self.GenL[i]) and ((newL >= self._nHrange[0]+2) and (newL <= self._nHrange[1]+2)):
						news = np.zeros(newL,dtype='int32')
						news[0] = self._nIn
						news[-1] = self._nOut
						for k in range(1,newL-1):
							if k >= self.GenL[i]-1:
								news[k] = self.Gens[i][self.GenL[i]-2]
							else:
								news[k] = self.Gens[i][k]
						self.Gens[i] = news
				elif j == 3:
					if (self.GenL[i] == 3):
						l = 1
					else:
						l = np.random.randint(1,self.GenL[i]-2)
					
					self.Gens[i][l] += np.int32(np.round((np.random.ranf()*2-1.0)*MaxMutateSize*self.Gens[i][l]))
				
	def _EvolveStep(self,MaxIter,Pmutate,MaxMutateSize,verb):
		print("Filling networks with data")
		self._FillData(False)
		print("Training networks")
		self._TrainNetworks(MaxIter,verb)
		print("Sorting by accuracy")
		self._SortAccuracy()
		print("Breeding networks")
		self._BreedNetworks()
		print("Mutating netowrks")
		self._MutateNetworks(Pmutate,MaxMutateSize)
		print("Killing networks")
		self._KillNetworks()
		print("Creating next generation of networks")
		self._InitializeNetworks()
		
	def Evolve(self,nGens,MaxIter=1000,Pmutate=0.25,MaxMutateSize=0.1,verb=True):
		self.nGens += nGens
		if (self.nGens == nGens):
			self.Accuracy = np.zeros(self.N*nGens,dtype='float32')
		else:
			self.Accuracy = np.append(self.Accuracy,np.zeros(self.N*nGens,dtype='float32'))
		for i in range(self.nGens-nGens,self.nGens):
			print("Evolving generation {:d} of {:d}".format(i+1,self.nGens))
			self._EvolveStep(MaxIter,Pmutate,MaxMutateSize,verb)
			self.Accuracy[self.N*i:self.N*(i+1)] = self.GenAccuracy
			print("Best accuracy: {:6.2f}".format(np.nanmax(self.GenAccuracy)))

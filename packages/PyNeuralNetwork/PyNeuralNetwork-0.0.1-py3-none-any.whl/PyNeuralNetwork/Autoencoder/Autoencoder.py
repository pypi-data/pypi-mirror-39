import numpy as np
from .. import Globals
from ..CostFunctions.MeanSquareCost import MeanSquareCost,MeanSquareDelta
from ..CostFunctions.CrossEntropyCost import CrossEntropyCost,CrossEntropyDelta
from ..Tools.MultiProgressBar import MultiProgressBar
from ColorString import ColorString
import time
import matplotlib.pyplot as plt
import os
import copy



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
			



class Autoencoder(object):
	def __init__(self,IOLayer,CodeLayer,HiddenLayer=[],ActFuncs='sigmoid',CostFunction='mean-squared',Lambda=0.0):
		#The code currently assumes symmetry around the code layer
		self.s = np.concatenate(([IOLayer],HiddenLayer,[CodeLayer],HiddenLayer,[IOLayer])).astype('int32')
		self.L = self.s.size
		
		#list activation functions and gradients
		if ActFuncs is None:
			self.AFname = np.array(['sigmoid']*(self.L-1))
		elif isinstance(ActFuncs,str):
			self.AFname = np.array([ActFuncs]*(self.L-1))
		else:
			afn = []
			for i in range(0,self.L-1):
				if i < np.size(ActFuncs):
					afn.append(ActFuncs[i])
				else:
					afn.append('sigmoid')
			self.AFname = np.array(afn)
			
		self.AF = np.zeros(self.L-1,dtype='object')
		self.AFgrad = np.zeros(self.L-1,dtype='object')
			
		for i in range(0,self.L-1):
			self.AF[i],self.AFgrad[i] = Globals.ActFuncs[self.AFname[i].lower()]

		self.CostFunction = CostFunction
			
		if CostFunction == 'mean-squared':
			self.CF = MeanSquareCost
			self.CFDelta = MeanSquareDelta
		else:
			self.CF = CrossEntropyCost
			self.CFDelta = CrossEntropyDelta
			
		#random initialization of Theta
		self.ResetWeights()
			
		#initialize cost
		self.Jt = np.array([0],dtype='float32')
			
		#initialize datasets
		self.m = 0

		self.nSteps = 0
		
		self.Lambda = Lambda
		
	def ResetWeights(self):
		self.ThetaW = []
		self.ThetaB = []
		for j in range(0,self.L-1):
			self.ThetaW.append(np.random.randn(self.s[j],self.s[j+1]).astype('float64')/np.sqrt(self.s[j]))
			self.ThetaB.append(np.random.randn(1,self.s[j+1]).astype('float64'))
			

	def InputData(self,Xin,Rescale=False):
		#Store input data
		self.Xin = Xin
		#scale so that it is all between 0 and 1
		self.Rescale = Rescale
		if Rescale:
			self.X = 1.0/(1.0+np.exp(-Xin))
		else:
			self.X = Xin
			
		self.Xin = self.Xin.astype('float64')
		self.m = self.X.shape[0]

		#create propagation arrays
		self._z,self._a = self._GetPropagationArrays(self.X)		
		
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
		
	def _ForwardPropagate(self,z,a):
		for i in range(0,self.L-1):
			z[i] = np.dot(a[i],self.ThetaW[i]) + self.ThetaB[i]
			a[i+1] = self.AF[i](z[i])
	
	
	def _BackPropagate(self,a,y,m,n,Lambda=None):
		if Lambda is None:
			Lambda = self.Lambda
		

		ThetaWGrad = []
		ThetaBGrad = []
		
		for i in range(0,self.L-1):
			ThetaWGrad.append(np.zeros(self.ThetaW[i].shape))
			ThetaBGrad.append(np.zeros(self.ThetaB[i].shape))

		
		#Calculate for final layer first
		dl = self.CFDelta(a[-1],y,self.AFgrad[-1])

		
		for i in range(self.L-2,-1,-1):
			ThetaBGrad[i][:] = np.dot(np.ones((1,m)),dl)/m
			ThetaWGrad[i][:] = np.dot(a[i].T,dl)/m + (Lambda/n)*self.ThetaW[i]
			
			#dl = np.dot(dl,self.ThetaW[i].T)*a[i]*(1-a[i])	
			dl = np.dot(dl,self.ThetaW[i].T)*self.AFgrad[i](a[i])	
		return ThetaWGrad,ThetaBGrad


	def _CalculateStep(self,X,y,Alpha,m,n):
		
		#first of all create arrays to allow forward propagation
		z,a = self._GetPropagationArrays(X)
		
		#now use them arrays to propagate the input data through the network
		self._ForwardPropagate(z,a)
		#self._ForwardPropagate(self._zc,self._ac)
		
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
			self.ThetaW[i] = self.ThetaW[i] - self.VW[i]
			self.ThetaB[i] = self.ThetaB[i] - self.VB[i]


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
		n = self.m
		if MiniBatchSize is None:
			nb = 1
			MiniBatchSize = n
		else:
			nb = np.int32(np.ceil(n/MiniBatchSize))
		#create arrays to store costs
		Jt = np.zeros(nEpoch,dtype='float32')

			
		#Get initial cost if there have been no steps
		if self.nSteps == 0:
			self._ForwardPropagate(self._z,self._a)
			self.Jt[0] = self.CF(self._a[-1],self.X,self.ThetaW,self.Lambda)

			self.nSteps = 1
		outstr = ''
		nSteps = 0
		StoppedLearning = False
		
		BatchStr = ColorString('Batches:','bright green')
		EpochStr = ColorString('Epochs:','bright green')
		HeadStr = ColorString('Total Epochs','bright green') + ColorString(' {:5d}   ','yellow') + ColorString('Training: Cost ','bright red') + ColorString('{:6.4f}','yellow')
		if not quiet:
			mpb = MultiProgressBar(nb,nEpoch,BatchStr,EpochStr,CharDone=ColorString('=','bright magenta'),CharTodo=ColorString('-','blue'),PercColor='cyan',FracColor='yellow')
		
		#print('\n\n\n')
		
		#loop through each epoch
		for i in range(0,nEpoch):
			
			#take a step for each mini batch
			for j in range(0,nb):
				
				X = self.X[j*MiniBatchSize:(j+1)*MiniBatchSize]
				m = X.shape[0]
				#ProgressBar2(j+1,nb,i+1,nEpoch,'Batch:','Epoch:',HeadStr=outstr,Final=False)
				if not quiet:
					mpb.UpdateBars(j+1,i+1,outstr)
				CalculateStep(X,X,Alpha,m,n)
			
			#once each batch has done, get cost functions
			self._ForwardPropagate(self._z,self._a)
			Jt[i] = self.CF(self._a[-1],self.X,self.ThetaW,self.Lambda)


			
			outstr = HeadStr.format(i + self.nSteps,Jt[i])

			if not quiet:
				mpb.UpdateBars(nb,i+1,outstr)
			#print(outstr,end='')
			nSteps += 1
			
			if EarlyStop:
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
	



	
	def _CheckCostGradient(self,nSteps,J,gTol,gTolEpochs,gTolMinEpochs):
		
		if nSteps < gTolMinEpochs or nSteps < gTolEpochs:
			return False
			
		J0 = J[nSteps - gTolEpochs]
		J1 = J[nSteps - 1]
		
		grad = (J0 - J1)/gTolEpochs
		
		if grad < gTol:
			return True		
			
			
	def TrainNetwork(self,nEpoch=100,MiniBatchSize=10,Alpha=1.0,gTol=0.0,gTolEpochs=10,gTolMinEpochs=10,Momentum=None):
		self.Momentum = Momentum
		self.VW = None
		self.VB = None
		if self.m == 0:
			print('Please insert training data before trining!')
			return
		
		
		#calculate number of mini batches
		n = self.m
		if MiniBatchSize is None:
			nb = 1
			MiniBatchSize = n
		else:
			nb = np.int32(np.ceil(n/MiniBatchSize))
		#create arrays to store costs
		Jt = np.zeros(nEpoch,dtype='float32')

			
		#Get initial cost if there have been no steps
		if self.nSteps == 0:
			self._ForwardPropagate(self._z,self._a)
			self.Jt[0] = self.CF(self._a[-1],self.X,self.ThetaW,self.Lambda)
			self.nSteps = 1
		
		nSteps = 0
		StoppedLearning = False
		#loop through each epoch
		for i in range(0,nEpoch):
			
			#take a step for each mini batch
			for j in range(0,nb):
				X = self.X[j*MiniBatchSize:(j+1)*MiniBatchSize]
				m = X.shape[0]
				self._CalculateStep(X,X,Alpha,m,n)
			
			#once each batch has done, get cost functions
			self._ForwardPropagate(self._z,self._a)
			Jt[i] = self.CF(self._a[-1],self.X,self.ThetaW,self.Lambda)

			outstr = '\rEpoch {:5d}, Training: Cost {:10.7f}'.format(i + self.nSteps,Jt[i])
			print(outstr,end='')
			nSteps += 1
			
			StoppedLearning = self._CheckCostGradient(nSteps,Jt,gTol,gTolEpochs,gTolMinEpochs-self.nSteps)
			if StoppedLearning:
				break
			
		print()
		if StoppedLearning:
			print('Cost function has stopped improving')
		else:
			print('Reached max epoch')
		#add the costs and accuracies to the 
		self.nSteps += nSteps
		self.Jt = np.append(self.Jt,Jt[:nSteps])

	def _GetEncodingArrays(self,x):
		a = []
		z = []
		a.append(x)
		m = x.shape[0]
		for i in range(0,(self.L-1)//2):
			zt = np.zeros((m,self.s[i+1]),dtype='float64')
			z.append(zt)
			a.append(zt)
		return z,a

	def _EncodePropagate(self,z,a):
		for i in range(0,(self.L-1)//2):
			z[i] = np.dot(a[i],self.ThetaW[i]) + self.ThetaB[i]
			a[i+1] = self.AF[i](z[i])		
	
	def _DecodePropagate(self,z,a):
		for i in range((self.L-1)//2,self.L-1):
			z[i] = np.dot(a[i],self.ThetaW[i]) + self.ThetaB[i]
			a[i+1] = self.AF[i](z[i])				

	def Encode(self,x):
		z,a = self._GetEncodingArrays(x)
		self._EncodePropagate(z,a)
		
		
		return a[-1]
		
	def Decode(self,):
		pass

	def TestCoding(self,X):
		z,a = self._GetPropagationArrays(X)
		self._ForwardPropagate(z,a)
		return a[-1]

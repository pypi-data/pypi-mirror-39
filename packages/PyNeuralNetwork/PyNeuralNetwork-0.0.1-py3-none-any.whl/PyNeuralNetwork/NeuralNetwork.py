import numpy as np
import matplotlib.pyplot as plt
from ._CppInterface import _CreateNetwork,_LoadNetwork,_SaveNetwork,_DestroyNetwork,_InputTrainingData,_InputCrossValidationData,_TrainGradientDescent,_TrainGradientDescentSingle,_GetnSteps,_GetTrainingProgress,_GetCrossValidationProgress,_ClassifyData

class NeuralNetwork (object):
	def __init__(self,Layers,Lambda=0.0,ThetaRange=0.12):
		if isinstance(Layers,str):
			#load network
			self.s,self.instance = _LoadNetwork(1,Layers)
		else:
			self.s = [Layers]
			self.instance = _CreateNetwork(1,[Layers],Lambda,ThetaRange)	

	def __del__(self):
		_DestroyNetwork(self.instance)

	def InputTrainingData(self,Xin,yin,verb=True):
		_InputTrainingData(self.instance,0,Xin,yin,verb)
		
	def InputCrossValidationData(self,Xin,yin,verb=True):
		_InputCrossValidationData(self.instance,0,Xin,yin,verb)		
		
	def TrainNetwork(self,MaxIter=100,Alpha=1.0,verb=True):
		self.GradientDescentTrain(MaxIter,Alpha,verb)
			
	def GradientDescentTrain(self,MaxIter=100,Alpha=1.0,verb=True):
		_TrainGradientDescent(self.instance,MaxIter,Alpha,verb)
	

	
	def ShowTrainingSetAccuracy(self):
		J,Acc = _GetTrainingProgress(self.instance,0,1)
		print("Training Set Accuracy: {:6.2f}%".format(100.0*Acc[-1]))
		
	def ShowCVSetAccuracy(self):
		J,Acc = _GetCrossValidationProgress(self.instance,0,1)
		print("CV Set Accuracy: {:6.2f}%".format(100.0*Acc[-1]))

	
	def GetTrainingSetProgress(self):
		J,Acc = _GetTrainingProgress(self.instance,0,1)
		return J,Acc

	def GetCVSetProgress(self):
		J,Acc = _GetCrossValidationProgress(self.instance,0,1)
		return J,Acc
	
	
			
	def ClassifyData(self,Xin):
		
		y,p = _ClassifyData(self.instance,0,Xin,self.s[0][-1])
		return y,p
		

	def SaveNetwork(self,FileName=''):
		if FileName == '':
			print('Please enter valid file name')
			return
	
		_SaveNetwork(self.instance,FileName)
	
		print('Saved: '+FileName)
		
	def PlotAccuracy(self,fig=None,maps=[1,1,0,0]):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		Jt,Acct = _GetTrainingProgress(self.instance,0,1)
		Jc,Accc = _GetCrossValidationProgress(self.instance,0,1)
		
		ax.plot(Acct,color=[1.0,0.0,0.0],label='Training Set Accuracy')
		ax.plot(Accc,color=[0.0,0.0,1.0],label='Cross-validation Set Accuracy')
		legend = ax.legend(loc='lower right')
		ax.axis([0,Acct.size,0.0,100.0])
		fig.xlabel('Iterations')
		fig.ylabel('Accuracy')	
		return ax
			

	def PlotCost(self,fig=None,maps=[1,1,0,0]):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		Jt,Acct = _GetTrainingProgress(self.instance,0,1)
		Jc,Accc = _GetCrossValidationProgress(self.instance,0,1)
		
		ax.plot(Jt,color=[1.0,0.0,0.0],label='Training Set Cost')
		ax.plot(Jc,color=[0.0,0.0,1.0],label='Cross-validation Set Cost')
		legend = ax.legend(loc='upper right')
		#ax.axis([0,Jt.size,0.0,1.0])
		fig.xlabel('Iterations')
		fig.ylabel('Cost')	
		return ax







class NeuralNetworkArray (object):
	def __init__(self,nN,Layers,Lambda=0.0,ThetaRange=0.12):
		self.Normalize = False
		if isinstance(Layers,str):
			#load network
			self.nN = nN
			self.s,self.instance = _LoadNetwork(nN,Layers)
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
				
			self.instance = _CreateNetwork(self.nN,self.s,self.Lambda,self.ThetaRange)	

	def __del__(self):
		_DestroyNetwork(self.instance)

	def InputTrainingData(self,ind,Xin,yin,verb=True,Normalize=False,nSigma=3.0):
		self.Normalize = Normalize
		if Normalize:
			#calculate mean and standard deviation
			#subtract mean and divide by nSigma*Sigma
			self.mu = np.mean(Xin,axis=0)
			self.sigma = np.std(Xin,axis=0)
			self.nsigma = nSigma
			X = (Xin - self.mu)/(self.nsigma*self.sigma)
		else:
			X = Xin		
		_InputTrainingData(self.instance,ind,X,yin,verb)
		
	def InputCrossValidationData(self,ind,Xin,yin,verb=True):
		if self.Normalize:
			#calculate mean and standard deviation
			#subtract mean and divide by nSigma*Sigma
			X = (Xin - self.mu)/(self.nsigma*self.sigma)
		else:
			X = Xin			
		_InputCrossValidationData(self.instance,ind,X,yin,verb)		
			
	def GradientDescentTrain(self,MaxIter=100,Alpha=1.0,verb=True):
		_TrainGradientDescent(self.instance,MaxIter,Alpha,verb)
	
	def GradientDescentTrainSingle(self,ind,MaxIter=100,Alpha=1.0,verb=True):
		_TrainGradientDescentSingle(self.instance,ind,MaxIter,Alpha,verb)
	
	def ShowTrainingSetAccuracy(self,ind):
		J,Acc = _GetTrainingProgress(self.instance,ind,self.nN)
		print("Training Set Accuracy: {:6.2f}%".format(100.0*Acc[-1]))
		
	def ShowCVSetAccuracy(self,ind):
		J,Acc = _GetCrossValidationProgress(self.instance,ind,self.nN)
		print("Training Set Accuracy: {:6.2f}%".format(100.0*Acc[-1]))

	
	def GetTrainingSetProgress(self,ind):
		J,Acc = _GetTrainingProgress(self.instance,ind,self.nN)
		return J,Acc

	def GetCVSetProgress(self,ind):
		J,Acc = _GetCrossValidationProgress(self.instance,ind,self.nN)
		return J,Acc
	
	
			
	def ClassifyData(self,ind,Xin):
		if self.Normalize:
			#calculate mean and standard deviation
			#subtract mean and divide by nSigma*Sigma
			X = (Xin - self.mu)/(self.nsigma*self.sigma)
		else:
			X = Xin			
		y,p = _ClassifyData(self.instance,ind,X,self.s[ind][-1])
		return y,p
		

	def SaveNetwork(self,FileName=''):
		if FileName == '':
			print('Please enter valid file name')
			return
	
		_SaveNetwork(self.instance,FileName)
	
		print('Saved: '+FileName)
		
	def PlotAccuracy(self,ind,fig=None,maps=[1,1,0,0]):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		Jt,Acct = _GetTrainingProgress(self.instance,ind,self.nN)
		Jc,Accc = _GetCrossValidationProgress(self.instance,ind,self.nN)
		
		ax.plot(Acct,color=[1.0,0.0,0.0],label='Training Set Accuracy')
		ax.plot(Accc,color=[0.0,0.0,1.0],label='Cross-validation Set Accuracy')
		legend = ax.legend(loc='lower right')
		ax.axis([0,Acct.size,0.0,100.0])
		fig.xlabel('Iterations')
		fig.ylabel('Accuracy')	
		return ax
			

	def PlotCost(self,ind,fig=None,maps=[1,1,0,0]):
		
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		Jt,Acct = _GetTrainingProgress(self.instance,ind,self.nN)
		Jc,Accc = _GetCrossValidationProgress(self.instance,ind,self.nN)
		
		ax.plot(Jt,color=[1.0,0.0,0.0],label='Training Set Cost')
		ax.plot(Jc,color=[0.0,0.0,1.0],label='Cross-validation Set Cost')
		legend = ax.legend(loc='upper right')
		#ax.axis([0,Jt.size,0.0,1.0])
		fig.xlabel('Iterations')
		fig.ylabel('Cost')	
		return ax

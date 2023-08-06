import numpy as np
from . import Globals
from scipy import misc
from .Autoencoder import Autoencoder
from .Tools.RemoveAxisLabels import RemoveAxisLabels
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

mnistfiles = ['t10k-images.idx3-ubyte','t10k-labels.idx1-ubyte','train-images.idx3-ubyte','train-labels.idx1-ubyte']
mnistpath = Globals.DATA_PATH+'MNIST/'

def ReadMNISTLabels(Train=True):
	if Train:
		fname = mnistfiles[3]
	else:
		fname = mnistfiles[1]
	
	f = open(mnistpath + fname,'rb')
	MagNum = np.fromfile(f,dtype='>i4',count=1)[0]
	n = np.fromfile(f,dtype='>i4',count=1)[0]
	y = np.fromfile(f,dtype='>u1',count=n)
	f.close()
	return y
	
def ReadMNISTImages(Train=True,Flatten=False):
	if Train:
		fname = mnistfiles[2]
	else:
		fname = mnistfiles[0]
		
	f = open(mnistpath + fname,'rb')
	MagNum = np.fromfile(f,dtype='>i4',count=1)[0]
	n = np.fromfile(f,dtype='>i4',count=1)[0]
	nr = np.fromfile(f,dtype='>i4',count=1)[0]
	nc = np.fromfile(f,dtype='>i4',count=1)[0]
	if Flatten:
		X = np.fromfile(f,dtype='>u1',count=n*nr*nc).reshape((n,nr*nc)).astype('float32')/255
	else:
		X = np.fromfile(f,dtype='>u1',count=n*nr*nc).reshape((n,nr,nc)).astype('float32')/255
	f.close()
	return X	
		


def GetMNISTData():
	Xtrain = ReadMNISTImages(True,True)
	Xtest = ReadMNISTImages(False,True)
	ytrain = ReadMNISTLabels(True)
	ytest = ReadMNISTLabels(False)
	
	return Xtrain,ytrain,Xtest,ytest


def ReadDigit(i):
	fname = '{:d}.bmp'.format(i)
	image = 1 - misc.imread(mnistpath+fname,flatten=True)/255
	return image

def ReadDigits():
	out = []
	for i in range(0,10):
		out.append(ReadDigit(i).flatten())
	return np.array(out)


def _GetFrameRenderer(ae,fig,inds,Method,MiniBatchSize):

	def _DrawFrame(i):
		#fig.clf()
		print('Frame {0}'.format(i))
		if i > 0:
			ae.Train(nEpoch=1,Method=Method,MiniBatchSize=MiniBatchSize)
		ae.TestSquareExamples(inds,fig)
		
	return _DrawFrame


def AnimateMNISTAutoencoder(fname='MNISTAE',nEpoch=11,dT=250,Method='rmsprop',MiniBatchSize=1000):
	inds = np.arange(60000)
	np.random.shuffle(inds)
	inds = inds[:25]
		
	fout = fname+'{:d}.gif'.format(nEpoch)
	plt.ioff()	
	ae = MNISTAutoEncoder(128)
	fig = ae.TestSquareExamples(inds)
	cf = fig.gcf()
	DF = _GetFrameRenderer(ae,fig,inds,Method,MiniBatchSize)
	print('Starting Animation')
	anim = FuncAnimation(cf,DF,frames=nEpoch,interval=dT)
	print('Saving')
	anim.save(fout,dpi=95,writer='imagemagick')
	plt.close()
	plt.ion()	
	
	
	

class MNISTAutoEncoder(object):
	def __init__(self,CodeLayer=128,HiddenLayer=[],ActFuncs='sigmoid',CostFunction='mean-squared',Lambda=0.0,Subset=None):
	
	
		self.Xt,self.yt,self.Xc,self.yc = GetMNISTData()
		if not Subset is None:
			self.Xt = self.Xt[:Subset]
		self.net = Autoencoder(784,CodeLayer,HiddenLayer,ActFuncs,CostFunction,Lambda)
		self.net.InputData(self.Xt)
	
	def Train(self,Method='rmsprop',nEpoch=20,MiniBatchSize=1000,**kwargs):
		kwargs['nEpoch'] = nEpoch
		kwargs['MiniBatchSize'] = MiniBatchSize
		self.net.Train(Method,**kwargs)
		
	def TestExample(self,i=None):
		fig = plt
		fig.figure(figsize=(12,5))
		
		if i is None:
			i = np.random.randint(self.Xt.shape[0])
		x0 = np.array([self.Xt[i]])
		x1 = self.net.TestCoding(x0)
		
		x0 = x0.reshape((28,28))
		x1 = x1.reshape((28,28))
		ax0 = fig.subplot2grid((1,2),(0,0))
		ax0.imshow(x0,cmap=plt.cm.get_cmap('gnuplot'))
		ax1 = fig.subplot2grid((1,2),(0,1))
		ax1.imshow(x1,cmap=plt.cm.get_cmap('gnuplot'))

	def TestSquareExamples(self,n,fig=None):
		
		if np.size(n) == 1:
			m = self.Xt.shape[0]
			inds = np.arange(m)
			np.random.shuffle(inds)
			inds = inds[:n*n]
		else:
			inds = np.copy(n)
			n = np.int32(np.sqrt(np.size(inds)))
			
		input_plot = np.zeros((n*28,n*28),dtype='float32')
		output_plot = np.zeros((n*28,n*28),dtype='float32')
		
		X0 = self.Xt[inds]
		X1 = self.net.TestCoding(X0)
		
		for i in range(0,n):
			for j in range(0,n):
				I = j + i*n
				x0 = X0[I].reshape((28,28))
				x1 = X1[I].reshape((28,28))
				input_plot[i*28:(i+1)*28,j*28:(j+1)*28] = x0
				output_plot[i*28:(i+1)*28,j*28:(j+1)*28] = x1
				
		
		if fig is None:
			fig = plt
			fig.figure(figsize=(12,5))	
		fig.suptitle('Epoch: {:d}'.format(self.net.nSteps))	
		ax0 = fig.subplot2grid((1,2),(0,0))
		ax0.imshow(input_plot,cmap=plt.cm.get_cmap('Greys'))
		ax0.set_title('Original Data')
		RemoveAxisLabels(ax0,'x')
		RemoveAxisLabels(ax0,'y')
		ax1 = fig.subplot2grid((1,2),(0,1))
		ax1.imshow(output_plot,cmap=plt.cm.get_cmap('Greys'))
		ax1.set_title('Reproduced Data')
		RemoveAxisLabels(ax1,'x')
		RemoveAxisLabels(ax1,'y')
		return fig
		
def MNISTClassifier(HiddenLayers=[128],ActFuncs='sigmoid',CostFunction='cross-entropy',Lambda=0.0):
	
	Xt,yt,Xc,yc = GetMNISTData()
	Layers = np.concatenate(([784],HiddenLayers,[10]))
	net = pNetwork(Layers,Lambda,ActFuncs=ActFuncs,CostFunction=CostFunction)
	net.InputTrainingData(Xt,yt)
	net.InputCrossValidationData(Xc,yc)
	return net

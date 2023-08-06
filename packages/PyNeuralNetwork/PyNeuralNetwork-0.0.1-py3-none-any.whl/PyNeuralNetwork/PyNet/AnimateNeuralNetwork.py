import numpy as np
import matplotlib.pyplot as plt
from .NeuralNetwork import NeuralNetwork
from matplotlib.animation import FuncAnimation

def _GetFrameRenderer(fig,net,X,y,nEpoch,label,nTrain=1):

	def _DrawFrame(i):
		#fig.clf()
		print('Frame {0}'.format(i))
		fig.suptitle(label)
		net.TrainNetwork(nTrain,1)
		net.PlotArchitecture(fig,[2,2,0,0])
		_PlotTruthTable(fig,[2,2,1,0],net,X,y)
		net.PlotCost(fig,[2,2,0,1],[0,nEpoch])
		net.PlotAccuracy(fig,[2,2,1,1],[0,nEpoch],[0.0,100.0])
		fig.tight_layout()
		
	return _DrawFrame

def _PlotTruthTable(fig,maps,net,X,y):
	
	uX,uind = np.unique(X,axis=0,return_index=True)
	uy = y[uind]
	
	_,res = net.Classify(uX)
	res = np.char.mod('%4.2f',res)
	tab = (np.append(uX.T,[uy-1],axis=0).T).astype('U1')
	tab = np.append(tab.T,[res],axis=0).T
	
	nx = uX.shape[1]
	labs = []
	for i in range(0,nx):
		labs.append('$x_{:d}$'.format(i))
	labs.append('$y$')
	labs.append('$h$')
	
	
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	table = ax.table(cellText=tab,colLabels=labs,loc='center')
	ax.axis('off')
	table.scale(1,4)

def AnimateNeuralNetwork(X,y,Layers,nEpoch=100,label='',dT=100,nTrain=1):
	plt.ioff()
	net = NeuralNetwork(Layers)
	net.InputTrainingData(X,y)
	
	fig = plt
	fig.figure(figsize=(10,7))
	cf = fig.gcf()
	
	DF = _GetFrameRenderer(fig,net,X,y,nEpoch,label,nTrain)
	print('Starting Animation')
	anim = FuncAnimation(cf,DF,frames=nEpoch//nTrain,interval=dT)
	print('Saving')
	anim.save(label.replace(' ','')+'NN.gif',dpi=95,writer='imagemagick')
	plt.close()
	plt.ion()


def AnimateANDGate():
	
	X = np.array([[0,0],[0,1],[1,0],[1,1]])
	y = np.array([0,0,0,1])+1
	
	AnimateNeuralNetwork(X,y,[2,1],100,'AND Gate')
	
	
def AnimateNANDGate():
	
	X = np.array([[0,0],[0,1],[1,0],[1,1]])
	y = np.array([1,1,1,0])+1
	
	AnimateNeuralNetwork(X,y,[2,1],100,'NAND Gate')

def AnimateORGate():
	
	X = np.array([[0,0],[0,1],[1,0],[1,1]])
	y = np.array([0,1,1,1])+1
	
	AnimateNeuralNetwork(X,y,[2,1],100,'OR Gate')

def AnimateXORGate():
	
	X = np.array([[0,0],[0,1],[1,0],[1,1]])
	y = np.array([0,1,1,0])+1
	
	AnimateNeuralNetwork(X,y,[2,2,1],1000,'XOR Gate',nTrain=10)

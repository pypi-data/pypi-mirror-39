import numpy as np
import matplotlib.pyplot as plt
from ..Tools.PlotCircle import PlotCircle

def PlotNetwork(Layers,ShowUnitLabels=True,InputXLabel=True,ShowThetaLabels=True,figsize=(12,9*0.75),lw=2.0):
	
	
	L = np.size(Layers)
	Lmax = np.max(Layers)
	
	R = np.min([0.8/Lmax,((16/9)-0.2)*0.5/L])/2.0
	Gapy = (1.0 - 0.1 - 2*R)/(Lmax-1)
	
	#This is set up for a 16:9 ratio
	fig = plt
	fig.figure(figsize=figsize)
	ax = fig.gca()
	ax.set_position([0,0,1,1])
	ax.axis([0.0,figsize[0]/figsize[1],0.0,1.0])
	ax.set_xticks([0.0])
	ax.set_yticks([0.0])
	
	X = []
	Y = []

	for i in range(0,L):
		xt = np.zeros(Layers[i],dtype='float32')
		yt = np.zeros(Layers[i],dtype='float32')
		for j in range(0,Layers[i]):
			xt[j] = (0.05 + R + ((1.0-2*R-0.1)/(L-1))*i)*figsize[0]/figsize[1]
			yt[j] = 1.0 - (0.05 + R + Gapy*j + 0.9*0.5*(1.0-Layers[i]/Lmax))
		X.append(xt)
		Y.append(yt)
			
	for i in range(0,L):	
		if i == 0:
			UnitCol = [0.0,0.0,1.0]
		elif i == L-1:
			UnitCol = [0.0,1.0,0.0]
		else:
			UnitCol = [1.0,0.75,0.0]
			
		for j in range(0,Layers[i]):
			PlotCircle(fig,R,x0=X[i][j],y0=Y[i][j],linewidth=2.0,linestyle='-',zorder=2,color=UnitCol,fill=[1.0,1.0,1.0])
			if ShowUnitLabels:
				istr = '({0})'.format(i+1)
				if InputXLabel and i == 0:
					lab = '$x_{0}$'.format(j)
				elif i == L-1:
					lab = '$a_{0}$'.format(j+1)+'$^{'+istr+'}$'
				else:
					lab = '$a_{0}$'.format(j)+'$^{'+istr+'}$'
				fig.text(X[i][j],Y[i][j],lab,ha='center',va='center',size=200*R)
			if i < L-1:
				if i == L-2:
					st = 0
				else:
					st = 1
				for k in range(st,Layers[i+1]):
					fig.plot([X[i][j],X[i+1][k]],[Y[i][j],Y[i+1][k]],color=[0.25,0.25,0.25],linewidth=lw,zorder=0.0)
					
				if ShowThetaLabels:
					istr = '({0})'.format(i+1)
					for k in range(0,Layers[i+1]):
						thstr = r'$\theta$'+'$_{'+'{0},{1}'.format(j,k)+'}$'+'$^{'+istr+'}$'
						fig.text(0.5*(X[i][j]+X[i+1][k]),0.5*(Y[i][j]+Y[i+1][k]),thstr,size=200*R)

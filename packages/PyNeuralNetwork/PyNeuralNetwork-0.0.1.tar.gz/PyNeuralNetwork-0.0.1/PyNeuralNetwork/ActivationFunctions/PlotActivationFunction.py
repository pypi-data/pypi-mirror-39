import numpy as np
import matplotlib.pyplot as plt
from .. import Globals

def PlotActivationFunction(name,rnge=[-5,5],n=100):
	
	F,G = Globals.ActFuncs[name.lower()]
	
	z = np.linspace(rnge[0],rnge[1],n)
	f = F(z)
	g = G(z)
	
	fig = plt
	fig.figure()
	fig.plot(z,f,color=[0.0,0.0,1.0],label=name)
	fig.plot(z,g,color=[1.0,0.5,0.0],label=name+' gradient')
	
	R = fig.axis()
	fig.axis([rnge[0],rnge[1],R[2],R[3]])
	
	fig.plot(rnge,[0.0,0.0],color=[0.0,0.0,0.0],linestyle=':')
	fig.plot([0.0,0.0],[R[2],R[3]],color=[0.0,0.0,0.0],linestyle=':')
	fig.legend()

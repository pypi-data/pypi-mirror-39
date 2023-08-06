import numpy as np
from .Sigmoid import InverseSigmoid,SigmoidGradient

def MeanSquareCost(h,y,ThetaW,Lambda=0.0):
	m = y.shape[0]
	J = np.sum((h - y)**2)/(2*m)
	
	
	if Lambda > 0.0:
		
		nL = np.size(ThetaW)
		#Regularization
		Reg = 0.0
		for i in range(0,nL):
			T = ThetaW[i]
			Reg += Lambda/(2.0*m) * np.sum(T**2.0)

		J += Reg
	
	return J	

def MeanSquareDelta(h,y):
	
	z = InverseSigmoid(h)
	return (h - y)*SigmoidGradient(z)

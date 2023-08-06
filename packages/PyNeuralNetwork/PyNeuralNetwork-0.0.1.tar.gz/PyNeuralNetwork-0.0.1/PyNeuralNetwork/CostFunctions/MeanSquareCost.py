import numpy as np
from ._Regularization import _L1Reg,_L2Reg

def MeanSquareCost(h,y,ThetaW,L1=0.0,L2=0.0):
	m = y.shape[0]
	#diff = (h-y)**2
	#print(h.dtype,y.dtype,diff.dtype,h.min(),h.max(),y.min(),y.max(),diff.min(),diff.max(),np.sum(diff))
	#J = np.sum((h - y)**2)/(2*m)
	J = np.mean((h - y)**2)/2
	
	
	if L1 > 0.0:
		L1Reg = _L1Reg(ThetaW,L1,m)
	else:
		L1Reg = 0.0
	
	if L2 > 0.0:
		L2Reg = _L2Reg(ThetaW,L2,m)
	else:
		L2Reg = 0.0	
	
	J = J + L1Reg + L2Reg
	return J	

def MeanSquareDelta(h,y,InvAFgrad):

	return (h - y)*InvAFgrad(h)

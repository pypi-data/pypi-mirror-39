import numpy as np

def _L1Reg(ThetaW,L1,m):
	L = np.size(ThetaW)
	Reg = 0.0
	for i in range(0,L-1):
		T = ThetaW[i]
		Reg += L1/(2.0*m) * np.sum(np.abs(T))		
	return Reg
	
def _L2Reg(ThetaW,L2,m):
	L = np.size(ThetaW)
	Reg = 0.0
	for i in range(0,L-1):
		T = ThetaW[i]
		Reg += L2/(2.0*m) * np.sum(T**2.0)	
	return Reg

import numpy as np


def _GetOneHotClassLabels(y):
	m = np.size(y)
	k = self.s[-1]
	ind_offset = np.arange(m)*k
	yout = np.zeros((m,k))
	yout.flat[ind_offset + y.ravel()-1] = 1
	return yout

def CrossEntropyCost(h,y,ThetaW,Lambda=0.0):
	
	J = 0.0
	m = y.shape[0]
	K = y.shape[1]

	for k in range(0,K):
		yk = y[:,k]
		hk = h[:,k]
		J +=  (1.0/m)*np.sum(-yk*np.log(hk.clip(min=1e-40)) - (1.0 - yk)*np.log((1.0 - hk).clip(min=1e-40)))		
	
	
	if Lambda > 0.0:
		nL = np.size(ThetaW)
		#Regularization
		Reg = 0.0
		for i in range(0,nL):
			T = ThetaW[i]
			Reg += Lambda/(2.0*m) * np.sum(T**2.0)

		J += Reg
	
	return J


def CrossEntropyDelta(h,y):
	return h - y

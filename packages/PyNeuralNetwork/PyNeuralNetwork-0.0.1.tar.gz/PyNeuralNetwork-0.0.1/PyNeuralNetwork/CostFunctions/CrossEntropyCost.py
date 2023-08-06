import numpy as np
from ._Regularization import _L1Reg,_L2Reg

def _GetOneHotClassLabels(y):
	m = np.size(y)
	k = self.s[-1]
	ind_offset = np.arange(m)*k
	yout = np.zeros((m,k))
	yout.flat[ind_offset + y.ravel()-1] = 1
	return yout

def CrossEntropyCost(h,y,ThetaW,L1=0.0,L2=0.0):
	
	J = 0.0
	m = y.shape[0]
	K = y.shape[1]

	for k in range(0,K):
		yk = y[:,k]
		hk = h[:,k]
		J +=  (1.0/m)*np.sum(-yk*np.log(hk.clip(min=1e-40)) - (1.0 - yk)*np.log((1.0 - hk).clip(min=1e-40)))		
	
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


def CrossEntropyDelta(h,y,InvAFgrad):
	return h - y

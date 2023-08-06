import numpy as np

def Tanh(z):
	z = np.array(z)
	ez = np.exp(-2*z)
	sigz = (1.0/(1.0+ez))
	return 2*sigz - 1
	
def TanhGradient(z):
	th = Tanh(z)
	return 1 - th**2
	
def InverseTanh(a):
	sigz = (a + 1.0)/2.0
	ez = 1.0/sigz - 1.0
	z = np.log(ez)/(-2.0)
	return z
	
def InverseTanhGradient(a):
	z = InverseTanh(a)
	return TanhGradient(z)

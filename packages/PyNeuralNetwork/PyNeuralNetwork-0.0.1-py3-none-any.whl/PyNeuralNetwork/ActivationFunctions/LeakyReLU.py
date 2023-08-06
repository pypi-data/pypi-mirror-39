import numpy as np

def LeakyReLU(z):
	
	z = np.array(z)
	gt0 = np.float64(z > 0).clip(min=0.01)
	a = z*gt0
	return a
	
def LeakyReLUGradient(z):
	z = np.array(z)
	gt0 = np.float64(z > 0).clip(min=0.01)
	return gt0


def InverseLeakyReLU(a):
	a = np.array(a)
	gt0 = np.float64(a > 0).clip(min=0.01)
	z = a/gt0
	return z

def InverseLeakyReLUGradient(a):
	z = InverseLeakyReLU(a)
	return LeakyReLUGradient(z)

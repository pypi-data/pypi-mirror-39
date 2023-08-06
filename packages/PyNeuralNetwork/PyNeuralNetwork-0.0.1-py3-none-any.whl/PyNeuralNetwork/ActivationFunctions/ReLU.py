import numpy as np

def ReLU(z):
	
	z = np.array(z)
	gt0 = np.float64(z > 0)
	a = z*gt0
	return a
	
def ReLUGradient(z):
	z = np.array(z)
	gt0 = np.float64(z > 0)
	return gt0


import numpy as np

def Linear(z):
	return np.array(z)
	
def LinearGradient(z):
	z = np.array(z)
	return np.ones(z.shape,dtype='float64')


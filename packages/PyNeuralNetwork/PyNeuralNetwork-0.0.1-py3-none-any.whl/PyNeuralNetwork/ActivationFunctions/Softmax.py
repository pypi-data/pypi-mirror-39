import numpy as np

def Softmax(z):
	return (np.exp(z).T/np.sum(np.exp(z),axis=1)).T

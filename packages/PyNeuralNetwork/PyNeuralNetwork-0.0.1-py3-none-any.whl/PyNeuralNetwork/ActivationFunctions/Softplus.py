import numpy as np

def Softplus(z):
	#ReLU == Rectified linear unit
	#This is an approximation called the softplus function - the derivitive of which is the sigmoid function
	z = np.array(z)
	if np.size(z) > 1:
		bad = np.where(z > 50)
		good = np.where(z <=50)
		out = np.copy(z)
		out[bad] = z[bad]
		out[good] = np.log(1.0 + np.exp(z[good]))
		return out
	else:
		if z > 50:
			return z
		else:
			return np.log(1.0 + np.exp(z))

def SoftplusGradient(z):
	#ReLU == Rectified linear unit
	#This is an approximation called the softplus function - the derivitive of which is the sigmoid function

	z = np.array(z)
	if np.size(z) > 1:
		bad = np.where(z > 50)
		good = np.where(z <=50)
		out = np.copy(z)
		out[bad] = 1
		out[good] = 1.0/(1.0 + np.exp(-z[good]))
		return out
	else:
		if z > 50:
			return 1
		else:
			return 1.0/(1.0 + np.exp(-z))


def InverseSoftplus(a):
	
	z = np.log10(np.exp(a) - 1.0)
	return z
	

def InverseSoftplusGradient(a):
	z = InverseSoftplus(a)
	return SoftplusGradient(z)

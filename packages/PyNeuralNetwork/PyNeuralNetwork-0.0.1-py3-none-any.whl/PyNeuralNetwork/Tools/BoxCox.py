import numpy as np
from scipy.stats import boxcox,boxcox_normmax

def BoxCox(x,lamda,shift=None):
	if shift is None:
		xs,shift = ShiftX(x)
	else:
		xs = x + shift
	if lamda == 0:
		xt = np.log(xs)
	else:
		xt = (xs**lamda - 1)/lamda
	return xt
	
def BoxCoxLogLikelihood(x,lamda):
	n = np.size(x)
	xl = BoxCox(x,lamda)
	xlbar = np.mean(xl)
	
	fxl = -(n/2)*np.log(np.sum((xl - xlbar)**2)/n) + (lamda-1)*np.sum(np.log(x))
	
	return fxl

def MaximizeBoxCoxLikelihood(x,LamdaRange=[-4.0,4.0],Tol=0.001):
	#import matplotlib.pyplot as plt
	
	LR = np.array(LamdaRange)
	dL = 1.0
	Repeat = True
	out = 1.0
	while Repeat:
		nL = np.int32((LR[1]-LR[0])/dL)
		L = np.arange(nL)*dL + LR[0]
		ll = np.zeros(nL,dtype='float64')
		for j in range(0,nL):
			ll[j] = BoxCoxLogLikelihood(x,L[j])
		#print(ll)
		bad = np.where(np.isfinite(ll) == False)[0]
		ll[bad] = np.nan
		good = np.where(np.isfinite(ll))[0]
		if good.size == 0:
			return np.nan
		best = np.where(ll == np.nanmax(ll))[0]
		#print(best,ll[best[0]])
		if best[0] == 0:
			best[0] = 1
		if best[0] == nL-1:
			best[0] -= 1
		if dL < Tol:
			out = L[best[0]]
			Repeat = False
		#plt.plot(L,ll)
		LR = np.array([L[best[0]-1],L[best[0]+1]])
		dL = (LR[1]-LR[0])/nL
	return out


def ShiftX(xin):
	x = xin[np.isfinite(xin)]
	shift = 0.0
	if (x < 0).any():
		newx = x - np.min(x)
		shift += -np.min(x)
	else:
		newx = x
	if (newx == 0).any():
		gt0 = np.where(newx > 0)[0]
		if gt0.size == 0:
			return x,np.nan
		minx = np.min(newx[newx > 0])/2.0
		newx += minx
		shift += minx
	return newx,shift
	

def FitBoxCox(x):

	#first of all - shift the data so that there are no negatives!
	xs,shift = ShiftX(x)
	if np.isnan(shift):
		return x,1.0,1.0
	#now use scipy.stats.boxcox to fit function
	#lamda = boxcox_normmax(xs,brack=(-2.0,1.9),method='all').min()
	lamda = MaximizeBoxCoxLikelihood(xs)
	xt = boxcox(xs,lamda)
	
	return xt,lamda,shift
	
def ReverseBoxCox(xt,lamda,shift):
	if lamda == 0:
		xs = np.exp(xt)
	else:
		xs = (xt*lamda + 1)**(1/lamda)
		
	x = xs-shift
	return x
	
	
def BoxCoxNormalize(x,nSigma=1.0,NotFin='ignore'):
	#copy input array
	X = np.copy(x.astype('float64'))
	
	#deal with bad data - NotFin to value to replace infs and NaNs with
	if NotFin is 'ignore':
		good = np.where(np.isfinite(X))[0]
		Xg = X[good]
	else:
		bad = np.where(np.isfinite(X) == False)[0]
		X[bad] = NotFin
		Xg = X

	if Xg.size == 0:
		return X,0.0,1.0,1.0,1.0
	
	#perform BC transform
	Xbc,lamda,shift = FitBoxCox(Xg)
	
	Xbc[np.isfinite(Xbc) == False] = np.nan
	
	#calculate mean and std
	mu = np.nanmean(Xbc)
	nsig = np.nanstd(Xbc)*nSigma
	
	#rescale data
	Xs = (Xbc - mu)/(nsig)
	
	#Add bad data back in if necessary
	if NotFin is 'ignore':
		Xout = np.zeros(X.size,dtype='float64')+np.nan
		Xout[good] = Xs
	else:
		Xout = Xs
	return Xout,mu,nsig,lamda,shift
	
def BoxCoxUnNormalize(x,mu,nsig,lamda,shift):
	Xs = np.copy(x)
	Xbc = Xs*nsig + mu
	Xout = ReverseBoxCox(Xbc,lamda,shift)
	
	return Xout
		
	

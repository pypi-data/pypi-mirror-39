import numpy as np
import NeuralNetwork as nnet
import matplotlib.pyplot as plt

def TestPython():

	Theta = [np.array([[0.06321,   -0.03352,    0.00713],   [-0.00333,   -0.10788,    0.11148]]), 
			np.array([[0.01134,    0.00081,   -0.11814],    [0.01597,    0.10201,    0.05310]])]
	
	f = open('trainingdata.dat','r')
	lines = f.readlines()
	f.close()
	
	y = np.zeros(24,dtype='int32')
	x = np.zeros((24,2),dtype='float32')
	
	for i in range(0,24):
		s = lines[i].split()
		x[i,0] = np.float32(s[0])
		x[i,1] = np.float32(s[1])
		y[i] = np.int32(s[2])
	
	
	nn = nnet.NeuralNetwork(np.array([2,2,2]),0.0,Theta)
	nn.InputTrainingData(x,y)
	nn.GradientDescentTrain(1000,1.0)
	nn.TrainNetwork()
	#print(nn.dJ)
	
def TestPython2():
	
	x1 = 2.5*np.random.randn(1000) + 5.0
	y1 = np.zeros(1000)+1
	
	
	x2 = 1.5*np.random.randn(1000) - 2.0
	y2 = np.zeros(1000)+2
	
	h1,b1 = np.histogram(x1,bins=20)
	bc1 = 0.5*(b1[:-1] + b1[1:])
	
	h2,b2 = np.histogram(x2,bins=20)
	bc2 = 0.5*(b2[:-1] + b2[1:])
	
	plt.figure()
	plt.plot(bc1,h1)
	plt.plot(bc2,h2)
	
	x = np.append(x1,x2)
	y = np.append(y1,y2)
	
	ind = np.arange(2000)
	np.random.shuffle(ind)
	
	x = x[ind]
	y = y[ind]
	
	xt = x[0:1500]
	yt = y[0:1500]
	
	xcv = x[1500:]
	ycv = y[1500:]
	
	
	nn = nnet.NeuralNetwork(np.array([1,2,2]),0.0)
	nn.InputTrainingData(np.array([xt]).T,yt)
	nn.InputCrossValidationData(np.array([xcv]).T,ycv)
	nn.TrainNetwork()
	print(nn.GetTrainingSetAccuracy(),nn.GetCVSetAccuracy())
	
	
	
def TestPython3():
	
	x1 = np.array([ 6.77840789,  1.33019172,  5.38676427,  3.11548739,  4.3502877 ,  7.1006716 ,  6.75914805,  6.10551742,  2.63819611,  1.99015142])
	y1 = np.zeros(10)+1
	
	
	x2 = np.array([-1.0672715 , -6.38518699, -4.01523372, -0.43279053, -1.98294515,  -4.31963048, -2.72775383, -3.68820375,  0.72378299, -1.70199415])

	y2 = np.zeros(10)+2
	
	
	x = np.append(x1,x2)
	y = np.append(y1,y2)
	
	ind = np.arange(20)
	np.random.shuffle(ind)
	
	x = x[ind]
	y = y[ind]
	
	xt = np.array([ 1.99015142,  3.11548739,  2.63819611,  6.77840789,  6.75914805,  7.1006716 , -0.43279053,  5.38676427,  4.3502877 ,  6.10551742,   1.33019172, -4.01523372, -1.98294515,  0.72378299, -4.31963048])

	yt = np.array([ 1.,  1.,  1.,  1.,  1.,  1.,  2.,  1.,  1.,  1.,  1.,  2.,  2., 2.,  2.])
	
	xcv = np.array([3.68820375, -1.0672715 , 6.38518699, -1.70199415, -2.72775383])
	ycv = np.array([ 1.,  2.,  1.,  2.,  2.])
	
	Theta = []
	Theta.append(np.array([[-0.11297765, 0.0457558 ],[-0.11188263,  0.00843696]], dtype='float32'))
	Theta.append(np.array([[0.11509074,0.10543039,-0.03145336],[-0.1168719,0.05472495,-0.00337395]], dtype='float32'))
	
	nn = nnet.NeuralNetwork(np.array([1,2,2]),0.0,Theta)
	nn.InputTrainingData(np.array([xt]).T,yt)
	nn.InputCrossValidationData(np.array([xcv]).T,ycv)
	nn.GradientDescentTrain(2000,0.1)
	print(nn.GetTrainingSetAccuracy(),nn.GetCVSetAccuracy())

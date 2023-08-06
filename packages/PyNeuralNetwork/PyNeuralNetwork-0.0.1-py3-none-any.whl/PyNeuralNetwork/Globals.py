import os
import ctypes
from numpy.ctypeslib import ndpointer
from .ActivationFunctions.ReLU import ReLU,ReLUGradient
from .ActivationFunctions.LeakyReLU import LeakyReLU,InverseLeakyReLUGradient
from .ActivationFunctions.Sigmoid import Sigmoid,InverseSigmoidGradient
from .ActivationFunctions.Linear import Linear,LinearGradient
from .ActivationFunctions.Softplus import Softplus,InverseSoftplusGradient
from .ActivationFunctions.Tanh import Tanh,InverseTanhGradient

DATA_PATH = os.path.dirname(__file__)+'/__data/'

LibNN=ctypes.CDLL(DATA_PATH+'libneuralnet/libneuralnet.so')

ActFuncs = {'linear':(Linear,LinearGradient),
			'relu':(ReLU,ReLUGradient),
			'leakyrelu':(LeakyReLU,InverseLeakyReLUGradient),
			'softplus':(Softplus,InverseSoftplusGradient),
			'sigmoid':(Sigmoid,InverseSigmoidGradient),
			'tanh':(Tanh,InverseTanhGradient)}


_CppCreateNetwork = LibNN.CreateNetwork
_CppCreateNetwork.argtypes = [	ctypes.c_int,
									ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
									ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
									ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
									ndpointer(ctypes.c_float, flags="C_CONTIGUOUS")]
_CppCreateNetwork.restype = ctypes.c_int
									
_CppLoadNetwork = LibNN.LoadNetwork
_CppLoadNetwork.argtypes = [	ctypes.c_int, 
									ctypes.c_char_p]
_CppLoadNetwork.restype = ctypes.c_int

_CppSaveNetwork = LibNN.SaveNetwork
_CppSaveNetwork.argtypes = [	ctypes.c_int,
									ctypes.c_char_p]

_CppDestroyNetwork = LibNN.DestroyNetwork
_CppDestroyNetwork.argtypes = [	ctypes.c_int ]

_CppGetnSteps = LibNN.GetnSteps
_CppGetnSteps.argtypes = [	ctypes.c_int,
								ndpointer(ctypes.c_int, flags="C_CONTIGUOUS")]

_CppInputTrainingData = LibNN.InputTrainingData
_CppInputTrainingData.argtypes = [	ctypes.c_int,
										ctypes.c_int,
										ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
										ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
										ctypes.c_int,
										ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
										ctypes.c_bool]
									
_CppInputCrossValidationData = LibNN.InputCrossValidationData
_CppInputCrossValidationData.argtypes = [	ctypes.c_int,
												ctypes.c_int,
												ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
												ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
												ctypes.c_int,
												ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
												ctypes.c_bool]
									
_CppTrainGradientDescent = LibNN.TrainGradientDescent
_CppTrainGradientDescent.argtypes = [	ctypes.c_int,
											ctypes.c_int,
											ctypes.c_float,
											ctypes.c_bool]
											
_CppTrainGradientDescentSingle = LibNN.TrainGradientDescentSingle
_CppTrainGradientDescentSingle.argtypes = [	ctypes.c_int,
											ctypes.c_int,
											ctypes.c_int,
											ctypes.c_float,
											ctypes.c_bool]
										
_CppGetTrainingProgress = LibNN.GetTrainingProgress
_CppGetTrainingProgress.argtypes = [	ctypes.c_int,
											ctypes.c_int,
											ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
											ndpointer(ctypes.c_float, flags="C_CONTIGUOUS")]
										
_CppGetCrossValidationProgress = LibNN.GetCrossValidationProgress
_CppGetCrossValidationProgress.argtypes = [	ctypes.c_int,
													ctypes.c_int,
													ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
													ndpointer(ctypes.c_float, flags="C_CONTIGUOUS")]
											
_CppClassifyData = LibNN.ClassifyData
_CppClassifyData.argtypes = [	ctypes.c_int,
									ctypes.c_int,
									ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
									ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
									ctypes.c_int,
									ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
									ndpointer(ctypes.c_float, flags="C_CONTIGUOUS")]


_CppCreateEvolutionaryNetwork = LibNN.CreateEvolutionaryNetwork
_CppCreateEvolutionaryNetwork.argtypes = [	ctypes.c_int,
											ctypes.c_int,
											ctypes.c_int,
											ctypes.c_int,
											ctypes.c_int,
											ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
											ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
											ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
											ndpointer(ctypes.c_float, flags="C_CONTIGUOUS")]

_CppDestroyEvolutionaryNetwork = LibNN.DestroyEvolutionaryNetwork

_CppEvolutionaryNetworkInputData = LibNN.EvolutionaryNetworkInputData
_CppEvolutionaryNetworkInputData.argtypes = [	ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"),
												ctypes.c_int,
												ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
												ctypes.c_float]

_CppEvolutionaryNetworkEvolve = LibNN.EvolutionaryNetworkEvolve
_CppEvolutionaryNetworkEvolve.argtypes = [	ctypes.c_int,
											ctypes.c_int,
											ctypes.c_float,
											ctypes.c_float,
											ctypes.c_bool]



_CppGetL = LibNN.GetL
_CppGetL.argtypes = [ctypes.c_int,ctypes.c_int]
_CppGetL.restype = ctypes.c_int

_CppGets = LibNN.Gets
_CppGets.argtypes = [	ctypes.c_int,
						ctypes.c_int,
						ndpointer(ctypes.c_int,flags="C_CONTIGUOUS")]

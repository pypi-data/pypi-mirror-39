from . import CostFunctions
from . import ActivationFunctions
from . import PyNet
#from . import tfNet #got rid of tensorflow
from . import Autoencoder
from .NeuralNetwork import NeuralNetwork ,NeuralNetworkArray 
from .EvolutionaryNeuralNetwork import EvolutionaryNeuralNetwork,PyEvolutionaryNeuralNetwork
from .Tests import ReadCancerData,GetCancerNN
from ._CppInterface import _CreateNetwork,_DestroyNetwork,_LoadNetwork,_SaveNetwork,_InputTrainingData,_InputCrossValidationData,_TrainGradientDescent,_TrainGradientDescentSingle,_GetnSteps,_GetTrainingProgress,_GetCrossValidationProgress,_ClassifyData,_GetL,_Gets,_CreateEvolutionaryNetwork,_DestroyEvolutionaryNetwork,_EvolutionaryNetworkInputData,_EvolutionaryNetworkEvolve
from .MNIST import ReadMNISTLabels,ReadMNISTImages,GetMNISTData,ReadDigit,ReadDigits,_GetFrameRenderer,AnimateMNISTAutoencoder,MNISTAutoEncoder,MNISTClassifier
#---Custom---#"
from . import Globals
#---EndCustom---#

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <vector>
#include <cstring>
#include "network.h"
#include "evolution.h"
using namespace std;

vector<Network**> vNet;
vector<int> vNetI, vn;

NNEvolution *nnevo;

int NextInstance();
int MaxInstance();
int InstanceIndex(int ins);

extern "C" {
	int CreateNetwork(int n, int *nLayers, int *Layers, float *Lambda, float *ThetaRange);
	void DestroyNetwork(int instance);
	int LoadNetwork(int n, const char *fname);
	void SaveNetwork(int instance, const char *fname);
	void InputTrainingData(int instance, int i, int *xshape, float *xin, int ylen, int *yin, bool verb);
	void InputCrossValidationData(int instance, int i, int *xshape, float *xin, int ylen, int *yin, bool verb);
	void TrainGradientDescent(int instance, int MaxIter, float Alpha, bool verb);
	void TrainGradientDescentSingle(int instance, int i, int MaxIter, float Alpha, bool verb);
	void GetnSteps(int instance, int *nSteps);
	void GetTrainingProgress(int instance, int i, float *Jt, float *Acct);
	void GetCrossValidationProgress(int instance, int i, float *Jcv, float *Acccv);
	void ClassifyData(int instance, int i, int *xshape, float *xin, int m, int *yout, float *SMout);
	void CreateEvolutionaryNetwork(int nNetworks,int nInput, int nOutput, int nTop, int nCrap, int *nHrange, int *lwrange, float *lambdarange, float *alpharange);
	void DestroyEvolutionaryNetwork();
	void EvolutionaryNetworkInputData(float *xin, int m, int *yin, float FractionTrain);
	void EvolutionaryNetworkEvolve(int ngens, int MaxIter, float Pmutate, float MaxMutateSize, bool verb);
	int GetL(int instance, int i);
	void Gets(int instance, int i, int *s);
}

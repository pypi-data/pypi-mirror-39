#include "libneuralnet.h"

int NextInstance() {
	if (vNetI.size() == 0) {
		return 0;
	} else {
		return MaxInstance()+1;
	}
}

int MaxInstance() { 
	int i, n, mx = 0;
	n = vNetI.size();
	for (i=0;i<n;i++) {
		if (vNetI[i] > mx) {
			mx = vNetI[i];
		}
	}
	return mx;
}

int InstanceIndex(int ins) {
	int i, n;
	n = vNetI.size();
	for (i=0;i<n;i++) {
		if (vNetI[i] == ins) {
			return i;
		}
	}
	return -1;	
}


int CreateNetwork(int n, int *nLayers, int *Layers, float *Lambda, float *ThetaRange) {
	int instance, ind;
	instance = NextInstance();
	vNetI.push_back(instance);
	ind = InstanceIndex(instance);
	vn.push_back(n);	
	int i, p = 0;
	vNet.push_back(new Network*[n]);
	for (i=0;i<n;i++) {
		vNet[ind][i] = new Network(nLayers[i],&Layers[p],Lambda[i],ThetaRange[i]);
		p += nLayers[i];
	}
	return instance;
}


void DestroyNetwork(int instance) {
	int i, ind;
	ind = InstanceIndex(instance);	
	for (i=0;i<vn[ind];i++) {
		delete vNet[ind][i];
	}
	delete[] vNet[ind];
	vNetI.erase(vNetI.begin()+ind);
	vNet.erase(vNet.begin()+ind);	
	vn.erase(vn.begin()+ind);
}


int LoadNetwork(int n, const char *fname) {
	vn.push_back(n);
	int ind, i, instance;
	instance = NextInstance();
	vNetI.push_back(instance);
	vNet.push_back(new Network*[n]);
	ind = InstanceIndex(instance);
	char *s, sn[6];
	s = (char*) malloc((strlen(fname)+7)*sizeof(char));
	
	for (i=0;i<n;i++) {
		sprintf(sn,"-%02d.nn",i);
		strcpy(s,fname);
		strcat(s,sn);
		printf("Reading file %d of %d:  %s\n",i+1,n,s);
		vNet[ind][i] = new Network(s);
	}
	free(s);
	return instance;
}

void SaveNetwork(int instance, const char *fname) {
	int i, ind;
	ind = InstanceIndex(instance);
	char *s, sn[6];
	s = (char*) malloc((strlen(fname)+7)*sizeof(char));
	for (i=0;i<vn[ind];i++) {
		sprintf(sn,"-%02d.nn",i);
		strcpy(s,fname);
		strcat(s,sn);
		vNet[ind][i]->Save(s);
	}
	free(s);
}



void InputTrainingData(int instance, int i, int *xshape, float *xin, int ylen, int *yin, bool verb) {
	int ind;
	ind = InstanceIndex(instance);
	if (verb) {
		vNet[ind][i]->InputTrainingData(xshape,xin,ylen,yin);
	} else {
		vNet[ind][i]->InputTrainingDataQuiet(xshape,xin,ylen,yin);
	}
}



void InputCrossValidationData(int instance, int i, int *xshape, float *xin, int ylen, int *yin, bool verb) {
	int ind;
	ind = InstanceIndex(instance);	
	if (verb) {
		vNet[ind][i]->InputCrossValidationData(xshape,xin,ylen,yin);
	} else {
		vNet[ind][i]->InputCrossValidationDataQuiet(xshape,xin,ylen,yin);
	}	
}


void TrainGradientDescent(int instance, int MaxIter, float Alpha, bool verb) {
	int ind;
	ind = InstanceIndex(instance);
	int i;
	if (verb) {
		for (i=0;i<vn[ind];i++) {
			if (vn[ind] > 1) {
				printf("Training Network %d of %d\n",i+1,vn[ind]);
			}
			vNet[ind][i]->TrainGradientDescent(MaxIter,Alpha);
		}
	} else {
		for (i=0;i<vn[ind];i++) {
			vNet[ind][i]->TrainGradientDescentQuiet(MaxIter,Alpha);
		}
	}
	
}

void TrainGradientDescentSingle(int instance, int i, int MaxIter, float Alpha, bool verb) {
	int ind;
	ind = InstanceIndex(instance);
	if (verb) {
		if (vn[ind] > 1) {
			printf("Training Network %d of %d\n",i+1,vn[ind]);
		}
		vNet[ind][i]->TrainGradientDescent(MaxIter,Alpha);
	} else {
		vNet[ind][i]->TrainGradientDescentQuiet(MaxIter,Alpha);
	}
}

void GetnSteps(int instance, int *nSteps) {
	int ind;
	ind = InstanceIndex(instance);
	int i;
	for (i=0;i<vn[ind];i++) {
		nSteps[i] = vNet[ind][i]->GetnSteps();
	}
}

int GetL(int instance, int i) {
	int ind;
	ind = InstanceIndex(instance);
	return vNet[ind][i]->GetL();
}

void Gets(int instance, int i, int *s) {
	int ind;
	ind = InstanceIndex(instance);
	vNet[ind][i]->Gets(s);	
}

void GetTrainingProgress(int instance, int i, float *Jt, float *Acct) {
	int ind;
	ind = InstanceIndex(instance);
	vNet[ind][i]->GetTrainingAccuracy(Jt,Acct);
}

void GetCrossValidationProgress(int instance, int i, float *Jcv, float *Acccv) {
	int ind;
	ind = InstanceIndex(instance);
	int j;
	vNet[ind][i]->GetCrossValidationAccuracy(Jcv,Acccv);
}

void ClassifyData(int instance, int i, int *xshape, float *xin, int m, int *yout, float *SMout) {
	int ind;
	ind = InstanceIndex(instance);
	vNet[ind][i]->ClassifyData(xshape,xin,m,yout,SMout);
}



void CreateEvolutionaryNetwork(int nNetworks,int nInput, int nOutput, int nTop, int nCrap, int *nHrange, int *lwrange, float *lambdarange, float *alpharange) {
	SeedRandom();
	nnevo = new NNEvolution(nNetworks);
	nnevo->SetEvolutionParameters(nInput,nOutput,nTop,nCrap,nHrange,lwrange,lambdarange,alpharange);
}

void DestroyEvolutionaryNetwork() {
	delete nnevo;
}

void EvolutionaryNetworkInputData(float *xin, int m, int *yin, float FractionTrain) {
	nnevo->InputData(xin,m,yin,FractionTrain);
}

void EvolutionaryNetworkEvolve(int ngens, int MaxIter, float Pmutate, float MaxMutateSize, bool verb) {
	nnevo->Evolve(ngens,MaxIter,Pmutate,MaxMutateSize,verb);
}

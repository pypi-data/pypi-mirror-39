#ifndef __EVOLUTION_H__
#define __EVOLUTION_H__
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <vector>
#include "randomnumber.h"
#include "network.h"
#include "arraycopy.h"

using namespace std;

class NNEvolution {
	public:
		NNEvolution(int);
		~NNEvolution();
		void SetEvolutionParameters(int,int,int,int,int*,int*,float*,float*);
		void CreateRandomNetworks();
		void RecreateNetworks();
		void InputData(float*,int,int*,float);
		void FillData(bool);
		void TrainNetworks(int,bool);
		void SortAccuracy();
		void EvolveStep(int,float,float,bool);
		void Evolve(int,int,float,float,bool);
		void BreedNetworks();
		void KillNetworks();
		void MutateNetworks(float,float);
		
		int N, nGens;
		
		
		
	private:
		float *Accuracy;
		vector<Network*> nets;
		int Ntop, Ncrap, Nkeep, nIn, nOut;
		int nHrnge[2], lwrnge[2];
		float alpharnge[2], lambdarnge[2];
		float *GenAlpha, *GenAccuracy, *GenLambda, BestAlpha, BestLambda;	
		int mt, mcv;
		float *Xt, *Xcv;
		int *yt, *ycv, xtshape[2], xcvshape[2];
		bool HasData, ParamsSet;
		int *GenOrder, *GenL, **Gens, nKeep, *KeepInds, BestL, *Bests;
		bool *GenKeep;
};

#endif

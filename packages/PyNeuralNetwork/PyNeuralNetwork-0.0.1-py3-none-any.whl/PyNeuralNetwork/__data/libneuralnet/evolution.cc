#include "evolution.h"

/*
 * EXPERIMENTAL!
 * 
 * Things we will vary:
 * 	- Number of hidden layers (nH between nHmin and nHmax)
 * 	- Hidden Layer width (lw between lwmin and lwmax)
 * 	- Regularization parameter (lambda between lambdamin and lambdamax)
 * 	- Learning rate (alpha between alpha min and alpha max)
 * 
 * There are nN networks
 * 
 * Step 1:
 *		Initialize N networks randomly
 * Step 2:
 * 		Train them upto MaxIter iterations
 * Step 3:
 *  	Sort by CV accuracy
 * Step 4:
 * 		Keep Ntop of the best performing networks and Ncrap of the others
 * Step 5:
 * 		Perform random mutations on some parameters of some networks with some probability Pmutate
 * Step 6:
 * 		After Keeping Ntop and Ncrap networks, there are N-(Ntop+Ncrap) left to fill by breeding random pairs of the remainers
 * 
 * 
 * 
 */

NNEvolution::NNEvolution(int nNetworks) {
	
	N = nNetworks;
	nGens = 0;
	HasData = false;
	GenAccuracy = (float*) malloc(N*sizeof(float));
	GenAlpha = (float*) malloc(N*sizeof(float));
	GenLambda = (float*) malloc(N*sizeof(float));
	GenL = (int*) malloc(N*sizeof(int));
	Gens = (int**) malloc(N*sizeof(int*));
	GenOrder = (int*) malloc(N*sizeof(int));
	GenKeep = (bool*) malloc(N*sizeof(bool));
	Bests = NULL;
	ParamsSet = false;

}

NNEvolution::~NNEvolution() {
	int i;
	if (ParamsSet) {
		for (i=0;i<N;i++) {
			delete nets[i];
		}
		free(KeepInds);
	}
	free(GenAccuracy);
	free(GenOrder);
	free(GenKeep);
	free(GenAlpha);
	free(GenLambda);
	free(GenL);
	for (i=0;i<N;i++) {
		free(Gens[i]);
	}
	free(Gens);
	
	if (HasData) {
		free(Xt);
		free(Xcv);
		free(yt);
		free(ycv);
	}
	if (nGens > 0) {
		free(Accuracy);
	}
}

void NNEvolution::SetEvolutionParameters(int nInput, int nOutput, int nTop, int nCrap, int *nHrange, int *lwrange, float *lambdarange, float *alpharange) {
	nIn = nInput;
	nOut = nOutput;
	Ntop = nTop;
	Ncrap = nCrap;
	Nkeep = Ntop + Ncrap;
	KeepInds = (int*) malloc(Nkeep*sizeof(int));
	
	
	ArrayCopy(nHrange,nHrnge,2);
	ArrayCopy(lwrange,lwrnge,2);
	ArrayCopy(lambdarange,lambdarnge,2);
	ArrayCopy(alpharange,alpharnge,2);
	
	
	CreateRandomNetworks();
	ParamsSet = true;
	
	int i, j;
	for (i=0;i<N;i++) {
		printf("Network %d: Alpha = %f, Lambda = %f, L = %d, S = ",i,GenAlpha[i],GenLambda[i],GenL[i]);
		for (j=0;j<GenL[i];j++) {
			printf("%d,",Gens[i][j]);
		}
		printf("\n");
	}
}

void NNEvolution::CreateRandomNetworks() {
	int i, ind, nH, lambda;
	for (ind=0;ind<N;ind++) {
		nH = RandomNumber(nHrnge);
		GenL[ind] = nH+2;
		Gens[ind] = (int*) malloc(GenL[ind]*sizeof(int));
		Gens[ind][0] = nIn;
		Gens[ind][GenL[ind]-1]= nOut;
		for (i=1;i<GenL[ind]-1;i++) {
			Gens[ind][i] = RandomNumber(lwrnge);
		}
		GenLambda[ind] = RandomLogRange(lambdarnge);
		nets.push_back(new Network(GenL[ind],Gens[ind],GenLambda[ind],0.12));
		GenAlpha[ind] = RandomLogRange(alpharnge);
	}
}


void NNEvolution::InputData(float *xin, int m, int *yin, float FractionTrain) {
	mt = (int) (((float) m) *FractionTrain);
	mcv = m - mt;
	xtshape[0] = mt;
	xtshape[1] = nIn;
	xcvshape[0] = mcv;
	xcvshape[1] = nIn;
	//printf("mt: %d mcv: %d \n",mt,mcv);
	int i, offset;
	Xt = (float*) malloc(mt*nIn*sizeof(float)); 
	yt = (int*) malloc(mt*sizeof(int)); 
	Xcv = (float*) malloc(mcv*nIn*sizeof(float)); 
	ycv = (int*) malloc(mcv*sizeof(int)); 
	for (i=0;i<mt*nIn;i++) {
		Xt[i] = xin[i];
	}
	for (i=0;i<mt;i++) {
		yt[i] = yin[i];
	}
	offset = mt*nIn;
	for (i=0;i<mcv*nIn;i++) {
		Xcv[i] = xin[i+offset];
	}
	for (i=0;i<mcv;i++) {
		ycv[i] = yin[i+mt];
	}
	HasData = true;
}


void NNEvolution::FillData(bool verb) {
	int i;
	for (i=0;i<N;i++) {
		if (verb) {
			nets[i]->InputTrainingData(xtshape,Xt,mt,yt);
			nets[i]->InputCrossValidationData(xcvshape,Xcv,mcv,ycv);
		} else {
			nets[i]->InputTrainingDataQuiet(xtshape,Xt,mt,yt);
			nets[i]->InputCrossValidationDataQuiet(xcvshape,Xcv,mcv,ycv);	
		}	
	}
	
}

void NNEvolution::TrainNetworks(int MaxIter, bool verb) {
	int i;
	for (i=0;i<N;i++) {
		if (verb) {
			printf("Training network %d of %d\n",i+1,N);
			printf("%f\n",GenAlpha[i]);
			nets[i]->TrainGradientDescent(MaxIter,GenAlpha[i]);
		} else {
			nets[i]->TrainGradientDescentQuiet(MaxIter,GenAlpha[i]);
		}
	}
}

void NNEvolution::SortAccuracy() {
	int i, nSteps;
	float Jcv,Acv;
	for (i=0;i<N;i++) {
		nets[i]->GetLastCrossValidationAccuracy(&Jcv,&Acv);
		GenAccuracy[i] = Acv;
		GenOrder[i] = i;
	}
	bool swapped = true;
	int tmp;
	int n = N;
	while (swapped) {
		swapped = false;
		for (i=1;i<n;i++) {
			if (GenAccuracy[GenOrder[i-1]] < GenAccuracy[GenOrder[i]]) {
				tmp = GenOrder[i];
				GenOrder[i] = GenOrder[i-1];
				GenOrder[i-1] = tmp;
				swapped = true;
			}
		}
		n--;
	}
	for (i=0;i<Ntop;i++) { 
		GenKeep[GenOrder[i]] = true;
	}
	for (i=Ntop;i<N;i++) {
		GenKeep[GenOrder[i]] = false;
	}
	int bad = 0;
	while (bad < Ncrap) {
		tmp = GenOrder[RandomNumber(Ntop,N-1)];
		GenKeep[tmp] = true;
		bad++;
	}
	int p = 0;
	for (i=0;i<N;i++) {
		if (GenKeep[i]) { 
			KeepInds[p] = i;
			p++;
		}
	}
	BestAlpha = GenAlpha[GenOrder[0]];
	BestLambda = GenLambda[GenOrder[0]];
	BestL = GenL[GenOrder[0]];
	if (Bests == NULL) {
		Bests = (int*) malloc(BestL*sizeof(int));
	} else {
		Bests = (int*) realloc(Bests,BestL*sizeof(int));
	}
	for (i=0;i<BestL;i++) {
		Bests[i] = Gens[GenOrder[0]][i];
	}
}

void NNEvolution::KillNetworks() {
	int i;
	for (i=0;i<N;i++) {
		//printf("Netowrk pointer %p\n",&nets[i]);
		//printf("i: %d, N: %d\n",i,N);
		delete nets[i];
		//printf("i: %d, N: %d\n",i,N);
	}
}

void NNEvolution::BreedNetworks() {
	int i, parent[2], j, ind, *parentinds, nparent[2];
	int parentrange[] = {0,Nkeep-1}, yesno[] = {0,1};
	for (i=0;i<N;i++){
		
		if (not GenKeep[i]) {
			//printf("child: %d\n" ,i);
			//if this network is one to be removed then pick it
			//pick both parents randomly
			parent[0] = RandomNumber(parentrange);
			parent[1] = RandomNumber(parentrange);
			while (parent[0] == parent[1]) {
				parent[1] = RandomNumber(parentrange);
			}
			parent[0] = KeepInds[parent[0]];
			parent[1] = KeepInds[parent[1]];
			
			nparent[0] = 1;
			nparent[1] = 1;
			
			printf("parents: %d %d\n",parent[0],parent[1]);
			
			parentinds = new int[3];
			for (j=0;j<3;j++) {
				ind = 0;
				while (ind == 0) {
					ind = RandomNumber(-nparent[1],nparent[0]);
				}
				if (ind > 0) {
					parentinds[j] = 1;
					nparent[1]++;
				} else {
					parentinds[j] = 0;
					nparent[0]++;
				}
				printf("Property parent ind: %d\n",parentinds[j]);
			}
				
			GenAlpha[i] = GenAlpha[parent[parentinds[0]]];
			GenLambda[i] = GenLambda[parent[parentinds[1]]];
			GenL[i] = GenL[parent[parentinds[2]]];
			delete parentinds;
			
			
			//select s from parents in loop
			parentinds = new int[GenL[i]-2];
			nparent[0] = 1;
			nparent[1] = 1;
			Gens[i] = (int*) realloc(Gens[i],GenL[i]*sizeof(int));
			Gens[i][0] = nIn;
			Gens[i][GenL[i]-1] = nOut;
			for (j=0;j<GenL[i]-2;j++) {
				ind = 0;
				while (ind == 0) {
					ind = RandomNumber(-nparent[1],nparent[0]);
				}
				if (ind > 0) {
					ind = parent[1];
					nparent[1]++;
				} else {
					ind = parent[0];
					nparent[0]++;
				}
				printf("ind: %d\n",ind);
				Gens[i][j+1] = Gens[ind][(j % (GenL[ind]-2))+1];
			}
			delete parentinds;
		}
	}
}

void NNEvolution::MutateNetworks(float Pmutate, float MaxMutateSize) {
	int i, j, jrange[] = {0,3}, newL, l, lrange[] = {1,1};
	float mrange[] = {0.0,1.0}, pmrange[] = {-1.0,1.0};
	for (i=0;i<N;i++) {
		if (RandomNumber(mrange) < Pmutate) {
			//pick a property to mutate
			j = RandomNumber(jrange);
			if (j == 0) {
				//mutate Alpha
				GenAlpha[i] = GenAlpha[i] + RandomNumber(pmrange)*MaxMutateSize*GenAlpha[i];	
				if (GenAlpha[i] > alpharnge[1]) {
					GenAlpha[i] = alpharnge[1];
				}
				if (GenAlpha[i] < alpharnge[0]) {
					GenAlpha[i] = alpharnge[0];
				}		
			} else if (j == 1) {
				//mutate Lambda
				GenLambda[i] = GenLambda[i] + RandomNumber(pmrange)*MaxMutateSize*GenLambda[i];
				if (GenLambda[i] > lambdarnge[1]) {
					GenLambda[i] = lambdarnge[1];
				}
				if (GenLambda[i] < lambdarnge[0]) {
					GenLambda[i] = lambdarnge[0];
				}	
			} else if (j == 2) {
				//mutate L by adding or subtracting a layer
				newL = GenL[i] + ((int) round(RandomNumber(pmrange)));
				if (newL != GenL[i]) {
					
					Gens[i] = (int*) realloc(Gens[i],newL*sizeof(int));
					Gens[i][newL-1] = nOut;
					if (newL > GenL[i]) {
						Gens[i][newL-2] = Gens[i][newL-3];
					}
					GenL[i] = newL;
				}
			} else if (j == 3) {
				//mutate a random layer by adding or subtracting a small number of nodes
				if (GenL[i] == 3) {
					l = 1;
				} else { 
					lrange[1] = GenL[i]-2;
					l = RandomNumber(lrange);
				}
				Gens[i][l] = Gens[i][l] + (int) round(RandomNumber(pmrange)*MaxMutateSize*((float) Gens[i][l]));
			}
		}
	}
	
	
}

void NNEvolution::RecreateNetworks() {
	int i, j;
	for (i=0;i<N;i++) {
		nets[i] = new Network(GenL[i],Gens[i],GenLambda[i],0.12);
	}
	for (i=0;i<N;i++) {
		printf("Network %d: Alpha = %f, Lambda = %f, L = %d, S = ",i,GenAlpha[i],GenLambda[i],GenL[i]);
		for (j=0;j<GenL[i];j++) {
			printf("%d,",Gens[i][j]);
		}
		printf("\n");
	}
}


void NNEvolution::EvolveStep(int MaxIter, float Pmutate, float MaxMutateSize, bool verb) {
	if (verb) {
		printf("Filling networks with data\n");
	}
	FillData(verb);
	if (verb) {
		printf("Training networks\n");
	}
	TrainNetworks(MaxIter,verb);
	if (verb) {
		printf("Sorting by accuracy\n");
	}
	SortAccuracy();
	if (verb) {
		printf("Breeding networks\n");
	}
	BreedNetworks();
	if (verb) {
		printf("Mutating networks\n");
	}
	MutateNetworks(Pmutate,MaxMutateSize);
	if (verb) {
		printf("killing networks\n");
	}
	KillNetworks();
	if (verb) {
		printf("Recreating networks\n");
	}
	RecreateNetworks();	
}

void NNEvolution::Evolve(int ngens, int MaxIter, float Pmutate, float MaxMutateSize, bool verb) {
	nGens += ngens;
	if (nGens == ngens) {
		Accuracy = (float*) malloc(N*nGens*sizeof(float));
	} else {
		Accuracy = (float*) realloc(Accuracy,N*nGens*sizeof(float));
	}
	float BestAcc;
	int i, j;
	for (i=nGens-ngens;i<nGens;i++) {
		printf("Evolving Step %d of %d\n",i+1,nGens);
		EvolveStep(MaxIter,Pmutate,MaxMutateSize,verb);
		for (j=0;j<N;j++) {
			Accuracy[i*N + j] = GenAccuracy[j];
		}
		BestAcc = 0.0;
		for (j=0;j<N;j++) {
			if (GenAccuracy[j] > BestAcc) {
				BestAcc = GenAccuracy[j];
			}
		}
		printf("Best Accuracy: %6.2f \n",BestAcc);
	}
}
	


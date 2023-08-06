#include "network.h"
//This constructor will be used to initialize the network
Network::Network(int nLayers, int *Layers, float Lambda, float ThetaRange) {
	int i;
	//So here we need to get the initial dimensions of the matrices 
	L = nLayers;
	s = new int[L];
	nT = L - 1;
	na = L;
	nz = L -1;
	Tdims = new int[2*nT];
	adims = new int[2*na];
	zdims = new int[2*nz];
	ddims = new int[2*na];
	//assign dimensions to theta
	for (i=0;i<L;i++) {
		s[i] = Layers[i];
		//printf("%d \n",s[i]);
	}
	for (i=0;i<L-1;i++) {
		Tdims[i*2] = s[i + 1];
		Tdims[i*2+1] = s[i] + 1;
		//printf("%d %d\n",s[i+1],s[i]+1);
	}
	lambda = Lambda;
	range = ThetaRange;
	//create and randomly initialize Theta
	Theta = new MatrixArray(nT,Tdims);	
	dTheta = new MatrixArray(nT,Tdims);
	Theta->RandomInit(range);
	
	
	//create empty cost and accuracy arrays
	nJ = 10000;
	Jt = (float*) malloc(nJ*sizeof(float));
	Jcv = (float*) malloc(nJ*sizeof(float));
	Acct = (float*) malloc(nJ*sizeof(float));
	Acccv = (float*) malloc(nJ*sizeof(float));
	
	nSteps = 0;
	TData = false;
	CVData = false;
	Trained = false;
	mt = 0;
	mcv = 0;
}

Network::Network(const char *fname) {
	FILE *f;
	int Xshape[2];
	int i;
	f = fopen(fname,"rb");
	fread(&Trained,sizeof(bool),1,f);
	fread(&L,sizeof(int),1,f);
	s = new int[L];
	fread(s,sizeof(int),L,f);
	fread(&lambda,sizeof(float),1,f);
	fread(&range,sizeof(float),1,f);
	fread(&mt,sizeof(int),1,f);
	fread(&mcv,sizeof(int),1,f);
	nT = L - 1;
	na = L;
	nz = L - 1;
	Tdims = new int[2*nT];
	adims = new int[2*na];
	zdims = new int[2*nz];
	ddims = new int[2*na];
	TData = false;
	CVData = false;
	if (mt > 0) {
		TData = true;
		Xshape[0] = mt;
		Xshape[1] = s[0]+1;
		Xt = new Matrix(Xshape);
		fread(Xt->data,sizeof(float),Xt->len,f);
		yt = new int[mt];
		fread(yt,sizeof(int),mt,f);
		for (i=0;i<L;i++) {
			ddims[i*2] = mt;
			ddims[i*2 + 1] = s[i];
			if (i > 0) { 
				zdims[i*2 - 2] = mt;
				zdims[i*2 - 1] = s[i];	
			}
			if (i== L-1) {
				adims[i*2] = mt;
				adims[i*2 + 1] = s[i];

			} else {
				adims[i*2] = mt;
				adims[i*2 + 1] = s[i] + 1;
			}
		}
		
		at = new MatrixArray(L,adims);
		zt = new MatrixArray(L-1,zdims);
		delta = new MatrixArray(L,ddims);
		
		at->matrix[0]->FillMatrix(Xt->data);
	}
	if (mcv > 0) {
		CVData = true;
		Xshape[0] = mcv;
		Xshape[1] = s[0]+1;
		Xcv = new Matrix(Xshape);
		fread(Xcv->data,sizeof(float),Xcv->len,f);
		ycv = new int[mcv];
		fread(ycv,sizeof(int),mcv,f);
		int adimscv[L*2], zdimscv[(L-1)*2];
		for (i=0;i<L;i++) {
			if (i > 0) { 
				zdimscv[i*2 - 2] = mcv;
				zdimscv[i*2 - 1] = s[i];	
			}
			if (i== L-1) {
				adimscv[i*2] = mcv;
				adimscv[i*2 + 1] = s[i];

			} else {
				adimscv[i*2] = mcv;
				adimscv[i*2 + 1] = s[i] + 1;
			}
		}
		
		acv = new MatrixArray(L,adimscv);
		zcv = new MatrixArray(L-1,zdimscv);
		acv->matrix[0]->FillMatrix(Xcv->data);		
	}
	

	for (i=0;i<L-1;i++) {
		Tdims[i*2] = s[i + 1];
		Tdims[i*2+1] = s[i] + 1;
	}
	Theta = new MatrixArray(nT,Tdims);	
	dTheta = new MatrixArray(nT,Tdims);
	for (i=0;i<L-1;i++) {
		fread(Theta->matrix[i]->data,sizeof(float),Theta->matrix[i]->len,f);
	}
	fread(&nSteps,sizeof(int),1,f);
	fread(&nJ,sizeof(int),1,f);
	
	Jt = (float*) malloc(nJ*sizeof(float));
	Jcv = (float*) malloc(nJ*sizeof(float));
	Acct = (float*) malloc(nJ*sizeof(float));
	Acccv = (float*) malloc(nJ*sizeof(float));
	
	fread(Jt,sizeof(float),nJ,f);
	fread(Jcv,sizeof(float),nJ,f);
	fread(Acct,sizeof(float),nJ,f);
	fread(Acccv,sizeof(float),nJ,f);
	fclose(f);
}

//copy constructor
Network::Network(const Network &obj) {
	printf("calling copy constructor \n");
}

//destructor
Network::~Network() {
	delete[] s;
	delete[] Tdims;
	delete[] adims;
	delete[] zdims;
	delete[] ddims;
	free(Jt);
	free(Jcv);
	free(Acct);
	free(Acccv);
	delete Theta;
	delete dTheta;
	if (TData) {
		delete[] yt;
		delete Xt;
		delete at;
		delete zt;
		delete delta;
	}
	if (CVData) {
		delete[] ycv;
		delete Xcv;
		delete acv;
		delete zcv;
	}
}

//Self explanatory - input training data to network
void Network::InputTrainingData(int *xshape, float *xin, int ylen, int *yin){
	int i, j;
	//printf("S = [");
	//for (i=0;i<L;i++) {
	//	printf(" %d,",s[i]);
	//}
	//printf("]\n");
	if (xshape[1] != s[0]) {
		printf("X needs to have the dimensions (m,s1), where m is the number of training samples and s1 is equal to the number of units in the input layer of the network\n");
		return;
	}
	if (ylen != xshape[0]) {
		printf("y must have the dimensions (m,), where m is the number of training samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs\n");
		return;
	}	
	//printf("T1\n");
	mt = ylen;
	int Xshape[] = {mt,s[0]+1};
	Xt = new Matrix(Xshape);
	Xt->FillWithBias(xin);
	yt = new int[mt];
	

	//printf("T2\n");
	for (i=0;i<mt;i++) {
		yt[i] = yin[i];
	}
/*	for (i=0;i<10;i++) {
		for (j=0;j<s[0]+1;j++) {
			printf("%f ",Xt->Get(i,j));
		}
		printf(": %d\n",yt[i]);
	}*/
	TData = true;
	//printf("T3\n");
	//create at and zt
	for (i=0;i<L;i++) {
		//printf("T3.1\n");
		ddims[i*2] = mt;
		//printf("T3.15\n");
		ddims[i*2 + 1] = s[i];
		//printf("T3.2\n");
		if (i > 0) { 
			//printf("T3.2.1\n");
			zdims[i*2 - 2] = mt;
			zdims[i*2 - 1] = s[i];	
		}
		//printf("T3.3\n");
		if (i== L-1) {
			//printf("T3.3.1\n");
			adims[i*2] = mt;
			adims[i*2 + 1] = s[i];

		} else {
			//printf("T3.3.2\n");
			adims[i*2] = mt;
			adims[i*2 + 1] = s[i] + 1;
		}
	}
/*	printf("T4 %d\n",L);
	printf("adims: ");
	for (i=0;i<L*2;i++) {
		printf(" %d",adims[i]);
	}
	printf("\n");
	printf("zdims: ");
	for (i=0;i<(L-1)*2;i++) {
		printf(" %d",zdims[i]);
	}
	printf("\n");
	printf("ddims: ");
	for (i=0;i<L*2;i++) {
		printf(" %d",ddims[i]);
	}
	printf("\n");*/
	at = new MatrixArray(L,adims);
	//printf("T4.1 %d\n",L);
	zt = new MatrixArray(L-1,zdims);
	//printf("T4.2 %d\n",L);
	delta = new MatrixArray(L,ddims);
	//printf("T5\n");
	at->matrix[0]->FillMatrix(Xt->data);
	//printf("T6\n");
	
	Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
	//printf("T7\n");
	Acct[nSteps] = GetTrainingAccuracy();
	//printf("T8\n");
	printf("Initial Cost: %f, Accuracy: %f %% \n",Jt[0], Acct[0]);
	ThetaGradient(*Theta,*at,*delta,yt,L,s,lambda,*dTheta);
	//printf("T9\n");
}

void Network::InputTrainingDataQuiet(int *xshape, float *xin, int ylen, int *yin){
	if (xshape[1] != s[0]) {
		printf("X needs to have the dimensions (m,s1), where m is the number of training samples and s1 is equal to the number of units in the input layer of the network\n");
		return;
	}
	if (ylen != xshape[0]) {
		printf("y must have the dimensions (m,), where m is the number of training samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs\n");
		return;
	}	
	mt = ylen;
	int Xshape[] = {mt,s[0]+1};
	Xt = new Matrix(Xshape);
	Xt->FillWithBias(xin);
	yt = new int[mt];
	int i;
	for (i=0;i<mt;i++) {
		yt[i] = yin[i];
	}
	TData = true;
	
	//create at and zt
	for (i=0;i<L;i++) {
		ddims[i*2] = mt;
		ddims[i*2 + 1] = s[i];
		if (i > 0) { 
			zdims[i*2 - 2] = mt;
			zdims[i*2 - 1] = s[i];	
		}
		if (i== L-1) {
			adims[i*2] = mt;
			adims[i*2 + 1] = s[i];

		} else {
			adims[i*2] = mt;
			adims[i*2 + 1] = s[i] + 1;
		}
	}
	
	at = new MatrixArray(L,adims);
	zt = new MatrixArray(L-1,zdims);
	delta = new MatrixArray(L,ddims);
	
	at->matrix[0]->FillMatrix(Xt->data);
	
	
	Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
	Acct[nSteps] = GetTrainingAccuracy();

	ThetaGradient(*Theta,*at,*delta,yt,L,s,lambda,*dTheta);

}

//optionally input cross validation data
void Network::InputCrossValidationData(int *xshape, float *xin, int ylen, int *yin) {
	if (xshape[1] != s[0]) {
		printf("X needs to have the dimensions (m,s1), where m is the number of CV samples and s1 is equal to the number of units in the input layer of the network\n");
		return;
	}
	if (ylen != xshape[0]) {
		printf("y must have the dimensions (m,), where m is the number of CV samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs\n");
		return;
	}	
	mcv = ylen;
	int Xshape[] = {mcv,s[0]+1};
	Xcv = new Matrix(Xshape);
	Xcv->FillWithBias(xin);
	ycv = new int[mcv];
	int i;
	for (i=0;i<mcv;i++) {
		ycv[i] = yin[i];
	}
	CVData = true;
	int adimscv[L*2], zdimscv[(L-1)*2];
	//create acv and zcv
	for (i=0;i<L;i++) {
		if (i > 0) { 
			zdimscv[i*2 - 2] = mcv;
			zdimscv[i*2 - 1] = s[i];	
		}
		if (i== L-1) {
			adimscv[i*2] = mcv;
			adimscv[i*2 + 1] = s[i];

		} else {
			adimscv[i*2] = mcv;
			adimscv[i*2 + 1] = s[i] + 1;
		}
	}
	acv = new MatrixArray(L,adimscv);
	zcv = new MatrixArray(L-1,zdimscv);
	acv->matrix[0]->FillMatrix(Xcv->data);
	Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
	Acccv[nSteps] = GetCrossValidationAccuracy();
	printf("Initial Cross Validation Cost: %f, Accuracy: %f %% \n",Jcv[0], Acccv[0]);
}


void Network::InputCrossValidationDataQuiet(int *xshape, float *xin, int ylen, int *yin) {
	if (xshape[1] != s[0]) {
		printf("X needs to have the dimensions (m,s1), where m is the number of CV samples and s1 is equal to the number of units in the input layer of the network\n");
		return;
	}
	if (ylen != xshape[0]) {
		printf("y must have the dimensions (m,), where m is the number of CV samples, and the value stored in yin should represent the output unit index or (m,k) where k is the number of outputs\n");
		return;
	}	
	mcv = ylen;
	int Xshape[] = {mcv,s[0]+1};
	Xcv = new Matrix(Xshape);
	Xcv->FillWithBias(xin);
	ycv = new int[mcv];
	int i;
	for (i=0;i<mcv;i++) {
		ycv[i] = yin[i];
	}
	CVData = true;
	int adimscv[L*2], zdimscv[(L-1)*2];
	//create acv and zcv
	for (i=0;i<L;i++) {
		if (i > 0) { 
			zdimscv[i*2 - 2] = mcv;
			zdimscv[i*2 - 1] = s[i];	
		}
		if (i== L-1) {
			adimscv[i*2] = mcv;
			adimscv[i*2 + 1] = s[i];

		} else {
			adimscv[i*2] = mcv;
			adimscv[i*2 + 1] = s[i] + 1;
		}
	}
	
	acv = new MatrixArray(L,adimscv);
	zcv = new MatrixArray(L-1,zdimscv);
	
	acv->matrix[0]->FillMatrix(Xcv->data);
	
	Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
	Acccv[nSteps] = GetCrossValidationAccuracy();
	
}

//this will train the network using either gradient-descent or conjugate-gradient minimization
void Network::Train() {
	
}

//gradient-descent
void Network::TrainGradientDescent(int MaxIter, float Alpha) {
	int i;
	for (i=0;i<MaxIter-1;i++) {
		Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
		Acct[nSteps] = GetTrainingAccuracy();
		if (CVData) {
			Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
			Acccv[nSteps] = GetCrossValidationAccuracy();			
			printf("\rI: %8d - Cost: %7e - T Acc: %6.2f - CV Cost: %7e - CV Acc: %6.2f",nSteps+1,Jt[nSteps],Acct[nSteps],Jcv[nSteps],Acccv[nSteps]);
		} else {
			printf("\rI: %8d - Cost: %10e - T Acc: %6.2f",nSteps+1,Jt[nSteps],Acct[nSteps]);
		}

		ThetaGradient(*Theta,*at,*delta,yt,L,s,lambda,*dTheta);
		UpdateTheta(*Theta,*dTheta,Alpha);
		nSteps++;
		if (nSteps >= nJ) {
			ExtendArrays();
		}
		if (isnan(Jt[nSteps-1]) || isinf(Jt[nSteps-1])) {
			printf("Cost function is NaN\n");
			break;
		}
	}
	Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
	Acct[nSteps] = GetTrainingAccuracy();
	if (CVData) {
		Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
		Acccv[nSteps] = GetCrossValidationAccuracy();			
		printf("\rI: %8d - Cost: %7e - T Acc: %6.2f - CV Cost: %10e - CV Acc: %6.2f\n",nSteps+1,Jt[nSteps],Acct[nSteps],Jcv[nSteps],Acccv[nSteps]);
	} else {
		printf("\rI: %8d - Cost: %7e - T Acc: %6.2f\n",nSteps+1,Jt[nSteps],Acct[nSteps]);
	}	
	nSteps++;
	Trained = true;
}

void Network::TrainGradientDescentQuiet(int MaxIter, float Alpha) {
	int i;
	for (i=0;i<MaxIter-1;i++) {
		Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
		Acct[nSteps] = GetTrainingAccuracy();
		if (CVData) {
			Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
			Acccv[nSteps] = GetCrossValidationAccuracy();			
		}

		ThetaGradient(*Theta,*at,*delta,yt,L,s,lambda,*dTheta);
		UpdateTheta(*Theta,*dTheta,Alpha);
		nSteps++;
		if (nSteps >= nJ) {
			ExtendArrays();
		}
		if (isnan(Jt[nSteps-1]) || isinf(Jt[nSteps-1])) {
			printf("\nCost function is NaN\n");
			break;
		}
	}
	Jt[nSteps] = CostFunction(*Theta,*at,*zt,yt,L,s,lambda);
	Acct[nSteps] = GetTrainingAccuracy();
	if (CVData) {
		Jcv[nSteps] = CostFunction(*Theta,*acv,*zcv,ycv,L,s,lambda);
		Acccv[nSteps] = GetCrossValidationAccuracy();			
	}
	nSteps++;
	Trained = true;
}



//conjugate-gradient
void Network::TrainConjugateGradient() {
	
}

//this will calculate how accurately the network classifies the training
//set, where variable at is always updated after being passed to CostFunction
float Network::GetTrainingAccuracy() {
	int yp[mt];
	int i, good = 0;
	Predict(*at->matrix[L-1],yp);
	for (i=0;i<mt;i++) {
		good += (int) (yp[i] == yt[i]);
	}
	return ((float) good)/((float) mt)*100.0;
}

//as above, but for the CV set
float Network::GetCrossValidationAccuracy() {
	int yp[mcv];
	int i, good = 0;
	Predict(*acv->matrix[L-1],yp);
	for (i=0;i<mcv;i++) {
		good += (int) (yp[i] == ycv[i]);
	}
	return ((float) good)/((float) mcv)*100.0;	
}

//this will forward propagate input data through the network and either 
//classifiy it definitively, or provide probabilities using the softmax function
void Network::ClassifyData(int *xshape, float *xin, int m, int *yout) {
	Matrix *Xtest;
	int i, Xshape[] = {m,s[0]+1}, zdimstest[(L-1)*2], adimstest[L*2];
	Xtest = new Matrix(Xshape);
	Xtest->FillWithBias(xin);
	for (i=0;i<L;i++) {
		if (i > 0) { 
			zdimstest[i*2 - 2] = m;
			zdimstest[i*2 - 1] = s[i];	
		}
		if (i== L-1) {
			adimstest[i*2] = m;
			adimstest[i*2 + 1] = s[i];

		} else {
			adimstest[i*2] = m;
			adimstest[i*2 + 1] = s[i] + 1;
		}
	}
	
	atest = new MatrixArray(L,adimstest);
	ztest = new MatrixArray(L-1,zdimstest);
	
	atest->matrix[0]->FillMatrix(Xtest->data);	
	Propagate(*atest,*ztest,*Theta,L);
	Predict(*atest->matrix[L-1],yout);
	
	delete atest;
	delete ztest;
	delete Xtest;
}



void Network::ClassifyData(int *xshape, float *xin, int m, int *yout, float *SMout) {
	Matrix *Xtest;
	int i, Xshape[] = {m,s[0]+1}, zdimstest[(L-1)*2], adimstest[L*2];
	Xtest = new Matrix(Xshape);
	Xtest->FillWithBias(xin);
	for (i=0;i<L;i++) {
		if (i > 0) { 
			zdimstest[i*2 - 2] = m;
			zdimstest[i*2 - 1] = s[i];	
		}
		if (i== L-1) {
			adimstest[i*2] = m;
			adimstest[i*2 + 1] = s[i];

		} else {
			adimstest[i*2] = m;
			adimstest[i*2 + 1] = s[i] + 1;
		}
	}
	
	atest = new MatrixArray(L,adimstest);
	ztest = new MatrixArray(L-1,zdimstest);
	
	atest->matrix[0]->FillMatrix(Xtest->data);	
	Propagate(*atest,*ztest,*Theta,L);
	Predict(*atest->matrix[L-1], yout);
	
	int K = s[L-1];
	int smshape[] = {m,K};
	Matrix SM(smshape);
	
	PredictProbs(*ztest->matrix[L-2],SM);
	
	for (i=0;i<SM.len;i++) {
		SMout[i] = SM.data[i];
	}
	
	delete atest;
	delete ztest;
	delete Xtest;
}

void Network::ExtendArrays() {
	nJ += 10000;
	Jt = (float*) realloc(Jt,nJ*sizeof(float));
	Jcv = (float*) realloc(Jcv,nJ*sizeof(float));
	Acct = (float*) realloc(Acct,nJ*sizeof(float));
	Acccv = (float*) realloc(Acccv,nJ*sizeof(float));	
}

void Network::Save(const char *fname) {
	int i;
	FILE *f;
	f = fopen(fname,"wb");
	fwrite(&Trained,sizeof(bool),1,f);
	fwrite(&L,sizeof(int),1,f);
	fwrite(s,sizeof(int),L,f);
	fwrite(&lambda,sizeof(float),1,f);
	fwrite(&range,sizeof(float),1,f);
	fwrite(&mt,sizeof(int),1,f);
	fwrite(&mcv,sizeof(int),1,f);	
	
	if (TData) {
		fwrite(Xt->data,sizeof(float),Xt->len,f);
		fwrite(yt,sizeof(int),mt,f);
	}
	if (CVData) {
		fwrite(Xcv->data,sizeof(float),Xcv->len,f);
		fwrite(ycv,sizeof(int),mcv,f);
	}
	for (i=0;i<L-1;i++) {
		fwrite(Theta->matrix[i]->data,sizeof(float),Theta->matrix[i]->len,f);
	}
	fwrite(&nSteps,sizeof(int),1,f);
	fwrite(&nJ,sizeof(int),1,f);	
	fwrite(Jt,sizeof(float),nJ,f);
	fwrite(Jcv,sizeof(float),nJ,f);
	fwrite(Acct,sizeof(float),nJ,f);
	fwrite(Acccv,sizeof(float),nJ,f);
	fclose(f);
}

int Network::GetnSteps() {
	return nSteps;
}

void Network::GetTrainingAccuracy(float *Jtout, float *Actout) {
	int i;
	for (i=0;i<nSteps;i++) {
		Jtout[i] = Jt[i];
		Actout[i] = Acct[i];
	}
}

void Network::GetCrossValidationAccuracy(float *Jcvout, float *Accvout) {
	int i;
	for (i=0;i<nSteps;i++) {
		Jcvout[i] = Jcv[i];
		Accvout[i] = Acccv[i];
	}
}


void Network::GetLastCrossValidationAccuracy(float *Jcvout, float *Accvout) {
	int i;
	Jcvout[0] = Jcv[nSteps-1];
	Accvout[0] = Acccv[nSteps-1];

}

int Network::GetL() {
	return L;
}

void Network::Gets(int *sout) {
	int i;
	for (i=0;i<L;i++) {
		sout[i] = s[i];
	}
}

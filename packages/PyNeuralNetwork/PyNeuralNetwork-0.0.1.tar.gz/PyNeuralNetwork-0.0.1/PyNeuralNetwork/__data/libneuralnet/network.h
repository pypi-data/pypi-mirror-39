#ifndef __NETWORK_H__
#define __NETWORK_H__
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "matrix.h"
#include "matrixmath.h"
#include "matrixarray.h"
#include "propagate.h"
#include "costfunction.h"
#include "predict.h"
#include "thetagradient.h"
#include "updatetheta.h"
using namespace std;


class Network {
	public:
		Network(int,int*,float,float);
		Network(const char*);
		Network(const Network &obj);
		~Network();
		void InputTrainingData(int*,float*,int,int*);
		void InputTrainingDataQuiet(int*,float*,int,int*);
		void InputCrossValidationData(int*,float*,int,int*);
		void InputCrossValidationDataQuiet(int*,float*,int,int*);
		void Train();
		float GetTrainingAccuracy();
		float GetCrossValidationAccuracy();
		void ClassifyData(int*,float*,int,int*);
		void ClassifyData(int*,float*,int,int*,float*);
		void TrainGradientDescent(int,float);
		void TrainGradientDescentQuiet(int,float);
		void TrainConjugateGradient();
		void ExtendArrays();
		void Save(const char*);
		
		int GetnSteps();
		void GetTrainingAccuracy(float*,float*);
		void GetCrossValidationAccuracy(float*,float*);
		void GetLastCrossValidationAccuracy(float*,float*);
		int GetL();
		void Gets(int*);
	private:
		Matrix *Xt, *Xcv;
		int *yt = NULL, *ycv = NULL;
		int mt, mcv;
		int L, *s;
		bool TData, CVData, Trained;
		float lambda, range;
		float *Jt, *Jcv, *Acct, *Acccv;
		int nSteps, nJ;
		int nT, na, nz, *Tdims, *adims, *zdims, *ddims;
		MatrixArray *Theta, *at, *zt, *acv, *zcv, *atest, *ztest, *dTheta, *delta;
};
#endif

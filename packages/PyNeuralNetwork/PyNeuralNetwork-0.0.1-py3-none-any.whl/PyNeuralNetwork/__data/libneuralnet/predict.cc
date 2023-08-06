#include "predict.h"

void Predict(Matrix &K, int *yp) {
	int i,j,k,n,m;
	float max, tmp;
	m = K.shape[0];
	n = K.shape[1];
	for (i=0;i<m;i++) {
		max = K.Get(i,0);
		k = 0;
		for (j=1;j<n;j++) {
			tmp = K.Get(i,j);
			if (tmp > max) {
				max = tmp;
				k = j;
			}
		}
		yp[i] = k+1;
	}
		
}

void PredictProbs(Matrix &z, Matrix &sm) {
	int i, j, m, n;
	float tmp;
	m = z.shape[0];
	n = z.shape[1];
	for (i=0;i<m;i++) {
		tmp = 0.0;
		for (j=0;j<n;j++) {
			tmp += exp(z.Get(i,j));
		}
		for (j=0;j<n;j++){
			sm.Set(i,j,exp(z.Get(i,j))/tmp);
		}
	}
	
}

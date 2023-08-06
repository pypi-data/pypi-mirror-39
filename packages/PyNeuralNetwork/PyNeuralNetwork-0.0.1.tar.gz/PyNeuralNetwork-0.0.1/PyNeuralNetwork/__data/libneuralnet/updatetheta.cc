#include "updatetheta.h"


void UpdateTheta(MatrixArray &Theta, MatrixArray &dTheta, float alpha) {
	int i, j, k;
	for (i=0;i<Theta.n;i++) {
		for (j=0;j<Theta.matrix[i]->shape[0];j++) {
			for (k=0;k<Theta.matrix[i]->shape[1];k++) {
				Theta.matrix[i]->Set(j,k,Theta.matrix[i]->Get(j,k) - alpha*dTheta.matrix[i]->Get(j,k));
			}
		}
	}
}

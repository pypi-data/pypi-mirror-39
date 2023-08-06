#include "thetagradient.h"

void ThetaGradient(MatrixArray &Theta, MatrixArray &a, MatrixArray &delta, int *y, int L, int *s, float Lambda, MatrixArray &dTheta) {
	int i,j,k,yk,m;
	Matrix *tmp;
	float atmp;
	m = a.matrix[0]->shape[0];
	//printf("BackPropagation\n");
	for (j=L-1;j>-1;j--) {
		//printf("BP %d:\n",j);
		if (j == L-1) {
			for (k=0;k<s[L-1];k++) {
				for (i=0;i<m;i++) {
					yk = (int) (y[i] == k+1);
					//printf("%d\n",yk);
					delta.matrix[j]->Set(i,k,a.matrix[L-1]->Get(i,k) - (float) yk);
				}
			}
		} else {
			tmp = MatrixDot(*delta.matrix[j+1],*Theta.matrix[j],false,false);
			for (k=0;k<s[j];k++) {
				for (i=0;i<m;i++) {
					atmp = a.matrix[j]->Get(i,k+1);
					delta.matrix[j]->Set(i,k,tmp->Get(i,k+1)*atmp*(1.0-atmp));
				}
			}			
			delete tmp;
		}
		//delta.matrix[j]->PrintMatrix("Delta");
	}
	
	for (j=0;j<L-1;j++) {
		MatrixDot2(*delta.matrix[j+1],*a.matrix[j],true,false,*dTheta.matrix[j]);
		dTheta.matrix[j]->DivideScalar((float) m);
		if (Lambda > 0.0) {
			atmp = Lambda / ((float) m);
			for (k=0;k<dTheta.matrix[j]->shape[0];k++) {
				for (i=1;i<dTheta.matrix[j]->shape[1];i++) {
					dTheta.matrix[j]->Set(k,i, dTheta.matrix[j]->Get(k,i) + atmp*pow(Theta.matrix[j]->Get(k,i),2.0));
				}
			}			
		}
		
	}
	
}

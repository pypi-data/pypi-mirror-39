#include "costfunction.h"

float CostFunction(MatrixArray &Theta, MatrixArray &a, MatrixArray &z, int *y, int L, int *s, float Lambda) {
	int m;
	m = a.matrix[0]->shape[0];
	Propagate(a,z,Theta,L);
	
	float J = 0.0;
	int i,j,k,nout;
	nout = s[L-1];
	float yk, hk;
	
	for (k=0;k<nout;k++) {
		//for each output,k
		for (i=0;i<m;i++) {
			hk = a.matrix[L-1]->Get(i,k);
			if (y[i] == k+1) {
				J += -cliplog(hk,1.0e-40);
			} else {
				J += -cliplog((1.0-hk),1.0e-40);
			}
			//printf("%d %d %d %d\n",k,i,y[i],(y[i] == k+1));
		}
	}
	J/=((float) m);
	
	if (Lambda > 0.0) {
		float Reg = 0.0;
		
		for (i=0;i<L-1;i++) {
			for (j=0;j<Theta.matrix[i]->shape[0];j++) {
				for (k=1;k<Theta.matrix[i]->shape[1];k++) {
					Reg += pow(Theta.matrix[i]->Get(j,k),2.0); 
				}
			}
		}
		Reg*=(Lambda/(2.0*((float) m)));
		J+=Reg;
	}
	return J;
}

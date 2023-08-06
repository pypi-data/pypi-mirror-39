#include "propagate.h"

void Propagate(MatrixArray &a, MatrixArray &z, MatrixArray &Theta, int L) {
	int i;
	for (i=0;i<L-1;i++) {
		MatrixDot2(*a.matrix[i],*Theta.matrix[i],false,true,*z.matrix[i]);
		if (i < L-2) {
			ApplySigmoidWithBias(*z.matrix[i],*a.matrix[i+1]);
		} else {
			ApplySigmoid(*z.matrix[i],*a.matrix[i+1]);
		}
	}
}

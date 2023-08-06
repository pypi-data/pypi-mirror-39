#include "sigmoid.h"

float Sigmoid(float z) {
    return 1.0/(1.0 + exp(-z));
}

float SigmoidGradient(float z) {
    return Sigmoid(z)*(1.0 - Sigmoid(z));
}

void ApplySigmoid(Matrix &in, Matrix &out) {
	int i, n;
	n = out.len;
	for (i=0;i<n;i++) {
		out.Set(i,Sigmoid(in.data[i]));
	}
}

void ApplySigmoidWithBias(Matrix &in, Matrix &out) {
	int i, j;
	for (i=0;i<out.shape[0];i++) {
		for (j=1;j<out.shape[1];j++) {
			out.Set(i,j,Sigmoid(in.data[i*(out.shape[1]-1) + j -1]));
		}
		out.Set(i,0,1.0);
	}
}

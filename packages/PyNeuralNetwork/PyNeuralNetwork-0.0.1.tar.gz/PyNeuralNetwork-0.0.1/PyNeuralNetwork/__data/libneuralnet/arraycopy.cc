#include "arraycopy.h"

void ArrayCopy(float *in, float *out, int n) {
	int i;
	for (i=0;i<n;i++) {
		out[i] = in[i];
	}
}


void ArrayCopy(int *in, int *out, int n) {
	int i;
	for (i=0;i<n;i++) {
		out[i] = in[i];
	}
}

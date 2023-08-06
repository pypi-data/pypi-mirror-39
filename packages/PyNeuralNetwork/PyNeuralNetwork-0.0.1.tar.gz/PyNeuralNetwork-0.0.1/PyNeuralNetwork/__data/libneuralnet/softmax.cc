void Softmax(float *z, int n, float *sm) {
    float tot = 0.0;
    int i;
    for (i=0;i<n;i++) {
        tot += exp(z[i]);
    }
	for (i=0;i<n;i++) {
		sm[i] = exp(z[i])/tot;
	}
}


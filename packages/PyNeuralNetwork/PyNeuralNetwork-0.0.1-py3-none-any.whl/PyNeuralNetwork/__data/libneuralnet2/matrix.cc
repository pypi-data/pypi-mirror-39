#include "matrix.h"

//initialize matrix with shape, fill with zeros
Matrix::Matrix(int *inshape) {
	int i;
	shape[0] = inshape[0];
	shape[1] = inshape[1];
	len = inshape[0]*inshape[1];
	data = new float[len];
}

Matrix::Matrix(int x, int y) {
	int i;
	//printf("M1 %d %d\n",x,y);
	shape[0] = x;
	shape[1] = y;
	//printf("M2\n");
	len = x*y;
	//printf("M3 %d\n",len);
	data = new float[len];
	//printf("M4\n");
}

//copy constructor
Matrix::Matrix(const Matrix &obj) {
	printf("Matrix copy constructor called!");
	shape[0] = obj.shape[0];
	shape[1] = obj.shape[1];
	len = obj.len;
	data = new float[len];
	int i;
	for (i=0;i<len;i++) {
		data[i] = obj.data[i];
	}
}


//must deallocate the data array
Matrix::~Matrix() {
	delete[] data;
}

void Matrix::FillZeros() {
	int i;
	for (i=0;i<len;i++) {
		data[i] = 0.0;
	}
}

float Matrix::Get(int i, int j) {
	int ind = i*shape[1] + j;
	return data[ind];
}

float Matrix::GetT(int i, int j) {
	int ind = j*shape[1] + i;
	return data[ind];
}


void Matrix::Set(int i, float x) {
	data[i] = x;
}

void Matrix::Set(int i, int j, float x) {
	int ind = i*shape[1] + j;
	data[ind] = x;
}

void Matrix::TimesScalar(float x) {
	int i;
	for (i=0;i<len;i++) {
		data[i] *= x;
	}
}	

void Matrix::DivideScalar(float x) {
	int i;
	for (i=0;i<len;i++) {
		data[i] /= x;
	}
}	

void Matrix::AddScalar(float x) {
	int i;
	for (i=0;i<len;i++) {
		data[i] += x;
	}
}	

void Matrix::SubtractScalar(float x) {
	int i;
	for (i=0;i<len;i++) {
		data[i] -= x;
	}
}	

void Matrix::SubtractFromScalar(float x) {
	int i;
	for (i=0;i<len;i++) {
		data[i] = x - data[i];
	}
}	

void Matrix::PrintMatrix() {
	int i,j;
	for (i=0;i<shape[0];i++) {
		for (j=0;j<shape[1];j++) {
			printf("%10.5f ",Get(i,j));
		}
		printf("\n");
	}
}

void Matrix::PrintMatrix(const char *str) {
	int i,j;
	printf("%s\n",str);
	printf("shape = (%d,%d)\n",shape[0],shape[1]);
	for (i=0;i<shape[0];i++) {
		for (j=0;j<shape[1];j++) {
			printf("%10.5f ",Get(i,j));
		}
		printf("\n");
	}
}

void Matrix::CopyMatrix(Matrix &m) {
	int i,j;
	for (i=0;i<len;i++) {
		data[i] = m.data[i];
	}
}

void Matrix::FillMatrix(float *filldata) {
	int i;
	for (i=0;i<len;i++) {
		data[i] = filldata[i];
	}
}

void Matrix::FillWithBias(float *filldata) {
	int i, j;
	for (i=0;i<shape[0];i++) {
		for (j=1;j<shape[1];j++) {
			data[i*shape[1] + j] = filldata[i*(shape[1]-1) + j - 1];
		}
		data[i*shape[1]] = 1.0;
	}
}

#include "matrixarray.h"



//allocate arrays for Theta
MatrixArray::MatrixArray(int nMat, int *MatShapes) {
	int i;
	n = nMat;
	//printf("Ma1 %d\n",n);
	matrix = new Matrix*[n];
	//printf("Ma2\n");
	for (i=0;i<n*2;i+=2){
		//printf("%d %d %d ",n*2,i,i/2);
		//printf("%d %d\n",MatShapes[i],MatShapes[i+1]);
		matrix[i/2] = new Matrix(MatShapes[i],MatShapes[i+1]);
	}
	//printf("Ma3\n");
}

MatrixArray::MatrixArray(const MatrixArray &obj) {
	printf("Called Matrix array copy constructor\n");
}

MatrixArray::~MatrixArray() {
	int i;
	for (i=0;i<n;i++) {
		delete matrix[i];
	}
	delete[] matrix;
}

void MatrixArray::RandomInit(float Range) {
	//Range in the original python implementation = 0.12
	
	//seed the random number generator
	
	//now fill each array
	int i, j;
	
	for (i=0;i<n;i++) {
		//for each matrix
		for (j=0;j<matrix[i]->len;j++) {
			//for each element in matrix
			matrix[i]->data[j] = Range*(2.0*((float) rand()) / ((float) RAND_MAX) - 1.0);
		}
	}
}

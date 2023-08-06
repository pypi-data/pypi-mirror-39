#ifndef __MATRIX_H_INCLUDED__
#define __MATRIX_H_INCLUDED__
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
using namespace std;

class Matrix {
	public:
		int shape[2];
		int len;
		Matrix(int*);
		Matrix(int,int);
		Matrix(const Matrix &obj);
		~Matrix();
		void FillZeros();
		float Get(int,int);
		float GetT(int,int);
		void Set(int,float);
		void Set(int,int,float);
		void TimesScalar(float);
		void DivideScalar(float);
		void AddScalar(float);
		void SubtractScalar(float);
		void SubtractFromScalar(float);
		void PrintMatrix();
		void PrintMatrix(const char *);
		void CopyMatrix(Matrix&);
		void FillMatrix(float*);
		void FillWithBias(float*);
		float *data = NULL;
	private:
		
};

#endif

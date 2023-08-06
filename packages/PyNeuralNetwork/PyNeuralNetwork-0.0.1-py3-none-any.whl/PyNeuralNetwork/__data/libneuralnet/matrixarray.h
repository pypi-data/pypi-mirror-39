#ifndef __THETA_H__
#define __THETA_H__
#include <math.h>
#include <stdio.h>
#include <ctime>
#include <cstdlib>
#include "matrix.h"
using namespace std;
class MatrixArray {
	public:
		int n;
		Matrix **matrix;
		MatrixArray(int,int*);
		MatrixArray(const MatrixArray &obj);
		~MatrixArray();
		void RandomInit(float);
	private:

};

#endif

#ifndef __THETAGRADIENT_H__
#define __THETAGRADIENT_H__
#include <stdio.h>
#include <math.h>
#include "matrix.h"
#include "matrixmath.h"
#include "matrixarray.h"
void ThetaGradient(MatrixArray &Theta, MatrixArray &a, MatrixArray &delta, int *y, int L, int *s, float Lambda, MatrixArray &dTheta);
using namespace std;
#endif

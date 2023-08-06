#ifndef __COSTFUNCTION_H__
#define __COSTFUNCTION_H__
#include <math.h>
#include <stdio.h>
#include "matrixarray.h"
#include "cliplog.h"
#include "propagate.h"
using namespace std;
float CostFunction(MatrixArray &Theta, MatrixArray &a, MatrixArray &z, int *y, int L, int *s, float Lambda);
#endif

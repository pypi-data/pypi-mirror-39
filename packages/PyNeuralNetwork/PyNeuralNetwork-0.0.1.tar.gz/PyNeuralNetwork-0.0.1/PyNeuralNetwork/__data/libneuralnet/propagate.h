#ifndef __PROPAGATE_H__
#define __PROPAGATE_H__
#include <stdio.h>
#include <math.h>
#include "matrix.h"
#include "matrixmath.h"
#include "matrixarray.h"

#include "sigmoid.h"
using namespace std;

void Propagate(MatrixArray &a, MatrixArray &z, MatrixArray &Theta, int L);
#endif


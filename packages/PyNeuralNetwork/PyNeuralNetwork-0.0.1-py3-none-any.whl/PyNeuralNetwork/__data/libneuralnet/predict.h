#ifndef __PREDICT_H__
#define __PREDICT_H__
#include <stdio.h>
#include "matrix.h"
using namespace std;

void Predict(Matrix &K, int *yp);
void PredictProbs(Matrix &z, Matrix &sm);
#endif

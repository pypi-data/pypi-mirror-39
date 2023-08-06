#ifndef __SIGMOID_H__
#define __SIGMOID_H__
#include <math.h>
#include <stdio.h>
#include "matrix.h"
using namespace std;
float Sigmoid(float z);
float SigmoidGradient(float z);
void ApplySigmoid(Matrix &in, Matrix &out);
void ApplySigmoidWithBias(Matrix &in, Matrix &out);
#endif

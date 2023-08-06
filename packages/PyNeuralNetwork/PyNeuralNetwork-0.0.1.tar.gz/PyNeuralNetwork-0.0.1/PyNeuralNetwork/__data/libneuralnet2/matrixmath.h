#ifndef __MATRIXMATH_H__
#define __MATRIXMATH_H__
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "matrix.h"
#include <omp.h>
using namespace std;

Matrix * MatrixMultiply(Matrix &a, Matrix &b, bool aT, bool bT);
void MatrixMultiply2(Matrix &a, Matrix &b, bool aT, bool bT, Matrix &out);
Matrix * MatrixDot(Matrix &a, Matrix &b, bool aT, bool bT);
void MatrixDot2(Matrix &a, Matrix &b, bool aT, bool bT, Matrix &out);
#endif

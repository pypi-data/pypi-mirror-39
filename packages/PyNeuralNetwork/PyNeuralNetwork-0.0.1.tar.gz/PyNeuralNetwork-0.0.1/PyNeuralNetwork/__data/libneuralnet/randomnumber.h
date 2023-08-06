#ifndef __RANDOMNUMBER_H__
#define __RANDOMNUMBER_H__
#include <math.h>
#include <stdio.h>
#include <ctime>
#include <cstdlib>


using namespace std;
void SeedRandom();
int RandomNumber(int *Range);
int RandomNumber(int R0, int R1);
float RandomNumber(float *Range);
float RandomNumber(float R0, float R1);
float RandomLogRange(float R0, float R1);
float RandomLogRange(float *Range);
#endif

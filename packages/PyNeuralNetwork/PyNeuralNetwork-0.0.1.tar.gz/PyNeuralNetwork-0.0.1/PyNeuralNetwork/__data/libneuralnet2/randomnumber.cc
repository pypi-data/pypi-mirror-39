#include "randomnumber.h"

void SeedRandom() {
	//seed the random number generator
	srand((unsigned) time(NULL));
}	

int RandomNumber(int *Range) {
	//seed the random number generator
	//srand((unsigned) time(NULL));
	
	//now fill each array
	return (int) round((Range[1]-Range[0])*(((float) rand()) / ((float) RAND_MAX))) + Range[0];
}

int RandomNumber(int R0, int R1) {
	//seed the random number generator
	//srand((unsigned) time(NULL));
	
	//now fill each array
	return (int) round((R1-R0)*(((float) rand()) / ((float) RAND_MAX))) + R0;
}


float RandomNumber(float *Range) {
	//seed the random number generator
	//srand((unsigned) time(NULL));
	
	//now fill each array
	return (Range[1]-Range[0])*(((float) rand()) / ((float) RAND_MAX)) + Range[0];
}

float RandomNumber(float R0, float R1) {
	//seed the random number generator
	//srand((unsigned) time(NULL));
	
	//now fill each array
	return (R1-R0)*(((float) rand()) / ((float) RAND_MAX)) + R0;
}

float RandomLogRange(float R0, float R1) {
	R0 = log10f(R0);
	R1 = log10f(R1);
	return powf((R1-R0)*(((float) rand()) / ((float) RAND_MAX)) + R0,10.0);
}

float RandomLogRange(float *Range) {
	float R0 = log10f(Range[0]);
	float R1 = log10f(Range[1]);
	return powf(10.0,(R1-R0)*(((float) rand()) / ((float) RAND_MAX)) + R0);
}

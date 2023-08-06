# Compiler
CC=g++

# CFLAGS for CC
CFLAGS=-lm

All: o tests lib

o:
	$(CC) -c -fpic tests.cc matrix.cc matrixmath.cc matrixarray.cc network.cc sigmoid.cc propagate.cc cliplog.cc costfunction.cc predict.cc thetagradient.cc updatetheta.cc libneuralnet.cc evolution.cc randomnumber.cc arraycopy.cc

tests:
	$(CC) tests.o matrix.o matrixmath.o matrixarray.o network.o sigmoid.o propagate.o cliplog.o costfunction.o predict.o thetagradient.o updatetheta.o randomnumber.o -o tests $(CFLAGS)
	
lib:
	$(CC) -shared libneuralnet.o matrix.o matrixmath.o matrixarray.o network.o sigmoid.o propagate.o cliplog.o costfunction.o predict.o thetagradient.o updatetheta.o evolution.o randomnumber.o arraycopy.o -o libneuralnet.so $(CFLAGS)

clean:
	rm -v *.o tests *.so

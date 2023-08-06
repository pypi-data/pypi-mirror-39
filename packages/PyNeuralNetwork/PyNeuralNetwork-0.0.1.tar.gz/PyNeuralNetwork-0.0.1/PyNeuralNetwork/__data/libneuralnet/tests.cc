#include "tests.h"

float RandomNormal() {
	float x = (float)random()/(float)RAND_MAX;
	float y = (float)random()/(float)RAND_MAX;
	float z = sqrt(-2*log(x))*cos(2*M_PI*y);
	return z;
}

int main() {

	printf("Testing Matrices...\n");
	//create some test matrices
	Matrix *a, *b, *c, *d, *e;
	a = new Matrix (2,3);
	b = new Matrix (2,3);
	d = new Matrix (3,2);




	printf("Matrix of zeros (a)\n");
	a->FillZeros();
	a->PrintMatrix("a=");

	int i, j, v=0;
	for (i=0;i<2;i++) {
		for (j=0;j<3;j++) {
			a->Set(i,j,2.0*v++);
		}
	}
	printf("Filled a with some values\n");
	a->PrintMatrix("a=");
	b->FillZeros();
	printf("1\n");
	b->CopyMatrix(*a);
	printf("2\n");
	a->PrintMatrix("a=");
	b->PrintMatrix("b=");
	
	printf("Test multiplying a by b elementwise to make c\n");
	c = MatrixMultiply(*a,*b,false,false);
	a->PrintMatrix("a=");
	b->PrintMatrix("b=");
	c->PrintMatrix("c=");
	
	printf("create matrix d and multipy (dot) a by d to make e\n");
	d->FillZeros();
	d->AddScalar(10.0);
	a->PrintMatrix("a=");
	d->PrintMatrix("d=");
	e = MatrixDot(*a,*d,false,false);
	e->PrintMatrix("e=");
	
	
	printf("A test of MatrixDot2 with transpose a.bT\n");
	delete c;
	c = new Matrix(2,2);
	MatrixDot2(*a,*b,false,true,*c);
	a->PrintMatrix("a=");
	b->PrintMatrix("b=");
	c->PrintMatrix("result=");
	

	delete a;
	delete b;
	delete c;
	delete d;
	delete e;
	
	
	for (i=0;i<3;i++) {
		printf("creating matrix %d of %d\n",i+1,100);
		a = new Matrix(RandomNumber(2,10),RandomNumber(2,10));
		a->FillZeros();
		delete a;
	}
	
	MatrixArray *ma;
	int nMat, *Matshapes;
	for (i=0;i<2;i++) {
		printf("creating matrix array %d of %d\n",i+1,100);
		nMat = RandomNumber(2,4);
		Matshapes = new int[nMat*2];
		for (j=0;j<nMat*2;j++) {
			Matshapes[j] = RandomNumber(5,10);
		}
		ma = new MatrixArray(nMat,Matshapes);
		ma->RandomInit(0.12);
		delete ma;
		delete[] Matshapes;
	}	
/*	
	int nLayers = 3, Layers[] = { 1,2,2 };
	Network *nn;
	nn = new Network(nLayers,Layers,0.0,0.12);

	
	int mt = 1500, mcv = 500;
	float xt[mt], xcv[mcv];
	int yt[mt], ycv[mcv];
	float mu, sigma, x;
	int y;
	for (i=0;i<mt+mcv;i++) {
		y = (int) round(((float) rand()) / ((float) RAND_MAX));
		if (y == 1) {
			mu = 5.0;
			sigma = 2.5;
		} else {
			mu = -2.0;
			sigma = 1.5;
		}
		x = mu + sigma*RandomNormal();
		if (i < mt) {
			xt[i] = x;
			yt[i] = y;
		} else {
			xcv[i-mt] = x;
			ycv[i-mt] = y;
		}
		printf("x: %f, y: %d\n",x,y);
	}
	int xshape[] = {mt,1};
	
	float xt[] = {1.99015142,  3.11548739,  2.63819611,  6.77840789,  6.75914805,  7.1006716 , -0.43279053,  5.38676427,  4.3502877 ,  6.10551742,   1.33019172, -4.01523372, -1.98294515,  0.72378299, -4.31963048};
	int yt[] = {1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  2, 2,  2};
	
	float xcv[] = {3.68820375, -1.0672715 , 6.38518699, -1.70199415, -2.72775383};
	int ycv[] = { 1,  2,  1,  2,  2};
	
	int mt = 15, xshape[] = {15,1};
	
	float Theta0[] = {-0.11297765, 0.0457558 ,-0.11188263,  0.00843696};
	float Theta1[] = {0.11509074,0.10543039,-0.03145336,-0.1168719,0.05472495,-0.00337395};
	
	nn->InputTrainingData(xshape,xt,mt,yt);
	nn->Theta->matrix[0]->FillMatrix(Theta0);
	nn->Theta->matrix[1]->FillMatrix(Theta1);

	nn->Theta->matrix[0]->PrintMatrix("Theta 0");
	nn->Theta->matrix[1]->PrintMatrix("Theta 1");
	nn->TrainGradientDescent(2000,0.1f);

	delete nn;*/
	
	Network *nn;
/*	int xtshape[] = {15,1};
	
	float xt[] = {1.99015142,  3.11548739,  2.63819611,  6.77840789,  6.75914805,  7.1006716 , -0.43279053,  5.38676427,  4.3502877 ,  6.10551742,   1.33019172, -4.01523372, -1.98294515,  0.72378299, -4.31963048};
	int yt[] = {1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  2, 2,  2};
	
	float xcv[] = {3.68820375, -1.0672715 , 6.38518699, -1.70199415, -2.72775383};
	int ycv[] = { 1,  2,  1,  2,  2};
	
	int mt = 15, mcv = 5, xcshape[] = {5,1};
	int nLayers, *Layers;
	SeedRandom();
	for (i=0;i<100;i++) {
		printf("creating network %d of %d\n",i+1,100); 
		nLayers = RandomNumber(3,5);
		Layers = new int[nLayers];

		for (j=1;j<nLayers-1;j++) {
			Layers[j] = RandomNumber(2,7)+1;
		}
		Layers[0] = 1;
		Layers[nLayers-1] = 2;
		//printf("here1\n");
		nn = new Network(nLayers,Layers,0.1,0.12);
		//printf("here2\n");
		nn->InputTrainingData(xtshape,xt,mt,yt);
		//printf("here3\n");
		//nn->InputCrossValidationData(xcshape,xcv,mcv,ycv);
		//printf("here4\n");
		delete nn;
		//printf("here5\n");
		delete[] Layers;
	}*/
	
	nn = new Network("/media/data/work/python3/Cancer-00.nn");
	
	delete nn;
	return 0;
		
}
	
	

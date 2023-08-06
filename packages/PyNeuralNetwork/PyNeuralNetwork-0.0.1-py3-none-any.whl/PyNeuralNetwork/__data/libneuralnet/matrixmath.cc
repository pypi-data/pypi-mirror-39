#include "matrixmath.h"

Matrix * MatrixMultiply(Matrix &a, Matrix &b, bool aT, bool bT) {
	Matrix *o;
	int oshape[2];
	if (aT) {
		
		oshape[0] = a.shape[1];
		oshape[1] = a.shape[0];
	} else {
		oshape[0] = a.shape[0];
		oshape[1] = a.shape[1];
	}
	o = new Matrix(oshape[0],oshape[1]);
	int i,j;
	
	float (Matrix::*Geta)(int,int) ;
	float (Matrix::*Getb)(int,int);
	if (aT) {
		Geta = &Matrix::GetT;
	} else {
		Geta = &Matrix::Get;
	}
	if (bT) {
		Getb = &Matrix::GetT;
	} else {
		Getb = &Matrix::Get;
	}
	for (i=0;i<oshape[0];i++) {
		for (j=0;j<oshape[1];j++) {
			o->Set(i,j,(a.*Geta)(i,j)*(b.*Getb)(i,j));
		}
	}
	return o;
}


void MatrixMultiply2(Matrix &a, Matrix &b, bool aT, bool bT, Matrix &out) {
	int oshape[2];
	if (aT) {
		
		oshape[0] = a.shape[1];
		oshape[1] = a.shape[0];
	} else {
		oshape[0] = a.shape[0];
		oshape[1] = a.shape[1];
	}
	int i,j;
	
	float (Matrix::*Geta)(int,int) ;
	float (Matrix::*Getb)(int,int);
	if (aT) {
		Geta = &Matrix::GetT;
	} else {
		Geta = &Matrix::Get;
	}
	if (bT) {
		Getb = &Matrix::GetT;
	} else {
		Getb = &Matrix::Get;
	}
	for (i=0;i<oshape[0];i++) {
		for (j=0;j<oshape[1];j++) {
			out.data[i*oshape[1] + j] = (a.*Geta)(i,j)*(b.*Getb)(i,j);
		}
	}
}


Matrix * MatrixDot(Matrix &a, Matrix &b, bool aT, bool bT) {
	int kdim;
	int ashape[2], bshape[2];
	
	if (aT) {
		ashape[0] = a.shape[1];
		ashape[1] = a.shape[0]; 
	} else {
		ashape[0] = a.shape[0];
		ashape[1] = a.shape[1];		
	}

	if (bT) {
		bshape[0] = b.shape[1];
		bshape[1] = b.shape[0]; 
	} else {
		bshape[0] = b.shape[0];
		bshape[1] = b.shape[1];		
	}
	if (ashape[1] == bshape[0]) {
		kdim = ashape[1];
	} else {
		printf("Warning! shape of input values should be a(i,j), b(j,k), this may produce strange results\n");
		if (ashape[1] < bshape[0]) {
			kdim = ashape[1];
		} else {
			kdim = bshape[0];
		}
	}
	Matrix *o;
	o = new Matrix(ashape[0],bshape[1]);
	
	float (Matrix::*Geta)(int,int) ;
	float (Matrix::*Getb)(int,int);
	if (aT) {
		Geta = &Matrix::GetT;
	} else {
		Geta = &Matrix::Get;
	}
	if (bT) {
		Getb = &Matrix::GetT;
	} else {
		Getb = &Matrix::Get;
	}
	
	int i,j,k;
	float tmp;
	for (i=0;i<o->shape[0];i++) {
		for (j=0;j<o->shape[1];j++) {
			tmp = 0.0;
			for (k=0;k<kdim;k++) {
				tmp += (a.*Geta)(i,k)*(b.*Getb)(k,j);
			}
			o->Set(i,j,tmp);
		}
	}
	return o;
}


void MatrixDot2(Matrix &a, Matrix &b, bool aT, bool bT, Matrix &out) {
	int kdim;
	int ashape[2], bshape[2];
	
	if (aT) {
		ashape[0] = a.shape[1];
		ashape[1] = a.shape[0]; 
	} else {
		ashape[0] = a.shape[0];
		ashape[1] = a.shape[1];		
	}

	if (bT) {
		bshape[0] = b.shape[1];
		bshape[1] = b.shape[0]; 
	} else {
		bshape[0] = b.shape[0];
		bshape[1] = b.shape[1];		
	}
	if (ashape[1] == bshape[0]) {
		kdim = ashape[1];
	} else {
		printf("Warning! shape of input values should be a(i,j), b(j,k), this may produce strange results\n");
		if (ashape[1] < bshape[0]) {
			kdim = ashape[1];
		} else {
			kdim = bshape[0];
		}
	}

	
	float (Matrix::*Geta)(int,int) ;
	float (Matrix::*Getb)(int,int);
	if (aT) {
		Geta = &Matrix::GetT;
	} else {
		Geta = &Matrix::Get;
	}
	if (bT) {
		Getb = &Matrix::GetT;
	} else {
		Getb = &Matrix::Get;
	}
	
	int i,j,k;
	float tmp;
	for (i=0;i<ashape[0];i++) {
		for (j=0;j<bshape[1];j++) {
			tmp = 0.0;
			for (k=0;k<kdim;k++) {
				tmp += (a.*Geta)(i,k)*(b.*Getb)(k,j);
			}
			out.data[i*bshape[1] + j] = tmp;
		}
	}
}

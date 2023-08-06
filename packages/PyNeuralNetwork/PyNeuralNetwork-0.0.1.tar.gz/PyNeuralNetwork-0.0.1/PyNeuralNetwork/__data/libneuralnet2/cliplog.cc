#include "cliplog.h"

float cliplog(float x, float min) {
	if (x < min) {
		return log(min);
	} else {
		return log(x);
	}
}

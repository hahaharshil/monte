#include <stdlib.h>
#include <time.h>



void randInit(void) {
    srand48(time(NULL));
}


float randFloat(float min, float max){

    return min + (max - min) * drand48();
}


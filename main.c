#include <stdio.h>
#include <stdlib.h>
#include "random.h"


int main(int argc, char *argv[]){


    randInit();

    for(int i = 0; i < atoi(argv[1]); i++){
        printf("%f %f\n", randFloat(atoi(argv[2]), atoi(argv[3])), 
                        randFloat(atoi(argv[2]), atoi(argv[3])));
    }



    return 0;
}

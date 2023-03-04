#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<malloc.h>
#include<math.h>
#include "trigengines.c"

int test_rxengine() {
    float xfield[] = {0, 1, -1, 0};
    float yfield[] = {0, 1, -1, 0};
    float zfield[] = {0, 0, 0, 1};
    float xyzref = 0;
    float c = 1540;
    float tau_known[] = {0, sqrtf(2)/c, sqrtf(2)/c, sqrtf(2)/c};
    float * tau = rxengine(4, c, xyzref, xyzref, xyzref, xfield, yfield, zfield);

    for(int i = 0; i < 4; ++i) {
        if(abs(tau[i] - tau_known[i]) > 1E-6) {
            return -1;
        }
    }

    return 0;
}

int main(){
    printf("Beginning testing suite...\n");
    if (test_rxengine()) {
        printf("  An unexpected value occured in test_rxengine");
    }
    printf("Completed testing\n");
    return 0;
}
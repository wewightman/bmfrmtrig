#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<malloc.h>
#include<math.h>
#include "trigengines.c"

#define EPSILON 1E-32

int test_rxengine() {
    float xfield[4] = {0.0f, 1.0f, -1.0f, 0.0f};
    float yfield[4] = {0.0f, 1.0f, -1.0f, 0.0f};
    float zfield[4] = {0.0f, 0.0f, 0.0f, 1.0f};
    float xyzref = 0.0f;
    float c = 2.0f;
    float tau_known[] = {0.0f, sqrtf(2.0f)/c, sqrtf(2.0f)/c, 1/c};
    float * tau = rxengine(4, c, xyzref, xyzref, xyzref, xfield, yfield, zfield);

    int failed = 0;
    for(int i = 0; i < 4; ++i) {
        if(abs(tau[i] - tau_known[i]) > EPSILON) {
            failed = -1;
            printf("    index %d: expected %0.06e but got %0.06e\n", i, tau_known[i], tau[i]);
        }
    }

    return failed;
}

int test_pwtxengine() {
    float xfield[4] = {0.0f, 1.0f, -1.0f, 0.0f};
    float yfield[4] = {0.0f, 1.0f, -1.0f, 0.0f};
    float zfield[4] = {0.0f, 0.0f, 0.0f, 1.0f};
    float xyzref = 0.0f;
    float nxy = 0;
    float nz = 1.0f;
    float c = 2.0f;
    float tref = 0.0f;
    float * tau_known = zfield;
    float * tau = pwtxengine(4, c, tref, xyzref, xyzref, xyzref, nxy, nxy, nz, xfield, yfield, zfield);

    int failed = 0;
    for(int i = 0; i < 4; ++i) {
        if(abs(tau[i] - tau_known[i]) > EPSILON) {
            failed = -1;
            printf("    index %d: expected %0.06e but got %0.06e\n", i, tau_known[i], tau[i]);
        }
    }

    return failed;
}

int main(){
    printf("Beginning testing suite...\n");

    // run rxengine test
    printf("  Testing rxengine...\n");
    if (test_rxengine()) {printf("  Test failed\n");} else {printf("  Test passed\n");}

    // run pwtxengine test
    printf("  Testing pwtxengine...\n");
    if (test_pwtxengine()) {printf("  test failed\n");} 
    else {printf("  Test passed\n");}

    printf("Completed testing\n");
    return 0;
}
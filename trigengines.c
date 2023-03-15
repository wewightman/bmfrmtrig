#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<malloc.h>
#include<math.h>
#include "trigengines.h"

/**
 * rxengine
 * Calculate the temporal distance from reference point to each point in the field
 * N: number of points in field
 * c: speed of sound [m/s]
 * xref, yref, zref: (x, y, z) coordinate of reference point [m]
 * xfield, yfield, zfield: pointers to length N arrays of (x, y, z) coordinates in field
 */
float * rxengine(int N, float c, float * ref, float * points) {
    // define the output array of tau
    float * tau;
    tau = malloc(N*sizeof(float));

    // iterate through each point
    for(int i = 0; i < N; ++i) {
        float xdiff = points[3*i+0] - ref[0];
        float ydiff = points[3*i+1] - ref[1];
        float zdiff = points[3*i+1] - ref[2];

        tau[i] = sqrtf(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)/c;
    }

    // return the tau pointer
    return tau;
}

/**
 * pwtxengine
 * Calculate the temporal distance from reference point to each point in the field
 * N: number of points in field
 * c: speed of sound [m/s]
 * ref: (x, y, z) coordinate of reference point [m]
 * norm: (x, y, z) normal vector
 * xfield, nx, yfield, ny, zfield, nz: pointers to length N arrays of (x, y, z) coordinates in field
 */
float * pwtxengine(int N, float c, float tref, float *ref, float *norm, float *points) {
    // define the output array of tau
    float * tau;
    tau = malloc(N*sizeof(float));

    // iterate through each point
    float xdiff;
    float ydiff;
    float zdiff;
    for(int i = 0; i < N; ++i) {
        xdiff = norm[0] * (points[3*i+0] - ref[0]);
        ydiff = norm[1] * (points[3*i+1] - ref[1]);
        zdiff = norm[2] * (points[3*i+2] - ref[2]);

        tau[i] = sqrtf(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)/c;
    }

    // return the time delay pointer
    return tau;
}

int * genmask3D(int N, float fmaj, int dynmaj, float fmin, int dynmin, float * n, float *focus, float *ref, float *points) {
    float nmaj[3] = {n[0], n[1], 0.0f};
    float nmin[3] = {-n[1], n[0], 0.0f};
    float rmaj;
    float rmin;
    int inmaj;
    int inmin;

    int * mask = malloc(sizeof(int) * N);

    for(int i = 0; i < N; ++i) {
        // calculate radius from center line
        rmaj = nmaj[0] * (points[3*i+0] - ref[0]) + nmaj[1] * (points[3*i+1] - ref[1]);
        rmin = nmin[0] * (points[3*i+0] - ref[0]) + nmin[1] * (points[3*i+1] - ref[1]);
        if (rmaj < 0.0f) {rmaj = -rmaj;}
        if (rmin < 0.0f) {rmin = -rmin;}

        // determine if within major axis
        inmaj = 0;
        if(dynmaj) {
            if (2.0f*rmaj <= (points[3*i+2] - ref[2])/fmaj) {inmaj=-1;}
        } else {
            if (2.0f*rmaj <= (focus[2] - ref[2])/fmaj) {inmaj=-1;}
        }

        // calculate if within minor axis
        inmin = 0;
        if(dynmin) {
            if (2*rmin <= (points[3*i+2] - ref[2])/fmin) {inmin=-1;}
        } else {
            if (2*rmin <= (focus[2] - ref[2])/fmin) {inmin=-1;}
        }

        mask[i] = inmaj && inmin;
    }
    return mask;
}

/**
 * sumvecs:
 * sum vec1, vec2, and a given constant value
 */
float * sumvecs(int N, float *vec1, float *vec2, float v0) {
    float * summed = malloc(sizeof(float) * N);
    for (int i = 0; i < N; ++i) {
        summed[i] = vec1[i] + vec2[i] + v0;
    }
    return summed;
}

/**
 * calcindices
 * returns an Ntau length array of integer indices with values ranging from [-1, Ntrace)
 * A value of -1 indicates an array index out of bounds or a masked out value
 */
void calcindices(int Ntau, int Ntrace, float tstart, float Ts, float * tau, int *mask, int * tind) {
    int index;

    for (int i = 0; i < Ntau; ++i) {
        index = (int) ((tau[i] - tstart)/Ts);
        if((index >= Ntrace) || (index < 0) || !mask[i]) {
            tind[i] = index;
        } else {
            tind[i] = -1;
            mask[i] = 0;
        }
        
    }
}

/**
 * freeme:
 * Free an allocated c-array
 */
void freeme(float * ptr) {
    free((void*)ptr);
}

/**
 * 
 */
void printifa(int i, float f, float * a, int na) {
    printf("%p \n", a);
    printf("%d, %0.03f, [", i, f);
    for (int icount = 0; icount < na; ++icount) {
        printf("%f, ", a[icount]);
    }
    printf("\b\b]\n");
}

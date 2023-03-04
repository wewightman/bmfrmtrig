#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<malloc.h>
#include<math.h>

/**
 * rxengine
 * Calculate the temporal distance from reference point to each point in the field
 * N: number of points in field
 * c: speed of sound [m/s]
 * xref, yref, zref: (x, y, z) coordinate of reference point [m]
 * xfield, yfield, zfield: pointers to length N arrays of (x, y, z) coordinates in field
 */
float * rxengine(int N, float c, float xref, float yref, float zref, float * xfield, float * yfield, float * zfield) {
    // define the output array of tau
    float * tau;
    tau = malloc(N*sizeof(float));

    // iterate through each point
    for(int i = 0; i < N; ++i) {
        float xdiff = xfield[i] - xref;
        float ydiff = yfield[i] - yref;
        float zdiff = zfield[i] - zref;

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
 * xref, yref, zref: (x, y, z) coordinate of reference point [m]
 * nx, ny, nz: (x, y, z) normal vector
 * xfield, yfield, zfield: pointers to length N arrays of (x, y, z) coordinates in field
 */
float * pwtxengine(int N, float c, float tref, float xref, float yref, float zref, float nx, float ny, float nz, float * xfield, float * yfield, float * zfield) {
    // define the output array of tau
    float * tau;
    tau = malloc(N*sizeof(float));

    // iterate through each point
    float xdiff;
    float ydiff;
    float zdiff;
    for(int i = 0; i < N; ++i) {
        xdiff = nx * (xfield[i] - xref);
        ydiff = ny * (yfield[i] - yref);
        zdiff = nz * (zfield[i] - zref);

        tau[i] = sqrtf(xdiff*xdiff + ydiff*ydiff + zdiff*zdiff)/c;
    }

    // return the time delay pointer
    return tau;
}
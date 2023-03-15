// function declarations
extern float * rxengine(int N, float c, float * ref, float * points);
extern float * pwtxengine(int N, float c, float tref, float *ref, float *norm, float *points);
extern void genmask3D(int N, float fmaj, int dynmaj, float fmin, int dynmin, float * n, float *focus, float *ref, float *points, int *mask);
extern void calcindices(int Ntau, int Ntrace, float tstart, float Ts, float * tau, int *mask, int * tind);
extern float * selectdata(int Nsamp, int Ntind, int indacq, int * tind, float * data);
extern float * sumvecs(int N, float *vec1, float *vec2, float v0);
extern void freeme(float * ptr);
extern void printifa(int i, float f, float * a, int na);
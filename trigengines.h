// function declarations
extern float * rxengine(int N, float c, float * ref, float * points);
extern float * pwtxengine(int N, float c, float tref, float * ref, float * norm, float *points);
extern int * genmask3D(int N, float fmaj, int dynmaj, float fmin, int dynmin, float * n, float *focus, float *ref, float *points);
extern float * extractfromvec(int Ntau, int Ntrace, float tstart, float Ts, float * tautx, float * taurx, float *mask, float * trace);
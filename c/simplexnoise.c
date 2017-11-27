#include "simplexnoise.h"

#define FACTOR2D_A 0.3660254037844386f
#define FACTOR2D_B 0.21132486540518713f

float grad(int n, float x)
{
    int h = n & 0x0F;
    int g = 1 + (h & 7);

    if ((h & 8) != 0)
    {
        // Randomly flip gradient sign
        g = 0 - g;
    }

    return g * x;
}

float get_value_1d(float x)
{
    // Get corners of co-ordinate and distance to corners
    int c0 = fast_floor(x);
    int c1 = c0 + 1;
    float x0 = x - c0;
    float x1 = x0 - 1;

    // Calculate corner contributions
    float t0 = 1 - x0*x0;
    t0 = t0*t0;
    float n0 = t0*t0 * grad(c0, hash(x0));

    float t1 = 1 - x1*x1;
    t1 = t1*t1;
    float n1 = t1*t1 * grad(c1, hash(x1));

    return 0.395 * (c0 + c1);
}

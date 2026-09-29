// Version 3.1: 64 bits, formato 1:10:53, optimizacion con corrimiento
#include <stdio.h>
#include <stdint.h>
#include "intArith.h"

int main()
{
    initializeA(10, 53); // formato 1.10.53, 64 bits

    long sigma = setNumber(10.0);
    long rho = setNumber(28.0);
    long beta = setNumber(2.66666666666666666666);
    
    long x = setNumber(1.0);
    long y = setNumber(1.0);
    long z = setNumber(1.0);

    int iterations = 4166667; 
    int n = 1;                

    FILE *file = fopen("lorenz_prng64b.bin", "wb");

    int warmup = 50000;
    
    for (int i = 0; i < warmup; i++)
    {
        long dx = mulTrunc(sigma, (y - x));
        long dy = mulTrunc(x, (rho - z)) - y;
        long dz = mulTrunc(x, y) - mulTrunc(beta, z);

        dx = dx >> 7;
        dy = dy >> 7;
        dz = dz >> 7;

        x += dx; y += dy; z += dz;
    }

    for (int i = 0; i < iterations; i++) 
    {
        for (int j = 0; j < n; j++)
        {
            long dx = mulTrunc(sigma, (y - x));
            long dy = mulTrunc(x, (rho - z)) - y;
            long dz = mulTrunc(x, y) - mulTrunc(beta, z);

            dx = dx >> 7;
            dy = dy >> 7;
            dz = dz >> 7;

            x += dx; y += dy; z += dz;
        }

        // Extraer los 8 LSBs
         uint8_t lsb_state[3] = {
            (uint8_t)(x & 0xFF),
            (uint8_t)(y & 0xFF),
            (uint8_t)(z & 0xFF),
        };

        fwrite(lsb_state, 1, 3, file);
    }

    fclose(file);
    return 0;
}
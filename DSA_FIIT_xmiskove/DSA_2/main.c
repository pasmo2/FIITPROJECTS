#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include "dsa_strom.c"
#include "dsa_strom_cudzi.c"
#include "dsa_hash.c"
#include "dsa_hash_cudzi.c"






int main() {
    srand(time(0));
    fullTestStrom(1000);
    fullTestStromCudzi(1000);
    fullTestHash(1000);
    fullTestHashCudzi(1000);
    return 0;
}

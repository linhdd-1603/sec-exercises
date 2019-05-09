//  g++ -O2 -o encrypt.exe encrypt.cpp mt19937ar.cpp

#include <stdio.h>
#include <stdlib.h>
#include "mt19937ar.h"

typedef unsigned long dword;

void initialize(const char *seed);
void encrypt(const char *plain, const char *crypt, const char *key);
void decrypt(const char *plain, const char *crypt, const char *key);
int min(int a, int b) { return a<b ? a : b; }

int main()
{
    initialize("seed");

    encrypt("encrypt.cpp", "encrypt.enc", "encrypt.key");
    encrypt("flag.jpg", "flag.enc", "flag.key");

    //  decrypt("encrypt_dec.cpp", "encrypt.enc", "encrypt.key");
    //  decrypt("flag_dec.jpg", "flag.enc", "flag.key");
}

void initialize(const char *seed)
{
    const int N = 1024;

    FILE *f = fopen(seed, "rb");
    if (f==NULL)
    {
        printf("Failed to open %s\n", seed);
        exit(-1);
    }

    dword buf[N];
    fread(buf, sizeof (dword), N, f);

    fclose(f);

    init_by_array(buf, N);
}

void encrypt(const char *plain, const char *crypt, const char *key)
{
    FILE *fp = fopen(plain, "rb");
    if (fp==NULL)
    {
        printf("Failed to open %s\n", plain);
        exit(-1);
    }
    FILE *fc = fopen(crypt, "wb");
    if (fc==NULL)
    {
        printf("Failed to open %s\n", crypt);
        exit(-1);
    }
    FILE *fk = fopen(key, "wb");
    if (fk==NULL)
    {
        printf("Failed to open %s\n", key);
        exit(-1);
    }

    fseek(fp, 0, SEEK_END);
    dword length = (dword)ftell(fp);
    fseek(fp, 0, SEEK_SET);

    fwrite(&length, 4, 1, fc);

    for (int i=0; i<length; i+=4)
    {
        dword p;
        fread(&p, 4, 1, fp);
        dword k = genrand_int32();
        dword c = p^k;

        fwrite(&c, 4, 1, fc);
        fwrite(&k, 4, 1, fk);
    }

    fclose(fp);
    fclose(fc);
    fclose(fk);
}

void decrypt(const char *plain, const char *crypt, const char *key)
{
    FILE *fp = fopen(plain, "wb");
    if (fp==NULL)
    {
        printf("Failed to open %s\n", plain);
        exit(-1);
    }
    FILE *fc = fopen(crypt, "rb");
    if (fc==NULL)
    {
        printf("Failed to open %s\n", crypt);
        exit(-1);
    }
    FILE *fk = fopen(key, "rb");
    if (fk==NULL)
    {
        printf("Failed to open %s\n", key);
        exit(-1);
    }

    dword length;
    fread(&length, 4, 1, fc);

    for (int i=0; i<length; i+=4)
    {
        dword c;
        fread(&c, 4, 1, fc);
        dword k;
        fread(&k, 4, 1, fk);
        dword p = c^k;

        fwrite(&p, min(4,length-i), 1, fp);
    }

    fclose(fp);
    fclose(fc);
    fclose(fk);
}

static unsigned long mt[N]; /* the array for the state vector  */
static int mti=N+1; /* mti==N+1 means mt[N] is not initialized */

/* initializes mt[N] with a seed */
void init_genrand(unsigned long s)
{
    mt[0]= s & 0xffffffffUL;
    for (mti=1; mti<N; mti++) {
        mt[mti] =
	    (1812433253UL * (mt[mti-1] ^ (mt[mti-1] >> 30)) + mti);
        /* See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier. */
        /* In the previous versions, MSBs of the seed affect   */
        /* only MSBs of the array mt[].                        */
        /* 2002/01/09 modified by Makoto Matsumoto             */
        mt[mti] &= 0xffffffffUL;
        /* for >32 bit machines */
    }
}

/* initialize by an array with array-length */
/* init_key is the array for initializing keys */
/* key_length is its length */
/* slight change for C++, 2004/2/26 */
void init_by_array(unsigned long init_key[], int key_length)
{
    int i, j, k;
    init_genrand(19650218UL);
    i=1; j=0;
    k = (N>key_length ? N : key_length);
    for (; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525UL))
          + init_key[j] + j; /* non linear */
        mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
        i++; j++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
        if (j>=key_length) j=0;
    }
    for (k=N-1; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941UL))
          - i; /* non linear */
        mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
        i++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
    }

    mt[0] = 0x80000000UL; /* MSB is 1; assuring non-zero initial array */
}

/* generates a random number on [0,0xffffffff]-interval */
unsigned long genrand_int32(void)
{
    unsigned long y;
    static unsigned long mag01[2]={0x0UL, MATRIX_A};
    /* mag01[x] = x * MATRIX_A  for x=0,1 */

    if (mti >= N) { /* generate N words at one time */
        int kk;

        if (mti == N+1)   /* if init_genrand() has not been called, */
            init_genrand(5489UL); /* a default initial seed is used */

        for (kk=0;kk<N-M;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        for (;kk<N-1;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1UL];

        mti = 0;
    }

    y = mt[mti++];

    /* Tempering */
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);

    return y;
}

/* generates a random number on [0,0x7fffffff]-interval */
long genrand_int31(void)
{
    return (long)(genrand_int32()>>1);
}

/* generates a random number on [0,1]-real-interval */
double genrand_real1(void)
{
    return genrand_int32()*(1.0/4294967295.0);
    /* divided by 2^32-1 */
}

/* generates a random number on [0,1)-real-interval */
double genrand_real2(void)
{
    return genrand_int32()*(1.0/4294967296.0);
    /* divided by 2^32 */
}

/* generates a random number on (0,1)-real-interval */
double genrand_real3(void)
{
    return (((double)genrand_int32()) + 0.5)*(1.0/4294967296.0);
    /* divided by 2^32 */
}

/* generates a random number on [0,1) with 53-bit resolution*/
double genrand_res53(void)
{
    unsigned long a=genrand_int32()>>5, b=genrand_int32()>>6;
    return(a*67108864.0+b)*(1.0/9007199254740992.0);
}
/* These real versions are due to Isaku Wada, 2002/01/09 added */

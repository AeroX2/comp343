#include <iostream>
#include <math.h>

#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <gmpxx.h>

#include <sparsepp/spp.h>
using spp::sparse_hash_map;

unsigned int i = 0;
void interupt_handler(int s){
   printf("Caught signal %d, currently at %d\n",s,i);
   exit(1); 
}

/* Shanks' baby-step giant-step for finding discrete logarithms 
           a^x mod n = y, solve for x
*/
int main(int argc, char** argv)
{
	struct sigaction sigIntHandler; 
	sigIntHandler.sa_handler = interupt_handler;
	sigemptyset(&sigIntHandler.sa_mask);
	sigIntHandler.sa_flags = 0;
	sigaction(SIGINT, &sigIntHandler, NULL);

	sparse_hash_map<unsigned long, unsigned int> B;

	unsigned long y = strtoul(argv[1],NULL,10);
	unsigned long a = strtoul(argv[2],NULL,10);
	unsigned long n = strtoul(argv[3],NULL,10);

    unsigned long s = (unsigned long) ceil(sqrt(n));
    mpz_class l = a%n;
	mpz_class o;
	mpz_class base = a;
	mpz_class mod = n;
	mpz_powm_ui(o.get_mpz_t(), base.get_mpz_t(), s, mod.get_mpz_t());
    mpz_class q = y%n;

	B.reserve(s);
    for (i=0; i < s; i++) {
        B[q.get_ui()] = i; 
		q = (q*l)%n;
	}

	mpz_class z = o;
	for (i=0; i < s; i++) {
		auto test = B.find(z.get_ui());
		if (test != B.end()) {
            unsigned long r = test->second;
            unsigned long st = (i + 1) * s;
			std::cout << st - r << std::endl;
			break;
		}
        z = (z*o)%n;
	}

    return 0;
}

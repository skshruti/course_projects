#include<pthread.h>
#include<stdlib.h>
#include<string.h>
#include<stdio.h>
#include<math.h>
#include<stdbool.h>
#include <stdio.h> 
#include <time.h> 
  
typedef struct array{
	int* value;
	int size;
}array; 

typedef struct argument{
	array* primes;
	int* marked;
	int start;
	int end;

}argument; 

double thread_times[10];
int sizeThreadTimes=0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
bool isPrime(int n){
	for(int i=2;i<=sqrt(n);i++){
		if(n%i==0) return false;
	}
	return true;
}
void* staticPrime(argument* markedLimit){
	struct timespec start, finish;
	double elapsed;

	clock_gettime(CLOCK_MONOTONIC, &start);

	if(markedLimit->start==0) markedLimit->start=2;
	for(int i=markedLimit->start;i<markedLimit->end;i++){
		if(isPrime(i)==true){
			pthread_mutex_lock(&mutex);
			markedLimit->primes->value[markedLimit->primes->size]=i;
			markedLimit->primes->size++;
			pthread_mutex_unlock(&mutex);
		}
	}
	clock_gettime(CLOCK_MONOTONIC, &finish);

	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
	thread_times[sizeThreadTimes++]=elapsed;

	pthread_exit(NULL);	
}

int main(int argc, char **argv){
	long t;
	int n=atoi(argv[1]);
	int nthreads=atoi(argv[2]);


	int marked[n];
	array *primes=malloc(sizeof(array));
	int* primeValues=malloc((n/2)*sizeof(int));
	primes->value=primeValues;

	pthread_t *threads=malloc(t*sizeof(pthread_t));

	for(t=0;t<nthreads;t++){
		argument* markedLimit=(argument*)malloc(sizeof(argument));
		markedLimit->marked=marked;
		markedLimit->start=t*n/nthreads;
		markedLimit->end=(t+1)*n/nthreads;
		markedLimit->primes=primes;
		//printf("entered thread%ld\n", t);
		int rc = pthread_create(&threads[t], NULL, (void*)staticPrime, (void*)markedLimit);
		//printf("exited thread%ld\n", t);
		if(rc){
			printf("ERRORRR %d\n", rc);
			exit(-1);
		}
	}

	for(t=0;t<nthreads;t++){
		pthread_join(threads[t],NULL);
	}

	// FILE *primeFile;
	// primeFile=fopen("result/primes.txt","w");
	// for(int i=0;i<primes->size;i++){
	// 	fprintf(primeFile, "%d\n", primes->value[i]);
	// }
	// fclose(primeFile);

	FILE *temp;
	temp=fopen("output/data_static.txt","w");
	for(int i=0;i<nthreads;i++){
		fprintf(temp,"%d %f\n",i+1, thread_times[i]);
	}
	for(int i=0;i<primes->size;i++){
		fprintf(temp, "%d\n", primes->value[i]);
	}
    fclose(temp);
	pthread_exit(NULL);

	return 0;
}
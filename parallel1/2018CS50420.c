/*

COL380. assignment 1.

Deadline: 12.03.2021

Problem: 

Compute the sum of the First N natural numbers. 

The sequential version is provided below.

1. Develop two parallel versions of the given program using OpenMP `parallel for' with maximum 8 threads.

Compilation command: gcc -O0 ...

2. The speedup and efficiency of both parallel versions for 2, 4, 8 threads for N=10^3, N=10^5 and N=10^7 numbers.

3. Does the speedup follow Amdahl's law?

Hint: Use a time function in the program (e.g. omp_get_wtime) to measure the time.

*/

#include <omp.h> 
  
#include <stdio.h> 
#include <stdlib.h> 
#include <math.h> 



int serialized(int N, int t){
   unsigned long long sum=0;
   unsigned long long *a;
   a = (unsigned long long *)malloc(sizeof(unsigned long long)*N);

   a[0] = 1;
   double start = omp_get_wtime(); 
   
   for(int i=1;i<N;i++) {
      a[i] = a[i-1]+1;  
   }

   for(int i=0;i<N;i++) {
      sum+=a[i];
   } 
   printf("%llu\n", sum);
   double end = omp_get_wtime(); 
   //printf("Work took %f seconds\n", end - start);
   free(a);     
}

int parallel1(int N, int t){
   omp_set_num_threads(8);
   unsigned long long sum=0;
   unsigned long long *a;
   a = (unsigned long long *)malloc(sizeof(unsigned long long)*N);

   a[0] = 1;
   double start = omp_get_wtime(); 
   int i;
   for(i=1;i<N;i++) {
      a[i] = a[i-1]+1;  
   }

   unsigned long long* partialSums=(unsigned long long *)malloc(sizeof(unsigned long long)*t);
  
   #pragma omp parallel for 
   for(int i=0;i<t;i++) {
      unsigned long long sum_i=0;
      for(int j=(i*N)/t;j<((i+1)*N)/t;j++){
         sum_i+=a[j];
      }
      #pragma omp critical
      {
      partialSums[i]=sum_i;
      }
   } 

   for(int i=0;i<t;i++) {
      sum+=partialSums[i];
   } 

   printf("%llu\n", sum);
   double end = omp_get_wtime(); 
   //printf("Work took %f seconds\n", end - start);
   free(a);     
}

int parallel2(int N, int t){
   omp_set_num_threads(8);
   unsigned long long sum=0;
   unsigned long long *a;
   a = (unsigned long long *)malloc(sizeof(unsigned long long)*N);

   a[0] = 1;
   double start = omp_get_wtime(); 
   
   for(int i=1;i<N;i++) {
      a[i] = a[i-1]+1;  
   }
   
   int c=N;
   int weight=1;
   while(c>1){
      #pragma omp parallel for
      for(int i=0;i<N-weight;i+=2*weight) {
         a[i]=a[i]+a[(i+weight)];
      }
      c=(c+1)/2;
      weight*=2;
   }
   sum=a[0];

   printf("%llu\n", sum);
   double end = omp_get_wtime(); 
   //printf("Work took %f seconds\n", end - start);
   free(a);  
}


int main(int argc, char* argv[]) 
{ 
   int strategy=atoi(argv[1]);
   int N=atoi(argv[2]);
   int t=atoi(argv[3]);
   if(strategy==0) parallel1(N,t);
   else if(strategy==-1) serialized(N,t);
   else parallel2(N,t);
   // printf("SERIALIZED\n");
   // serialized(N,t);
   // printf("PARALLEL1\n");
   // parallel1(N,t);
   // printf("PARALLEL2\n");
   // parallel2(N,t);
} 
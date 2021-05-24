#include<stdlib.h>
#include<stdio.h>
#include<mpi.h>
#include<time.h>
#include<omp.h>
#include <string.h>
void write_output(char fname[], double** arr, int n ){
	FILE *f = fopen(fname, "w");
	if(f==NULL){
		printf("FILE NOT FOUND\n");
	}
	for( int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			//printf("adding to %s\n",fname);
			fprintf(f, "%0.12f ", arr[i][j]);
		}
		fprintf(f, "\n");
	}
	fclose(f);
	//printf("hi\n");
}

void print_matrix(double** arr, int n ){
	for( int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			printf("%0.12f ", arr[i][j]);
		}
		printf("\n");
	}
}

double **alloc_2d_matrix(int rows, int cols) {
    double *data = (double *)malloc(rows*cols*sizeof(double));
    double **array= (double **)malloc(rows*sizeof(double*));
    for (int i=0; i<rows; i++)
        array[i] = &(data[cols*i]);

    return array;
}

int main(int argc, char* argv[]){
	int my_rank, comm_sz;	
	int source;
	int n_threads=0;
	int n=atoi(argv[1]);
	char* filename=argv[2];
	srand(time(0));
    double **A;
    A = alloc_2d_matrix(n,n);
    double **L;
    L = alloc_2d_matrix(n,n);
    double **U;
    U = alloc_2d_matrix(n,n);
    
    FILE *fptr;
    fptr=fopen(filename,"r");
	int p, q;
	for (p = 0; p < n; p++){
		for (q = 0; q < n; q++){
	    	fscanf(fptr, "%lf", &A[p][q]);
		}
	}
	fclose(fptr);
	for (p = 0; p < n; p++) {
		U[p][p] = 1;
	}

	double startTime = omp_get_wtime(); 
	MPI_Init(NULL,NULL);
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
	n_threads=comm_sz;
	int ierr;
	int chunk,start,end,extra;
	int i,k;
	double sumL=0;
	double sumU=0;
	double total_sumL=0;
	double total_sumU=0;
	int firstTime=1;
	
	for(int j=0;j<n;j++){
		for (i = j; i < n; i++) {
			if(firstTime==0 && my_rank!=0){
				MPI_Recv(&(L[0][0]),n*n,MPI_DOUBLE,0,3,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
				MPI_Recv(&(U[0][0]),n*n,MPI_DOUBLE,0,3,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
			}
			firstTime=0;
			chunk=j/comm_sz;
			extra=j - (chunk*(comm_sz));
			start=my_rank*chunk;
			if(extra>0) start+=extra;
			end=start+chunk;
			if(my_rank<extra){
				start=my_rank*chunk+my_rank;
				end=start+chunk+1;
			}
			sumL = 0;
			sumU = 0;
			for (k = start; k < end; k++) {
				sumL = sumL + L[i][k] * U[k][j];	
				sumU = sumU + L[j][k] * U[k][i];
			}
			if(my_rank!=0){
				MPI_Send(&sumL,1,MPI_DOUBLE,0,0,MPI_COMM_WORLD);
				MPI_Send(&sumU,1,MPI_DOUBLE,0,1,MPI_COMM_WORLD);
			}
			else{
				total_sumL=sumL;
				total_sumU=sumU;
				for(source=1;source<comm_sz;source++){
					MPI_Recv(&sumL,1,MPI_DOUBLE,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
					total_sumL+=sumL;
					MPI_Recv(&sumU,1,MPI_DOUBLE,source,1,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
					total_sumU+=sumU;
				}
				L[i][j] = A[i][j] - total_sumL;
				
				if (L[j][j] == 0) {	
					//printf("uh oh\n");
					exit(0);
				}
				U[j][i] = (A[j][i] - total_sumU) / L[j][j];
				if(i<n-1 || j<n-1){
					for(source=1;source<comm_sz;source++){
						MPI_Send(&(L[0][0]),n*n,MPI_DOUBLE,source,3,MPI_COMM_WORLD);
						MPI_Send(&(U[0][0]),n*n,MPI_DOUBLE,source,3,MPI_COMM_WORLD);
					}
				}
			}
		}
		
	}

	if(my_rank==0){
		//printf("reached here");
		char result[50];
	    sprintf(result, "%d", n_threads);
	    //printf("%s\n", result);
		char file_L[50]="output_L_4_";
		strcat(file_L,result);  
		strcat(file_L,".txt");
		write_output(file_L,L,n);
		char file_U[50]="output_U_4_";
		strcat(file_U,result);  
		strcat(file_U,".txt");
		write_output(file_U,U,n);
		double endTime = omp_get_wtime(); 
    	//printf("Crout4 took %f seconds\n", endTime - startTime);
	}

	MPI_Finalize();
	
	return 0;
}

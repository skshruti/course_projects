#include<stdlib.h>
#include<stdio.h>
#include<omp.h>
#include<time.h>
#include<string.h>

void write_output(char fname[], double** arr, int n );
void crout0(double const **A, double **L, double **U, int n, int n_threads) {
	double start = omp_get_wtime(); 
	int i, j, k;
	double sum = 0;
	for (i = 0; i < n; i++) {
		U[i][i] = 1;
	}
	for (j = 0; j < n; j++) {
		for (i = j; i < n; i++) {
			sum = 0;
			for (k = 0; k < j; k++) {
				sum = sum + L[i][k] * U[k][j];	
			}
			L[i][j] = A[i][j] - sum;
		}
		for (i = j; i < n; i++) {
			sum = 0;
			for(k = 0; k < j; k++) {
				sum = sum + L[j][k] * U[k][i];
			}
			if (L[j][j] == 0) {	
				exit(0);
			}
			U[j][i] = (A[j][i] - sum) / L[j][j];
		}
	}
	//write_output("Lower/L0.txt",L,n);
	//write_output("Upper/U0.txt",U,n);
	char result[50];
	sprintf(result, "%d", n_threads);
	char file_L[50]="output_L_0_";
	strcat(file_L,result);  
	strcat(file_L,".txt");
	write_output(file_L,L,n);
	char file_U[50]="output_U_0_";
	strcat(file_U,result);  
	strcat(file_U,".txt");
	write_output(file_U,U,n);
	double end = omp_get_wtime(); 
    //printf("Crout0 took %f seconds\n", end - start);
}	

void crout1(double const **A, double **L, double **U, int n, int n_threads) {
	double start = omp_get_wtime(); 
	int i, j, k;
	double sum = 0;
	for (i = 0; i < n; i++) {
		U[i][i] = 1;
	}
	for (j = 0; j < n; j++) {
		// printf("holaa\n");
		#pragma omp parallel for private(i, k, sum) shared(j, A, L, U)
		for (i = j; i < n; i++) {
			sum = 0;
			for (k = 0; k < j; k++) {
				sum = sum + L[i][k] * U[k][j];	
			}
			L[i][j] = A[i][j] - sum;
		}
		#pragma omp parallel for private(i, k, sum) shared(j, A, L, U)
		for (i = j; i < n; i++) {
			sum = 0;
			for(k = 0; k < j; k++) {
				sum = sum + L[j][k] * U[k][i];
			}
			if (L[j][j] == 0) {			
				exit(0);
			}
			U[j][i] = (A[j][i] - sum) / L[j][j];
		}
	}
	//write_output("Lower/L1.txt",L,n);
	//write_output("Upper/U1.txt",U,n);
	char result[50];
	sprintf(result, "%d", n_threads);
	char file_L[50]="output_L_1_";
	strcat(file_L,result);  
	strcat(file_L,".txt");
	write_output(file_L,L,n);
	char file_U[50]="output_U_1_";
	strcat(file_U,result);  
	strcat(file_U,".txt");
	write_output(file_U,U,n);
	double end = omp_get_wtime(); 
    //printf("Crout1 took %f seconds\n", end - start);
}

void crout2(double const **A, double **L, double **U, int n, int n_threads) {
	double start = omp_get_wtime(); 
	int i, j, k;
	double sum = 0;
	for (i = 0; i < n; i++) {
		U[i][i] = 1;
	}
	
	for (j = 0; j < n; j++) {
		sum = 0;
		for (k = 0; k < j; k++) {
			sum = sum + L[j][k] * U[k][j];	
		}
		L[j][j] = A[j][j] - sum;
		#pragma omp parallel shared(A, L, U, j)
		{
		#pragma omp sections private(i, k, sum)
		{
			#pragma omp section
			{
				for (i = j+1; i < n; i++) {
					sum = 0;
					for (k = 0; k < j; k++) {
						sum = sum + L[i][k] * U[k][j];	
					}
					L[i][j] = A[i][j] - sum;
				}
			}
			#pragma omp section
			{
				for (i = j; i < n; i++) {
					sum = 0;
					for(k = 0; k < j; k++) {
						sum = sum + L[j][k] * U[k][i];
					}
					if (L[j][j] == 0) {	
						exit(0);
					}
					U[j][i] = (A[j][i] - sum) / L[j][j];
				}
			}
		}}
	}
	//write_output("Lower/L2.txt",L,n);
	//write_output("Upper/U2.txt",U,n);
	char result[50];
	sprintf(result, "%d", n_threads);
	char file_L[50]="output_L_2_";
	strcat(file_L,result);  
	strcat(file_L,".txt");
	write_output(file_L,L,n);
	char file_U[50]="output_U_2_";
	strcat(file_U,result);  
	strcat(file_U,".txt");
	write_output(file_U,U,n);
	double end = omp_get_wtime(); 
    //printf("Crout2 took %f seconds\n", end - start);
}

void crout3(double const **A, double **L, double **U, int n, int n_threads) {
	//printf("here!\n");
	double start = omp_get_wtime(); 
	int i, j, k;
	double sum = 0;
	for (i = 0; i < n; i++) {
		U[i][i] = 1;
	}
	
	for (j = 0; j < n; j++) {
		sum = 0;
		for (k = 0; k < j; k++) {
			sum = sum + L[j][k] * U[k][j];	
		}
		L[j][j] = A[j][j] - sum;
		// printf("yes %d\n", j);
		#pragma omp parallel shared(A, L, U, j)
		{
		#pragma omp sections private(i, k, sum)
		{
			#pragma omp section
			{
				#pragma omp parallel for private(i, k, sum) shared(j, A, L, U)
				for (i = j+1; i < n; i++) {
					sum = 0;
					for (k = 0; k < j; k++) {
						sum = sum + L[i][k] * U[k][j];	
					}
					L[i][j] = A[i][j] - sum;
				}
			}
			#pragma omp section
			{
				#pragma omp parallel for private(i, k, sum) shared(j, A, L, U)
				for (i = j; i < n; i++) {
					sum = 0;
					for(k = 0; k < j; k++) {
						sum = sum + L[j][k] * U[k][i];
					}
					if (L[j][j] == 0) {	
						exit(0);
					}
					U[j][i] = (A[j][i] - sum) / L[j][j];
				}
			}
		}}
	}
	//write_output("Lower/L3.txt",L,n);
	//write_output("Upper/U3.txt",U,n);
	char result[50];
	sprintf(result, "%d", n_threads);
	char file_L[50]="output_L_3_";
	strcat(file_L,result);  
	strcat(file_L,".txt");
	write_output(file_L,L,n);
	char file_U[50]="output_U_3_";
	strcat(file_U,result);  
	strcat(file_U,".txt");
	write_output(file_U,U,n);
	//printf("done\n");
	double end = omp_get_wtime(); 
    //printf("Crout3 took %f seconds\n", end - start);
}

void write_output(char fname[], double** arr, int n ){
	FILE *f = fopen(fname, "w");
	if(f==NULL){
		printf("FILE NOT FOUND\n");
	}
	for( int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			fprintf(f, "%0.12f ", arr[i][j]);
		}
		fprintf(f, "\n");
	}
	fclose(f);
}

int main(int argc, char* argv[]) 
{ 
	int n=atoi(argv[1]);
	char* filename=argv[2];
	int strategy=atoi(argv[4]);
	int n_threads=atoi(argv[3]);
	//printf("filename:: %s\n",filename);
	srand(time(0));
	double **matrix = (double **) malloc(n * sizeof(double*));   
    double **L = (double **) malloc(n * sizeof(double*));  
    double **U = (double **) malloc(n * sizeof(double*));   
    for (int i = 0; i < n; i++) {
        matrix[i] = (double *) malloc(n * sizeof(double));
        L[i] = (double *) malloc(n * sizeof(double));
        U[i] = (double *) malloc(n * sizeof(double));
    } 
    
	// int i, j;
	// for (i = 0; i < n; i++){
	// 	for (j = 0; j < n; j++){
	//     	matrix[i][j]=(rand() % (10)); 
	// 	}
	// }

	FILE *fptr;
    fptr=fopen(filename,"r");
	int p, q;
	for (p = 0; p < n; p++){
		for (q = 0; q < n; q++){
	    	fscanf(fptr, "%lf", &matrix[p][q]);
		}
	}
	fclose(fptr);
	
	omp_set_nested(1);
	omp_set_dynamic(0); 
	omp_set_num_threads(n_threads);

	//write_output("matrix.txt",matrix,n);
	if(strategy==0) crout0((double const **) matrix, L, U, n, n_threads);
	if(strategy==1) crout1((double const **) matrix, L, U, n, n_threads);
	if(strategy==2) crout2((double const **) matrix, L, U, n, n_threads);
	if(strategy==3) {
		//printf("hello\n");
		crout3((double const **) matrix, L, U, n,n_threads);
	}
	free(matrix);
	free(L);
	free(U);
	return 0;
} 
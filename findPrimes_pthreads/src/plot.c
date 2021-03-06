#include<pthread.h>
#include<stdlib.h>
#include<string.h>
#include<stdio.h>
#include<math.h>
#include<stdbool.h>

int main(int argc, char **argv){
 	FILE *gnuplotpipe;
	gnuplotpipe = popen("gnuplot -persistent", "w");
	fprintf(gnuplotpipe, "set title \"Time taken by ith thread\"\n");
	fprintf(gnuplotpipe, "set terminal png\n");
	fprintf(gnuplotpipe, "set output \"../output/plot.png\"\n");
	fprintf(gnuplotpipe, "set xlabel \"i\"\n");
	fprintf(gnuplotpipe, "set ylabel \"Naive\"\n");
	fprintf(gnuplotpipe, "set y2label \"Load Balanced\"\n");
	fprintf(gnuplotpipe, "set y2range [0:1]\n");
	fprintf(gnuplotpipe, "set y2tics border nomirror\n");
	fprintf(gnuplotpipe, "set ytics border nomirror\n");
	fprintf(gnuplotpipe, "plot '../output/data_static.txt' using 1:2 w lp axis x1y1 title 'Naive', '../output/data_dynamic.txt' using 1:2 w lp axis x1y2 title 'Load balanced'\n");
	fclose(gnuplotpipe);

	return 0;

}
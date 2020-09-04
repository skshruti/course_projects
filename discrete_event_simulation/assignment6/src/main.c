#include"../include/eventQueue.h"
#include<stdlib.h>
#include<stdio.h>

float simulateCommon(int noCust, int noTell, float simulationTime, float avgStime){
	eventQueue* queue=createQueue();
	tellerQueue* commonQueue=createTellerQ();
	tellerQueueList* tQL=createTQL();
	int i=0;
	while(i<noCust){
		cust cnull=createCust(0);
		teller tnull=createTeller(0);
		float arrTime = simulationTime * (rand()/(float)(RAND_MAX));
		cust customer=createCust(arrTime);
		event eve=createEvent("cust",customer,tnull);
		add(eve,queue);
		i++;
	}
	int j=0;
	while(j<noTell){
		cust cnull=createCust(0);
		teller tnull=createTeller(0);
		float serviceTime = 2*avgStime*rand()/(float)(RAND_MAX);
		float idTime = rand()/(float)(ID_MAX);
		float arrTime = simulationTime * (rand()/(float)(RAND_MAX));
		teller tell=createTeller(arrTime);
		event eve=createEvent("teller",cnull,tell);
		add(eve,queue);
		addtQL(tell.tQ,tQL);
		j++;
	}

	while((*queue).head!=pNull){
		actionSingle((*queue).head->data,queue,commonQueue,avgStime);
	}

	float avgTimeSpent=(*queue).timeSpent/(*queue).custServed;
	float deviation=0;
	calculateStd((*queue).dataList,avgTimeSpent,&deviation);
	printf("=>No. of tellers:: %d;type:: COMMON\n",noTell);
	printf("=>Total customers served:: %d\n",(*queue).custServed);
	printf("=>Average Time Spent:: %f\n",avgTimeSpent);
	printf("=>Standard deviation:: %f\n",deviation);
	printf("=>Maximum Waiting Time:: %f\n",(*queue).maxWaitTime);
	printf("=>Total tellerServiceTime:: %f\n",(*queue).totServiceTime);
	printf("=>Total tellerIdleTime:: %f\n",(*queue).totIdleTime);

	return avgTimeSpent;	
}

void simulateSeperate(int noCust, int noTell, float simulationTime, float avgStime){
	eventQueue* queue=createQueue();
	tellerQueue* commonQueue=createTellerQ();
	tellerQueueList* tQL=createTQL();
	int i=0;
	while(i<noCust){
		cust cnull=createCust(0);
		teller tnull=createTeller(0);
		float arrTime = simulationTime * (rand()/(float)(RAND_MAX));
		cust customer=createCust(arrTime);
		event eve=createEvent("cust",customer,tnull);
		add(eve,queue);
		i++;
	}
	int j=0;
	while(j<noTell){
		cust cnull=createCust(0);
		teller tnull=createTeller(0);
		float serviceTime = 2*avgStime*rand()/(float)(RAND_MAX);
		float idTime = rand()/(float)(ID_MAX);
		float arrTime = simulationTime * (rand()/(float)(RAND_MAX));
		teller tell=createTeller(arrTime);
		event eve=createEvent("teller",cnull,tell);
		add(eve,queue);
		addtQL(tell.tQ,tQL);
		j++;
	}
	while((*queue).head!=pNull){
		actionMulti((*queue).head->data,queue,tQL,avgStime);
	}

	float avgTimeSpent=(*queue).timeSpent/(*queue).custServed;
	float deviation=0;
	calculateStd((*queue).dataList,avgTimeSpent,&deviation);
	printf("=>No. of tellers:: %d;type:: ONE PER TELLER\n",noTell);
	printf("=>Total customers served:: %d\n",(*queue).custServed);
	printf("=>Average Time Spent:: %f\n",avgTimeSpent);
	printf("=>Standard deviation:: %f\n",deviation);
	printf("=>Maximum Waiting Time:: %f\n",(*queue).maxWaitTime);
	printf("=>Total tellerServiceTime:: %f\n",(*queue).totServiceTime);
	printf("=>Total tellerIdleTime:: %f\n",(*queue).totIdleTime);

	return;	
}


int main(int argc, char **argv){
	int noCust=atoi(argv[1]);
	int noTeller=atoi(argv[2]);
	float simulationTime=atof(argv[3]);
	float averageServiceTime=atof(argv[4]);

	simulateSeperate(noCust,noTeller,simulationTime,averageServiceTime);
	simulateCommon(noCust,noTeller,simulationTime,averageServiceTime);
	printf("\n\n\nplotting the graph\n\n");
	FILE *temp;
    int count=1;
    temp=fopen("obj/data.txt","w");
    while(count<=20){
        fprintf(temp,"%d %0.2f\n",count, simulateCommon(noCust,count,simulationTime,averageServiceTime));
        count++;
    }
    fclose(temp);
    
    FILE *gnuplotpipe;
    gnuplotpipe = popen("gnuplot -persistent", "w");
    fprintf(gnuplotpipe, "set title \"Average Time Spent by a Customer in case of Common Queue\"\n");
    fprintf(gnuplotpipe, "set xlabel \"Number of Tellers\"\n");
    fprintf(gnuplotpipe, "set ylabel \"Average Time Spent by the customers (in minutes) \"\n");
    fprintf(gnuplotpipe, "set terminal png\n");
    fprintf(gnuplotpipe, "set output \"output/AverageTimeSpent.png\"\n");
    fprintf(gnuplotpipe, "plot \"obj/data.txt\" smooth csplines lt 5 title \"Line of best fit\", \"obj/data.txt\" using 1:2 ls 5 title \"Points\" \n");
    fclose(gnuplotpipe);
    printf("\n\nplotted\n");
	
}
